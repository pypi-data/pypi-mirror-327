pub mod utils;

use std::collections::HashMap;
use pyo3::{exceptions::PyException, prelude::{pyfunction, pymodule, wrap_pyfunction, Bound, PyModule, PyModuleMethods as _, PyResult}};

pub use utils::{file_to_xlsx as parq_file_to_xlsx, folder_to_xlsx as parq_folder_to_xlsx};


#[pyfunction]
#[pyo3(signature = (source, destination, sheet_name=None, sheet_column=None, header_labels=HashMap::new()))]
fn parquet_file_to_xlsx(source: String, destination: String, sheet_name: Option<String>, sheet_column: Option<String>, header_labels: HashMap<String, String>) -> PyResult<()> {
    match parq_file_to_xlsx(source, destination, sheet_name, sheet_column, header_labels) {
        Ok(_) => {
            Ok(())
        },
        Err(e) => {
            Err(PyException::new_err(e.to_string()))
        }
    }
}


#[pyfunction]
#[pyo3(signature = (source, destination, sheet_name=None, sheet_column=None, header_labels=HashMap::new()))]
fn parquet_files_to_xlsx(source: String, destination: String, sheet_name: Option<String>, sheet_column: Option<String>, header_labels: HashMap<String, String>) -> PyResult<()> {
    match parq_folder_to_xlsx(source, destination, sheet_name, sheet_column, header_labels) {
        Ok(_) => {
            Ok(())
        },
        Err(e) => {
            Err(PyException::new_err(e.to_string()))
        }
    }
}




/// A Python module implemented in Rust.
#[pymodule]
fn parquet_to_excel(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parquet_file_to_xlsx, m)?)?;
    m.add_function(wrap_pyfunction!(parquet_files_to_xlsx, m)?)?;
    Ok(())
}
