// src/lib.rs
#![recursion_limit = "512"]

use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict};
use numpy::{PyArray2, PyArray1};
use ndarray::{Array1, Array2, ArrayView1, ArrayView2, Axis, s, Zip};
use ndarray::linalg::Dot; // BLAS–backed dot products
use statrs::distribution::{Continuous, ContinuousCDF, Normal};
use thiserror::Error;
use std::collections::HashSet;

#[derive(Error, Debug)]
pub enum AnalysisError {
    #[error("Model attribute missing: {0}")]
    ModelAttributeError(String),
    #[error("Numerical error in calculation")]
    NumericalError,
    #[error("Invalid variable type specification")]
    VariableTypeError,
}

impl std::convert::From<AnalysisError> for PyErr {
    fn from(err: AnalysisError) -> PyErr {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(err.to_string())
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum VariableType {
    Continuous,
    Discrete, // e.g. dummy variable with only 0 and 1 outcomes
}

/// Checks if, when rounded (after multiplying by 1000), the only unique values are 0 and 1000.
fn detect_variable_types(X: &Array2<f64>) -> Vec<VariableType> {
    X.columns()
        .into_iter()
        .map(|col| {
            let unique_vals: HashSet<i64> = col
                .mapv(|v| (v * 1000.0).round() as i64)
                .iter()
                .copied()
                .collect();
            let is_dummy = unique_vals.len() == 2 && unique_vals.iter().all(|&v| v == 0 || v == 1000);
            if is_dummy {
                VariableType::Discrete
            } else {
                VariableType::Continuous
            }
        })
        .collect()
}

#[pyfunction]
fn add_significance_stars(p: f64) -> &'static str {
    if p < 0.001 {
        "***"
    } else if p < 0.01 {
        "**"
    } else if p < 0.05 {
        "*"
    } else if p < 0.1 {
        "."
    } else {
        ""
    }
}

fn as_array2_f64<'py>(obj: &'py PyAny) -> PyResult<ArrayView2<'py, f64>> {
    // Safety: caller must ensure that the PyArray2 contains valid f64 data.
    let array = unsafe {
        obj.downcast::<PyArray2<f64>>()
            .map_err(|_| AnalysisError::ModelAttributeError("Expected 2D f64 array".into()))?
            .as_array()
    };
    Ok(array)
}

fn as_array1_f64<'py>(obj: &'py PyAny) -> PyResult<ArrayView1<'py, f64>> {
    // Safety: caller must ensure that the PyArray1 contains valid f64 data.
    let array = unsafe {
        obj.downcast::<PyArray1<f64>>()
            .map_err(|_| AnalysisError::ModelAttributeError("Expected 1D f64 array".into()))?
            .as_array()
    };
    Ok(array)
}

#[derive(Debug, Clone, Copy)]
enum ModelType {
    Logit,
    Probit,
    OrderedLogit,
    OrderedProbit,
    Multinomial,
    Poisson,
    NegativeBinomial,
    Unknown,
}

fn detect_model_type(model: &PyAny) -> PyResult<ModelType> {
    let model_obj = model.get_item("model")
        .map_err(|_| AnalysisError::ModelAttributeError("model".into()))?;
    let class_name: String = model_obj.getattr("__class__")?
        .getattr("__name__")?
        .extract()?;
    let lower_name = class_name.to_lowercase();

    if lower_name.contains("ordered") {
        let distr_obj = model_obj.getattr("distr")
            .map_err(|_| AnalysisError::ModelAttributeError("distr".into()))?;
        let distr_name: String = distr_obj.getattr("__class__")?
            .getattr("__name__")?
            .extract()?;
        match distr_name.to_lowercase().as_str() {
            s if s.contains("logistic") => Ok(ModelType::OrderedLogit),
            s if s.contains("normal") => Ok(ModelType::OrderedProbit),
            _ => Ok(ModelType::Unknown),
        }
    } else if lower_name.contains("logit") {
        Ok(ModelType::Logit)
    } else if lower_name.contains("probit") {
        Ok(ModelType::Probit)
    } else if lower_name.contains("mnlogit") {
        Ok(ModelType::Multinomial)
    } else if lower_name.contains("poisson") {
        Ok(ModelType::Poisson)
    } else if lower_name.contains("negativebinomial") {
        Ok(ModelType::NegativeBinomial)
    } else {
        Ok(ModelType::Unknown)
    }
}

