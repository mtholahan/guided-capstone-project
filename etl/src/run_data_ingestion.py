# Simulated Step 2–3 Spark job
import time, random
print("[run_data_ingestion] Starting simulated ingestion job...")
time.sleep(2)
if random.choice([True, True, True, False]):  # mostly succeed
    print("[run_data_ingestion] ✅ Completed successfully.")
else:
    raise RuntimeError("Simulated failure in data ingestion.")
