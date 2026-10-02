\# Automated Data Quality \& Validation System



An end-to-end Python-based data quality pipeline that automatically profiles, cleans, validates, and analyzes datasets before they are used for further analysis or machine learning.



\## Project Overview



The system works as a backend "data gatekeeper".



It takes a raw CSV dataset as input and performs:



1\. Data profiling

2\. Data cleaning and transformation

3\. AI-based validation and anomaly detection

4\. End-to-end pipeline orchestration



The system generates cleaned data and detailed data-quality reports.



\## Pipeline Architecture



Raw CSV Dataset

&#x20;      |

&#x20;      v

+-------------------+

|  Data Profiling   |

|     Module 1      |

+---------+---------+

&#x20;         |

&#x20;         v

+-------------------+

| Data Cleaning \&   |

| Transformation    |

|     Module 2      |

+---------+---------+

&#x20;         |

&#x20;         v

+-------------------+

| AI Validation \&   |

| Anomaly Detection |

|     Module 3      |

+---------+---------+

&#x20;         |

&#x20;         v

+-------------------+

| Integration \&     |

| Orchestration     |

|     Module 4      |

+---------+---------+

&#x20;         |

&#x20;         v

&#x20;  Quality Reports

&#x20;  + Cleaned Data



\## Modules



\### Module 1 — Data Profiling \& Metadata Intelligence



The profiling module analyzes the input dataset and identifies:



\- Dataset metadata

\- Column data types

\- Semantic meaning of columns

\- Missing values

\- Unique values and cardinality

\- Mixed-type columns

\- Type consistency

\- Format consistency

\- Suspicious columns

\- Potential PII

\- Numeric distributions

\- Correlations

\- Outliers



Output:



profiling\_report.json



Visualizations include:



\- Missing-value heatmap

\- Correlation heatmap

\- Numeric distributions

\- Outlier visualizations



\### Module 2 — Data Cleaning \& Transformation



The cleaning module prepares the dataset for downstream processing.



It includes:



\- Schema inference

\- Missing-value handling

\- Statistical imputation

\- KNN/regression/iterative imputation support

\- Duplicate detection

\- Fuzzy duplicate matching

\- String normalization

\- Numeric normalization

\- Date normalization

\- Categorical normalization

\- Data transformation

\- Data-quality scoring



Outputs:



cleaned\_data.csv

cleaning\_log.json



\### Module 3 — AI Validation \& Anomaly Detection



The validation module checks the cleaned dataset for potential quality problems.



It includes:



\- Email validation

\- Phone validation

\- Postcode validation

\- Numeric range validation

\- Categorical consistency checks

\- Isolation Forest anomaly detection

\- Local Outlier Factor (LOF)

\- Autoencoder-based anomaly detection

\- Suspicious pattern detection

\- Data drift checks

\- Column semantic classification

\- Severity scoring

\- Overall data health scoring

\- Model evaluation



Output:



validation\_report.json



\### Module 4 — Integration \& Production Engineering



The final module combines all previous modules into one end-to-end pipeline.



It includes:



\- Pipeline orchestration

\- YAML configuration

\- Command-line execution

\- Logging

\- Git version control

\- DVC dataset versioning

\- Docker containerization

\- Automated testing

\- Production-oriented documentation



The complete pipeline can be executed using:



python pipeline.py --input data/retail\_store\_sales.csv --output results/



\## Technologies Used



\- Python

\- Pandas

\- NumPy

\- Scikit-learn

\- RapidFuzz

\- PyYAML

\- Matplotlib

\- Seaborn

\- Pytest

\- Docker

\- Git

\- DVC



\## Dataset



The project uses a retail sales dataset containing intentionally dirty data for demonstrating data profiling, cleaning, validation, and anomaly detection.



Input dataset:



data/retail\_store\_sales.csv



The raw dataset is tracked using DVC.



\## Project Structure



automated-data-quality-system/

|

├── api/

│   ├── cleaning\_api.py

│   ├── profiling\_api.py

│   └── validation\_api.py

|

├── config/

│   └── pipeline\_config.yaml

|

├── data/

│   ├── .gitignore

│   └── retail\_store\_sales.csv.dvc

|

├── docs/

│   ├── module4\_documentation.txt

