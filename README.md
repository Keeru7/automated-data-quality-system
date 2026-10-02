# Automated Data Quality & Validation System

An end-to-end Python-based data quality pipeline that automatically **profiles, cleans, validates, and analyzes datasets** before they are used for further analysis or machine learning.

The system acts as a backend **"data gatekeeper"**, helping identify data-quality issues and producing cleaned datasets and detailed validation reports.

---

## 🚀 Project Overview

The system processes a raw CSV dataset through four major stages:

```text
Raw CSV Dataset
       │
       ▼
┌─────────────────────────┐
│  Module 1               │
│  Data Profiling         │
│  & Metadata Intelligence│
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Module 2               │
│  Data Cleaning          │
│  & Transformation       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Module 3               │
│  AI Validation          │
│  & Anomaly Detection    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Module 4               │
│  Integration            │
│  & Production Engineering│
└────────────┬────────────┘
             │
             ▼
   Quality Reports
   + Cleaned Dataset
✨ Project Highlights
Automated data profiling
Missing-value analysis
Schema inference
Statistical and ML-based imputation
Duplicate and fuzzy duplicate detection
Data normalization and transformation
Rule-based data validation
AI/ML anomaly detection
Data drift detection
Column semantic classification
Data-quality and health scoring
CLI-based pipeline execution
YAML configuration
Logging and error handling
Docker containerization
DVC dataset versioning
Automated testing with Pytest
📌 Modules
Module 1 — Data Profiling & Metadata Intelligence

The profiling module analyzes the input dataset and identifies:

Dataset metadata
Column data types
Semantic meaning of columns
Missing values
Unique values and cardinality
Mixed-type columns
Type consistency
Format consistency
Suspicious columns
Potential PII
Numeric distributions
Correlations
Outliers
Output
profiling_report.json
Visualizations
Missing-value heatmap
Correlation heatmap
Numeric distributions
Outlier visualizations
Module 2 — Data Cleaning & Transformation

The cleaning module prepares the dataset for downstream processing.

It includes:

Schema inference
Missing-value handling
Statistical imputation
KNN imputation
Regression imputation
Iterative imputation support
Duplicate detection
Fuzzy duplicate matching
String normalization
Numeric normalization
Date normalization
Categorical normalization
Data transformation
Data-quality scoring
Outputs
cleaned_data.csv
cleaning_log.json
Module 3 — AI Validation & Anomaly Detection

The validation module checks the cleaned dataset for potential quality problems.

Rule-Based Validation
Email validation
Phone validation
Postcode validation
Numeric range validation
Categorical consistency checks
AI/ML Validation
Isolation Forest
Local Outlier Factor (LOF)
Autoencoder-based anomaly detection
Suspicious pattern detection
Data drift detection
Column semantic classification
Severity scoring
Overall data health scoring
Model evaluation
Output
validation_report.json
Module 4 — Integration & Production Engineering

The final module integrates all previous modules into a single end-to-end pipeline.

It includes:

Pipeline orchestration
YAML configuration
Command-line execution
Logging
Git version control
DVC dataset versioning
Docker containerization
Automated testing
Production-oriented documentation
Run the complete pipeline
python pipeline.py --input data/retail_store_sales.csv --output results/
🛠️ Technologies Used
Technology	Purpose
Python	Core development
Pandas	Data processing
NumPy	Numerical operations
Scikit-learn	Machine learning and anomaly detection
RapidFuzz	Fuzzy duplicate matching
PyYAML	Pipeline configuration
Matplotlib	Data visualization
Seaborn	Statistical visualization
Pytest	Automated testing
Docker	Containerization
Git	Version control
DVC	Dataset versioning
📊 Dataset

The project uses a retail sales dataset containing intentionally dirty data for demonstrating:

Data profiling
Data cleaning
Data validation
Anomaly detection
Data-quality analysis
Input Dataset
data/retail_store_sales.csv

The raw dataset is tracked using DVC.

📁 Project Structure
automated-data-quality-system/
│
├── api/
│   ├── cleaning_api.py
│   ├── profiling_api.py
│   └── validation_api.py
│
├── config/
│   └── pipeline_config.yaml
│
├── data/
│   ├── .gitignore
│   └── retail_store_sales.csv.dvc
│
├── docs/
│   ├── module4_documentation.txt
│   └── profiling_report_schema.json
│
├── notebooks/
│   └── 01_data_profiling.ipynb
│
├── src/
│   ├── anomaly_detection.py
│   ├── cleaning.py
│   ├── column_classifier.py
│   ├── data_drift.py
│   ├── duplicate_detection.py
│   ├── imputation.py
│   ├── logger.py
│   ├── model_evaluation.py
│   ├── normalization.py
│   ├── profiling.py
│   ├── quality_scoring.py
│   ├── schema_inference.py
│   ├── severity_scoring.py
│   ├── suspicious_patterns.py
│   ├── transformation.py
│   ├── validation.py
│   ├── validation_pipeline.py
│   └── validation_rules.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_pipeline.py
│   ├── test_validation.py
│   └── test_validation_pipeline.py
│
├── visualizations/
│
├── .gitignore
├── .dvcignore
├── Dockerfile
├── pipeline.py
├── requirements.txt
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/Keeru7/automated-data-quality-system.git
2. Move into the project directory
cd automated-data-quality-system
3. Install dependencies
pip install -r requirements.txt
▶️ Running the Pipeline

Run the complete pipeline using:

python pipeline.py --input data/retail_store_sales.csv --output results/

The pipeline executes:

Step 1 → Data Profiling
Step 2 → Data Cleaning
Step 3 → Data Validation

After successful execution, the generated files are stored inside the results/ directory.

📄 Generated Outputs
results/
│
├── profiling_report.json
├── cleaned_data.csv
├── cleaning_log.json
├── validation_report.json
└── pipeline.log
profiling_report.json

Contains:

Dataset structure
Column types
Missing values
Cardinality
Semantic meaning
Format consistency
Suspicious columns
Potential PII
cleaned_data.csv

Contains the processed dataset after the cleaning and transformation stages.

cleaning_log.json

Records cleaning operations including:

Missing-value handling
Duplicate detection
Normalization
Transformations
Quality-score changes
validation_report.json

Contains:

Validation errors
Detected anomalies
Suspicious patterns
Data drift information
Severity information
Data health information
pipeline.log

Contains execution logs for the complete pipeline.

🧪 Testing

The project uses Pytest for automated testing.

Run:

pytest tests -v
Latest verification
18 tests passed
1 warning

The warning was a scikit-learn convergence warning and did not cause a test failure.

🐳 Docker

The project supports containerized execution using Docker.

Build the Docker image
docker build -t automated-data-quality-system .
Run the pipeline
docker run --rm automated-data-quality-system
Save generated results to the local project

On Windows:

docker run --rm -v "%cd%\results:/app/results" automated-data-quality-system

This allows the generated reports and cleaned dataset to remain available in the local results/ folder.

🔄 Data Versioning with DVC

DVC is used to track the raw dataset separately from the source code.

Dataset tracking file:

data/retail_store_sales.csv.dvc

Check DVC status:

dvc status
⚙️ Configuration

Pipeline configuration is stored in:

config/pipeline_config.yaml

The configuration controls:

Input dataset
Output directory
Profiling
Cleaning
Validation
Imputation method
Logging level
Log file

This allows pipeline behavior to be changed without modifying the main pipeline code.

🔗 Pipeline Execution Flow
Raw Dataset
     │
     ▼
Data Profiling
     │
     ▼
Data Cleaning
     │
     ▼
AI Validation
     │
     ▼
Quality Analysis
     │
     ├──────────────► profiling_report.json
     │
     ├──────────────► cleaning_log.json
     │
     ├──────────────► validation_report.json
     │
     ├──────────────► cleaned_data.csv
     │
     └──────────────► pipeline.log
📈 Project Result

The completed system provides an automated backend data-quality pipeline that takes a raw dataset and processes it through:

Raw Dataset
     ↓
Profiling
     ↓
Cleaning
     ↓
AI Validation
     ↓
Quality Analysis
     ↓
Reports + Cleaned Dataset

The complete pipeline has been verified using:

Python
Docker
DVC
Git
Pytest

The latest test execution completed with:

18 tests passed
👩‍💻 Author

Keerthana Martha

B.Tech Information Technology — 2026

GitHub: https://github.com/Keeru7

📌 Repository

GitHub Repository:

https://github.com/Keeru7/automated-data-quality-system