fn extract_model_components(model: &PyAny) -> PyResult<(Array1<f64>, Array2<f64>, Vec<String>, Array2<f64>)> {
    let params = model.get_item("params")
        .map_err(|_| AnalysisError::ModelAttributeError("params".into()))?;
    let beta = as_array1_f64(params)?.to_owned();

    let cov = model.call_method0("cov_params")
        .map_err(|_| AnalysisError::ModelAttributeError("cov_params".into()))?;
    let cov_beta = as_array2_f64(cov)?.to_owned();

    let model_obj = model.get_item("model")
        .map_err(|_| AnalysisError::ModelAttributeError("model".into()))?;
    let exog_names: Vec<String> = model_obj.get_item("exog_names")?
        .extract()?;

    let x_obj = model_obj.get_item("exog")
        .map_err(|_| AnalysisError::ModelAttributeError("exog".into()))?;
    let X = as_array2_f64(x_obj)?.to_owned();

    Ok((beta, cov_beta, exog_names, X))
}

/// Compute marginal effects for binary models (Logit/Probit).
fn compute_binary_margins(
    beta: &Array1<f64>,
    X: &Array2<f64>,
    cov_beta: &Array2<f64>,
    var_types: &[VariableType],
    is_logit: bool,
) -> Result<(Array1<f64>, Array1<f64>), AnalysisError> {
    let n_features = X.ncols();
    let mut ame = Array1::zeros(n_features);
    let mut jacobian = Array2::zeros((n_features, beta.len()));
    let normal = Normal::new(0.0, 1.0).map_err(|_| AnalysisError::NumericalError)?;

    let xb = X.dot(beta); // BLAS–backed

    for (idx, &vtype) in var_types.iter().enumerate() {
        if vtype == VariableType::Discrete {
            let mut X_plus = X.to_owned();
            X_plus.column_mut(idx).fill(1.0);
            let mut X_minus = X.to_owned();
            X_minus.column_mut(idx).fill(0.0);

            if is_logit {
                let z_plus = -X_plus.dot(beta);
                let z_minus = -X_minus.dot(beta);
                let p_plus = 1.0 / (1.0 + z_plus.mapv(|x| x.exp()));
                let p_minus = 1.0 / (1.0 + z_minus.mapv(|x| x.exp()));
                let n = p_plus.len();
                let effect = (p_plus - p_minus).sum() / (n as f64);
                ame[idx] = effect;
                jacobian[[idx, idx]] = effect;
            } else {
                let p_plus = X_plus.dot(beta).mapv(|z| normal.cdf(z));
                let p_minus = X_minus.dot(beta).mapv(|z| normal.cdf(z));
                let n = p_plus.len();
                let effect = (p_plus - p_minus).sum() / (n as f64);
                ame[idx] = effect;
                jacobian[[idx, idx]] = effect;
            }
        } else {
            if is_logit {
                let p = 1.0 / (1.0 + (-&xb).mapv(|z| z.exp()));
                let effect = beta[idx] * (p.sum() / (p.len() as f64));
                ame[idx] = effect;
                let grad = Zip::from(X.column(idx))
                    .and(&p)
                    .fold(0.0, |acc, &a, &b| acc + a * b)
                    / (p.len() as f64);
                jacobian[[idx, idx]] = grad;
            } else {
                let p = xb.mapv(|z| normal.pdf(z));
                let effect = beta[idx] * (p.sum() / (p.len() as f64));
                ame[idx] = effect;
                let grad = Zip::from(X.column(idx))
                    .and(&p)
                    .fold(0.0, |acc, &a, &b| acc + a * b)
                    / (p.len() as f64);
                jacobian[[idx, idx]] = grad;
            }
        }
    }
    let cov_ame = jacobian.dot(cov_beta).dot(&jacobian.t());
    let se = cov_ame.diag().mapv(|v| v.sqrt());
    Ok((ame, se))
}