│   └── profiling\_report\_schema.json

|

├── notebooks/

│   └── 01\_data\_profiling.ipynb

|

├── src/

│   ├── anomaly\_detection.py

│   ├── cleaning.py

│   ├── column\_classifier.py

│   ├── data\_drift.py

│   ├── duplicate\_detection.py

│   ├── imputation.py

│   ├── logger.py

│   ├── model\_evaluation.py

│   ├── normalization.py

│   ├── profiling.py

│   ├── quality\_scoring.py

│   ├── schema\_inference.py

│   ├── severity\_scoring.py

│   ├── suspicious\_patterns.py

│   ├── transformation.py

│   ├── validation.py

│   ├── validation\_pipeline.py

│   └── validation\_rules.py

|

├── tests/

│   ├── test\_cleaning.py

│   ├── test\_pipeline.py

│   ├── test\_validation.py

│   └── test\_validation\_pipeline.py

|

├── visualizations/

|

├── .gitignore

├── .dvcignore

├── Dockerfile

├── pipeline.py

└── requirements.txt



\## Installation



Clone the repository:



git clone https://github.com/Keeru7/automated-data-quality-system.git



Move into the project directory:



cd automated-data-quality-system



Install the required Python packages:



pip install -r requirements.txt



\## Running the Pipeline



Run the complete pipeline:



python pipeline.py --input data/retail\_store\_sales.csv --output results/



The pipeline executes:



Step 1 → Data Profiling

Step 2 → Data Cleaning

Step 3 → Data Validation



\## Generated Outputs



After successful execution:



results/

├── profiling\_report.json

├── cleaned\_data.csv

├── cleaning\_log.json

├── validation\_report.json

└── pipeline.log



\### profiling\_report.json



Contains information about:



\- Dataset structure

\- Column types

\- Missing values

\- Cardinality

\- Semantic meaning

\- Format consistency

\- Suspicious columns

\- Potential PII



\### cleaned\_data.csv



Contains the processed dataset after cleaning and transformation.



\### cleaning\_log.json



Records cleaning operations such as:



\- Missing-value handling

\- Duplicate detection

\- Normalization

\- Transformations

\- Quality-score changes



\### validation\_report.json



Contains validation and anomaly-detection results including:



\- Validation errors

\- Anomalies

\- Suspicious patterns

\- Data drift

\- Severity

\- Data health information



\### pipeline.log



Contains execution logs for the complete pipeline.



\## Running Tests



The project uses Pytest.



Run:



pytest tests -v



Latest project verification:



18 tests passed

1 warning



The warning was a scikit-learn convergence warning and did not cause a test failure.



\## Docker



Build the Docker image:



docker build -t automated-data-quality-system .



Run the pipeline:



docker run --rm automated-data-quality-system



To save generated results to the local project:



docker run --rm -v "%cd%\\results:/app/results" automated-data-quality-system



\## Data Versioning



DVC is used to track the raw dataset separately from the source code.



Dataset tracking file:



data/retail\_store\_sales.csv.dvc



Check DVC status:



dvc status



\## Configuration



Pipeline configuration is stored in:



config/pipeline\_config.yaml



The configuration controls:



\- Input dataset

\- Output directory

\- Profiling

\- Cleaning

\- Validation

\- Imputation method

\- Logging level

\- Log file



\## Key Features



\- Automated data profiling

\- Data cleaning and transformation

\- Missing-value handling

\- Duplicate detection

\- Fuzzy matching

\- Rule-based validation

\- AI/ML anomaly detection

\- Data drift detection

\- Data-quality scoring

\- CLI execution

\- YAML configuration

\- Logging

\- Docker support

\- DVC dataset versioning

\- Automated testing



\## Project Result



The completed system provides an automated data-quality pipeline that takes a raw dataset and produces:



Raw Dataset

&#x20;    ↓

Profiling

&#x20;    ↓

Cleaning

&#x20;    ↓

AI Validation

&#x20;    ↓

Quality Reports

&#x20;    ↓

Cleaned Dataset



The pipeline was tested end-to-end using Python, Docker, and Pytest.



\## Author



Keerthana Martha



B.Tech Information Technology — 2026



GitHub: https://github.com/Keeru7

