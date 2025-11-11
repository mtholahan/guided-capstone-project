"""
tracker.py – Guided Capstone Step 5
Tracks job execution status in a PostgreSQL table.
Implements assign_job_id, update_job_status, and get_job_status methods.
"""

import psycopg2
import datetime
import configparser
import argparse
from psycopg2 import sql

class Tracker:
    def __init__(self, jobname: str, cfg: configparser.ConfigParser):
        self.jobname = jobname
        self.cfg = cfg
        self.table = cfg.get("postgres", "job_tracker_table_name")

    def _conn(self):
        """Establish database connection."""
        return psycopg2.connect(
            host=self.cfg.get("postgres", "host"),
            dbname=self.cfg.get("postgres", "database"),
            user=self.cfg.get("postgres", "user"),
            password=self.cfg.get("postgres", "password"),
            port=self.cfg.get("postgres", "port")
        )

    def assign_job_id(self):
        """Create unique job_id using convention jobname_YYYY-MM-DD"""
        return f"{self.jobname}_{datetime.date.today()}"

    def update_job_status(self, status: str):
        """Insert or update job status in job_tracker table."""
        job_id = self.assign_job_id()
        update_time = datetime.datetime.now()

        query = sql.SQL("""
            INSERT INTO {table} (job_id, status, updated_time)
            VALUES (%s, %s, %s)
            ON CONFLICT (job_id)
            DO UPDATE SET status = EXCLUDED.status,
                          updated_time = EXCLUDED.updated_time;
        """).format(table=sql.Identifier(self.table))

        try:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(query, (job_id, status, update_time))
                conn.commit()
            print(f"[Tracker] ✅ {job_id} → {status}")
        except Exception as e:
            print(f"[Tracker] ❌ Error updating status: {e}")

    def get_job_status(self, job_id: str):
        """Retrieve current status for a job_id."""
        query = sql.SQL("SELECT status, updated_time FROM {table} WHERE job_id = %s;") \
                    .format(table=sql.Identifier(self.table))
        try:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(query, (job_id,))
                record = cur.fetchone()
                if record:
                    print(f"[Tracker] Job {job_id}: status={record[0]}, updated={record[1]}")
                    return record
                else:
                    print(f"[Tracker] No record found for {job_id}")
                    return None
        except Exception as e:
            print(f"[Tracker] ❌ Error reading status: {e}")
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update job tracker status.")
    parser.add_argument("--job", required=True, help="Job name, e.g. preprocess_etl")
    parser.add_argument("--status", required=True, help="Job status: success, failed, blocked, etc.")
    args = parser.parse_args()

    cfg = configparser.ConfigParser()
    cfg.read("config/config.ini")

    tracker = Tracker(args.job, cfg)
    tracker.update_job_status(args.status)
