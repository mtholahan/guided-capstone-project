#!/bin/bash
# Analytical Workflow: runs only if preprocess succeeded
. ~/.bash_profile
JOB="analytical_etl"

PG_OK=$(psql -U postgres -d guided_capstone -t -A -c \
  "SELECT status FROM job_tracker WHERE job_id LIKE 'preprocess_etl_%';")

if [ "$PG_OK" = "success" ]; then
  echo "[$(date)] Launching $JOB..."
  spark-submit --master local[*] etl/src/run_reporter.py config/config.ini
  python3 etl/src/tracker.py --job $JOB --status success
  echo "[$(date)] $JOB completed successfully."
else
  echo "[$(date)] Preprocess job not successful. Aborting analytical run."
  python3 etl/src/tracker.py --job $JOB --status blocked
  exit 1
fi