/// Compute marginal effects for count models.
fn compute_count_margins(
    beta: &Array1<f64>,
    X: &Array2<f64>,
    cov_beta: &Array2<f64>,
    var_types: &[VariableType],
) -> Result<(Array1<f64>, Array1<f64>), AnalysisError> {
    let n_features = X.ncols();
    let mut ame = Array1::zeros(n_features);
    let mut jacobian = Array2::zeros((n_features, beta.len()));

    let xb = X.dot(beta);
    let exp_xb = xb.mapv(|z| z.exp());

    for (idx, &vtype) in var_types.iter().enumerate() {
        if vtype == VariableType::Discrete {
            let mut X_plus = X.to_owned();
            X_plus.column_mut(idx).fill(1.0);
            let mut X_minus = X.to_owned();
            X_minus.column_mut(idx).fill(0.0);

            let rate_plus = X_plus.dot(beta).mapv(|z| z.exp());
            let rate_minus = X_minus.dot(beta).mapv(|z| z.exp());
            let n = rate_plus.len();
            let effect = (rate_plus - rate_minus).sum() / (n as f64);
            ame[idx] = effect;
            jacobian[[idx, idx]] = effect;
        } else {
            let mean_exp = exp_xb.sum() / (exp_xb.len() as f64);
            let effect = beta[idx] * mean_exp;
            ame[idx] = effect;
            for k in 0..X.ncols() {
                let term = Zip::from(exp_xb.view())
                    .and(X.column(k))
                    .fold(0.0, |acc, &a, &b| acc + a * b)
                    / (exp_xb.len() as f64);
                let derivative = if k == idx {
                    mean_exp + beta[idx] * term
                } else {
                    beta[idx] * term
                };
                jacobian[[idx, k]] = derivative;
            }
        }
    }
    let cov_ame = jacobian.dot(cov_beta).dot(&jacobian.t());
    let se = cov_ame.diag().mapv(|v| v.sqrt());
    Ok((ame, se))
}

/// Compute marginal effects for ordered models.
fn compute_ordered_margins(
    beta: &Array1<f64>,
    thresholds: &Array1<f64>,
    X: &Array2<f64>,
    cov_beta: &Array2<f64>,
    var_types: &[VariableType],
    is_logit: bool,
) -> Result<(Array1<f64>, Array1<f64>), AnalysisError> {
    let normal = Normal::new(0.0, 1.0).map_err(|_| AnalysisError::NumericalError)?;
    let n_features = X.ncols();
    let mut ame = Array1::zeros(n_features);
    let mut jacobian = Array2::zeros((n_features, beta.len()));

    // Compute xb once.
    let xb = X.dot(beta);

    for (idx, &vtype) in var_types.iter().enumerate() {
        if vtype == VariableType::Discrete {
            let mut X_plus = X.to_owned();
            X_plus.column_mut(idx).fill(1.0);
            let mut X_minus = X.to_owned();
            X_minus.column_mut(idx).fill(0.0);

            let mut total_effect = 0.0;
            for t in thresholds.iter() {
                if is_logit {
                    let z_plus = *t - X_plus.dot(beta);
                    let exp_neg_z_plus = (-z_plus).mapv(|v| v.exp());
                    let p_plus = 1.0 / (1.0 + exp_neg_z_plus);
                    let z_minus = *t - X_minus.dot(beta);
                    let exp_neg_z_minus = (-z_minus).mapv(|v| v.exp());
                    let p_minus = 1.0 / (1.0 + exp_neg_z_minus);
                    let n = p_plus.len();
                    total_effect += (p_plus - p_minus).sum() / (n as f64);
                } else {
                    let z = *t - X_plus.dot(beta);
                    let p = z.mapv(|v| normal.cdf(v));
                    let p_len = p.len();
                    total_effect += (p.clone() * X.column(idx)).iter().sum::<f64>() / (p_len as f64);
                }
            }
            ame[idx] = total_effect / (thresholds.len() as f64);
            jacobian[[idx, idx]] = ame[idx];
        } else {
            let mut total_effect = 0.0;
            for t in thresholds.iter() {
                if is_logit {
                    let z = *t - &xb;
                    let exp_neg_z = (-z).mapv(|v| v.exp());
                    let p = 1.0 / (1.0 + exp_neg_z);
                    let p_len = p.len();
                    total_effect += (p.clone() * X.column(idx)).iter().sum::<f64>() / (p_len as f64);
                } else {
                    let z = *t - &xb;
                    let p = z.mapv(|v| normal.cdf(v));
                    let p_len = p.len();
                    total_effect += (p.clone() * X.column(idx)).iter().sum::<f64>() / (p_len as f64);
                }
            }
            ame[idx] = total_effect / (thresholds.len() as f64);
            jacobian[[idx, idx]] = ame[idx];
        }
    }
    let cov_ame = jacobian.dot(cov_beta).dot(&jacobian.t());
    let se = cov_ame.diag().mapv(|v| v.sqrt());
    Ok((ame, se))
}

