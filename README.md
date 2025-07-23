# 📈 Equity Market Data Analysis (Springboard Guided Capstone)

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#-1-prerequisites)
3. [Getting Started](#-2-getting-started--quick-start)
4. [Project Workflow](#-3-project-workflow--usage-guide)
5. [Deployment & Orchestration](#-4-deployment--orchestration)
6. [Configuration](#-5-configuration)
7. [Testing & Validation](#-6-testing--validation)
8. [CI/CD Integration](#-7-cicd-integration)
9. [Troubleshooting](#-8-troubleshooting--common-issues)
10. [Contributing & Contact](#-9-contributing--contact)
11. [License](#-10-licensing--acknowledgements)

## Project Overview

This project analyzes equity market trade and quote data using Apache Spark on Azure. It demonstrates a full-scale, cloud-native big data pipeline, including ingestion, transformation, moving averages, and gold-layer KPIs — with optional support for streaming via Event Hubs.



## ✅ 1. Prerequisites

- Azure subscription with access to Databricks, ADLS Gen2, (OPTIONAL: Event Hubs and ADF)
- Databricks CLI and/or Databricks Connect installed
- Python 3.8+ (for local dev/testing)
- VS Code with Python and Azure extensions
- GitHub account and repo access
  



## ✅ 2. Getting Started / Quick Start

### 1. Clone repo
```bash
git clone https://github.com/mtholahan/equity-market-data-analysis.git
cd equity-market-data-analysis
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate     # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### 📁 Git Ignore

Make sure your `.gitignore` file includes common patterns like:

- venv/
- __pycache__/
-  __*.log__/
-  __*.env__/
-  ***.db**/
-  .idea/
-  **.databricks**/

This prevents committing virtual environments, temp files, or IDE/project settings.

### 3. Configure Azure credentials

- Run `az login` to authenticate
- Configure Databricks CLI using `databricks configure --token`
- Set your storage account in notebook variables or via Azure Key Vault

### 4. Set up config file

Copy the provided config template and customize it with your environment details:

```bash
cp conf/config.template.json conf/config.json
```



## ✅ 3. **Project Workflow / Usage Guide**

1. Upload sample input files to `data/sample_input/`
2. Run `notebooks/01_ingest_data.py` to load data into ADLS raw zone
3. Execute `02_clean_transform.py` to clean and join datasets
4. Run `03_moving_averages.py` to compute and store window functions
5. Execute `04_kpi_summary.py` to generate gold-layer KPIs.
   You can run them in Databricks notebooks or trigger via CLI.



## ✅ 4. Deployment & Orchestration

- ADF: `orchestrations/adf_pipeline.json` contains a scheduled pipeline with Databricks notebook activities
- Databricks CLI/REST: `scripts/trigger_databricks_job.sh` deploys and runs jobs

### Example:
```bash
bash scripts/trigger_databricks_job.sh
```



---

## ✅ 5. **Configuration**

Use environment variables or `conf/config.json`:

```json
{
  "storage_account": "<your-storage-account>",
  "raw_container": "raw",
  "silver_path": "silver/",
  "gold_path": "gold/"
}
```

Secure sensitive configs in Azure Key Vault or Databricks secrets.

---

## ✅ 6. **Testing & Validation**

- Unit test data-cleansing functions in `notebooks/99_utils.py`
- Define schema validation (via Spark schemas or PyTest) for ingest pipelines
- Verify streaming correctness by adding sample files and observing outputs in `/outputs/logs`

### ✅ Running Tests

```bash
pytest tests/
```

---



## ✅ 7. CI/CD Integration

## 🤖 CI/CD (Optional)

- Set up GitHub Actions in `.github/workflows/ci.yml`
- Automate:
  - Linting via `flake8`
  - Unit testing via `pytest`
  - Deploying Databricks jobs using `databricks-cli`



## ✅ 8. Troubleshooting & Common Issues

### Mounting ADLS fails:
- Check service principal or account key permissions
- Use `dbutils.fs.mount()` with correct OAuth settings

### Databricks job errors:
- View notebook logs in workspace UI under `Jobs -> Run history`
- Validate cluster runtime + installed libraries

### Streaming checkpoint issues:
- Locate `_checkpoint` folder in logs and reset when needed



## ✅ 9. Contributing & Contact

## 🤝 Contributing

Feel free to submit PRs. For major changes, please open an issue first.

## 📫 Contact

Mark – [markholahan@proton.me] or GitHub discussions/issues



## ✅ 10. Licensing & Acknowledgements

MIT License
