#!/bin/bash
# === Preprocess ETL Orchestration ===

JOB="preprocess_etl"
echo "[$(date)] Starting $JOB..."

# Run Spark ETL job
spark-submit --master local[*] etl/src/run_data_ingestion.py config/config.ini
STATUS=$?

if [ $STATUS -eq 0 ]; then
  echo "[$(date)] $JOB completed successfully."
  python etl/src/tracker.py --job $JOB --status success
else
  echo "[$(date)] $JOB failed!"
  python etl/src/tracker.py --job $JOB --status failed
  exit 1
fi