/// Compute marginal effects for multinomial models.
fn compute_multinomial_margins(
    beta: &Array2<f64>,
    X: &Array2<f64>,
    cov_beta: &Array2<f64>,
    var_types: &[VariableType],
) -> Result<(Array1<f64>, Array1<f64>), AnalysisError> {
    let n_classes = beta.shape()[0];
    let n_features = beta.shape()[1];
    let mut ame = Array1::zeros(n_features);
    let mut jacobian = Array2::zeros((n_features, n_features));

    let logits = X.dot(&beta.t());
    let max_logits = logits.map_axis(Axis(1), |row| {
        row.iter().cloned().fold(f64::NEG_INFINITY, f64::max)
    });
    let stable_logits = &logits - &max_logits.insert_axis(Axis(1));
    let exp_logits = stable_logits.mapv(|v| v.exp());
    let _sum_exp = exp_logits.sum_axis(Axis(1)); // unused

    for (idx, &vtype) in var_types.iter().enumerate() {
        if vtype == VariableType::Discrete {
            let mut X_plus = X.to_owned();
            X_plus.column_mut(idx).fill(1.0);
            let mut X_minus = X.to_owned();
            X_minus.column_mut(idx).fill(0.0);

            let logits_plus = X_plus.dot(&beta.t());
            let logits_minus = X_minus.dot(&beta.t());

            let max_plus = logits_plus.map_axis(Axis(1), |row| {
                row.iter().cloned().fold(f64::NEG_INFINITY, f64::max)
            });
            let max_minus = logits_minus.map_axis(Axis(1), |row| {
                row.iter().cloned().fold(f64::NEG_INFINITY, f64::max)
            });

            let stable_plus = &logits_plus - &max_plus.insert_axis(Axis(1));
            let stable_minus = &logits_minus - &max_minus.insert_axis(Axis(1));

            let exp_plus = stable_plus.mapv(|v| v.exp());
            let exp_minus = stable_minus.mapv(|v| v.exp());

            let sum_plus = exp_plus.sum_axis(Axis(1));
            let sum_minus = exp_minus.sum_axis(Axis(1));

            let probs_plus = exp_plus / sum_plus.insert_axis(Axis(1));
            let probs_minus = exp_minus / sum_minus.insert_axis(Axis(1));

            let n = probs_plus.len();
            let effect = (probs_plus - probs_minus).sum() / (n as f64);
            ame[idx] = effect;
            jacobian[[idx, idx]] = effect;
        } else {
            let mut effect_sum = 0.0;
            for i in 0..X.nrows() {
                let row = X.row(i);
                let logits_i = row.dot(&beta.t());
                let max_logit = logits_i.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
                let stable_logits = logits_i - max_logit;
                let exp_logits = stable_logits.mapv(|v| v.exp());
                let sum_exp = exp_logits.sum();
                let probs_i = exp_logits.mapv(|v| v / sum_exp);
                let weighted_sum: f64 = (0..n_classes)
                    .map(|k| probs_i[k] * beta[[k, idx]])
                    .sum();
                let mut me_i = 0.0;
                for k in 0..n_classes {
                    me_i += probs_i[k] * (beta[[k, idx]] - weighted_sum);
                }
                effect_sum += me_i;
            }
            ame[idx] = effect_sum / (X.nrows() as f64);
            jacobian[[idx, idx]] = 1.0; // crude approximation
        }
    }

    let cov_ame = jacobian.dot(cov_beta).dot(&jacobian.t());
    let se = cov_ame.diag().mapv(|v| v.sqrt());
    Ok((ame, se))
}

