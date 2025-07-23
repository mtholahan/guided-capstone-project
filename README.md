# 📈 Equity Market Data Analysis (Springboard Guided Capstone)

✅ 1. Prerequisites

## 🧩 Prerequisites

- Azure subscription with access to Databricks, ADLS Gen2, (OPTIONAL: Event Hubs and ADF)
- Databricks CLI and/or Databricks Connect installed
- Python 3.8+ (for local dev/testing)
- VS Code with Python and Azure extensions
- GitHub account and repo access
- 
✅ 2. Getting Started / Quick Start

## 🚀 Getting Started

### 1. Clone repo
```bash
git clone https://github.com/mtholahan/equity-market-data-analysis.git
cd equity-market-data-analysis
2. Install dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate     # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
3. Configure Azure credentials
Use az login to authenticate

Configure Databricks CLI (via databricks configure --token)

Set your storage account in notebook variables or via Azure Key Vault

---

### ✅ 3. **Project Workflow / Usage Guide**

```markdown
## 🧪 Workflow

1. Upload sample input files to `data/sample_input/`
2. Run `notebooks/01_ingest_data.py` to load data into ADLS raw zone
3. Execute `02_clean_transform.py` to clean and join datasets
4. Run `03_moving_averages.py` to compute and store window functions
5. Execute `04_kpi_summary.py` to generate gold-layer KPIs
You can run them in Databricks notebooks or trigger via CLI.

✅ 4. Deployment & Orchestration

## ⚙️ Deployment

- ADF/Synapse: `orchestrations/adf_pipeline.json` contains a scheduled pipeline with Databricks notebook activities
- Databricks CLI/REST: `scripts/trigger_databricks_job.sh` deploys and runs jobs

### Example:
```bash
bash scripts/trigger_databricks_job.sh

---

### ✅ 5. **Configuration**

```markdown
## 🛠 Configuration

Use environment variables or `conf/config.json`:

```json
{
  "storage_account": "<your-storage-account>",
  "raw_container": "raw",
  "silver_path": "silver/",
  "gold_path": "gold/"
}
Secure sensitive configs in Azure Key Vault or Databricks secrets.

---

### ✅ 6. **Testing & Validation**

```markdown
## 🔎 Testing & Validation

- Unit test data-cleansing functions in `notebooks/99_utils.py`
- Define schema validation (via Spark schemas or PyTest) for ingest pipelines
- Verify streaming correctness by adding sample files and observing outputs in `/outputs/logs`

✅ 7. CI/CD Integration

## 🤖 CI/CD (Optional)

- Set up GitHub Actions in `.github/workflows/ci.yml`
- Automate:
  - Linting via `flake8`
  - Unit testing via `pytest`
  - Deploying Databricks jobs using `databricks-cli`

✅ 8. Troubleshooting & Common Issues

## 🛠 Troubleshooting

### Mounting ADLS fails:
- Check service principal or account key permissions
- Use `dbutils.fs.mount()` with correct OAuth settings

### Databricks job errors:
- View notebook logs in workspace UI under `Jobs -> Run history`
- Validate cluster runtime + installed libraries

### Streaming checkpoint issues:
- Locate `_checkpoint` folder in logs and reset when needed

✅ 9. Contributing & Contact

## 🤝 Contributing

Feel free to submit PRs. For major changes, please open an issue first.

## 📫 Contact

Mark – [markholahan@proton.me] or GitHub discussions/issues

✅ 10. Licensing & Acknowledgements
MIT License