fn remove_intercept(exog_names: &mut Vec<String>, X: &Array2<f64>) -> (Array2<f64>, Vec<String>) {
    if exog_names.first().map(|s| s == "Intercept").unwrap_or(false) {
        (X.slice(s![.., 1..]).to_owned(), exog_names[1..].to_vec())
    } else {
        (X.clone(), exog_names.clone())
    }
}

#[pyfunction]
fn ame(
    py: Python,
    model: &PyAny,
    _precise: Option<bool>, // unused parameter renamed to _precise
) -> PyResult<PyObject> {
    let mtype = detect_model_type(model)?;
    let (beta, cov_beta, mut exog_names, X) = extract_model_components(model)?;
    let var_types = detect_variable_types(&X);

    let (ame_vals, se_vals) = match mtype {
        ModelType::Logit | ModelType::Probit => {
            compute_binary_margins(&beta, &X, &cov_beta, &var_types, matches!(mtype, ModelType::Logit))?
        }
        ModelType::Poisson | ModelType::NegativeBinomial => {
            compute_count_margins(&beta, &X, &cov_beta, &var_types)?
        }
        ModelType::OrderedLogit | ModelType::OrderedProbit => {
            let (X_no_int, new_exog_names) = remove_intercept(&mut exog_names, &X);
            exog_names = new_exog_names;
            let thresholds = as_array1_f64(
                model.get_item("model")?
                    .get_item("distr")?
                    .get_item("thresholds")?
            )?.to_owned();
            compute_ordered_margins(&beta, &thresholds, &X_no_int, &cov_beta, &var_types, matches!(mtype, ModelType::OrderedLogit))?
        }
        ModelType::Multinomial => {
            let beta = as_array2_f64(model.get_item("params")?)?.to_owned();
            let cov_beta = cov_beta.to_owned();
            compute_multinomial_margins(&beta, &X, &cov_beta, &var_types)?
        }
        ModelType::Unknown => return Err(AnalysisError::ModelAttributeError("Unsupported model type".into()).into()),
    };

    let normal = Normal::new(0.0, 1.0).map_err(|_| AnalysisError::NumericalError)?;
    let z_scores: Vec<f64> = ame_vals.iter().zip(&se_vals).map(|(&a, &s)| a / s).collect();
    let p_values: Vec<f64> = z_scores.iter().map(|&z| 2.0 * (1.0 - normal.cdf(z.abs()))).collect();
    let stars: Vec<&str> = p_values.iter().map(|&p| add_significance_stars(p)).collect();

    let pd = py.import("pandas")?;
    let data = PyDict::new(py);
    data.set_item("dy/dx", ame_vals.to_vec())?;
    data.set_item("Std. Err", se_vals.to_vec())?;
    data.set_item("z", z_scores)?;
    data.set_item("Pr(>|z|)", p_values)?;
    data.set_item("Significance", stars)?;

    let kwargs = PyDict::new(py);
    kwargs.set_item("data", data)?;
    kwargs.set_item("index", exog_names)?;

    let df = pd.call_method("DataFrame", (), Some(kwargs))?;
    Ok(df.to_object(py))
}

#[pymodule]
fn febolt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ame, m)?)?;
    Ok(())
}
