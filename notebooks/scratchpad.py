# ============================================================
# Guided Capstone Step 2 – Data Ingestion (Databricks CE version)
# Refactored to add bad-record routing (partition=B) and safer parsing
# ============================================================

from pyspark.sql import SparkSession
import pyspark.sql.types as T
from pyspark.sql.functions import input_file_name, regexp_extract, current_timestamp, lit
import json
from datetime import datetime

spark = SparkSession.builder.appName("guided_step2_ingestion").getOrCreate()

# === 1. Common schema (expanded) ===
schema = T.StructType([
    T.StructField("trade_dt", T.StringType()),          # Both
    T.StructField("rec_type", T.StringType()),          # “T”, “Q”, or “B” (bad record)
    T.StructField("symbol", T.StringType()),            # present in both
    T.StructField("exchange", T.StringType()),          # present in both
    T.StructField("event_tm", T.StringType()),          # present in both
    T.StructField("event_seq_nb", T.IntegerType()),     # present in both
    T.StructField("arrival_tm", T.StringType()),        # derived from ingestion timestamp
    T.StructField("trade_pr", T.DoubleType()),          # Trade only
    T.StructField("trade_size", T.IntegerType()),       # Trade only
    T.StructField("bid_pr", T.DoubleType()),            # Quote only
    T.StructField("bid_size", T.IntegerType()),         # Quote only
    T.StructField("ask_pr", T.DoubleType()),            # Quote only
    T.StructField("ask_size", T.IntegerType()),         # Quote only
    T.StructField("execution_id", T.StringType()),      # Trade only, may be null
    T.StructField("partition", T.StringType())          # “T”, “Q”, or “B”
])

# === helper to build a bad-record row ===
def bad_record():
    return {
        "trade_dt": None,
        "rec_type": "B",
        "symbol": None,
        "exchange": None,
        "event_tm": None,
        "event_seq_nb": None,
        "arrival_tm": datetime.utcnow().isoformat(),
        "trade_pr": None,
        "trade_size": None,
        "bid_pr": None,
        "bid_size": None,
        "ask_pr": None,
        "ask_size": None,
        "execution_id": None,
        "partition": "B"
    }

# === 2. CSV parser (best-guess, position-based, tolerant) ===
def parse_csv(line: str):
    try:
        # keep empties to preserve positions
        vals = [v.strip() for v in line.split(",")]
        if len(vals) < 7:
            return bad_record()

        trade_dt   = vals[0] or None
        arrival_tm = vals[1] or None
        rec_type   = (vals[2] or "").upper()

        # your current files put symbol at 3, event_tm at 4, seq at 5, exchange at 6
        symbol        = vals[3] or None
        event_tm      = vals[4] or None
        event_seq_nb  = int(vals[5]) if vals[5] else None
        exchange      = vals[6] or None

        # now branch by record type
        if rec_type == "T":
            # we don’t appear to have execution_id or trade_size in the current CSV sample,
            # so we leave them null and focus on trade_pr
            trade_pr   = float(vals[7]) if len(vals) > 7 and vals[7] else None
            trade_size = int(vals[8]) if len(vals) > 8 and vals[8] else None
            return {
                "trade_dt": trade_dt,
                "rec_type": "T",
                "symbol": symbol,
                "exchange": exchange,
                "event_tm": event_tm,
                "event_seq_nb": event_seq_nb,
                "arrival_tm": arrival_tm or datetime.utcnow().isoformat(),
                "trade_pr": trade_pr,
                "trade_size": trade_size,
                "bid_pr": None,
                "bid_size": None,
                "ask_pr": None,
                "ask_size": None,
                "execution_id": None,
                "partition": "T"
            }

        elif rec_type == "Q":
            # your original mapping: 7..10 are quote fields
            bid_pr   = float(vals[7]) if len(vals) > 7 and vals[7] else None
            bid_size = int(vals[8])   if len(vals) > 8 and vals[8] else None
            ask_pr   = float(vals[9]) if len(vals) > 9 and vals[9] else None
            ask_size = int(vals[10])  if len(vals) > 10 and vals[10] else None
            return {
                "trade_dt": trade_dt,
                "rec_type": "Q",
                "symbol": symbol,
                "exchange": exchange,
                "event_tm": event_tm,
                "event_seq_nb": event_seq_nb,
                "arrival_tm": arrival_tm or datetime.utcnow().isoformat(),
                "trade_pr": None,
                "trade_size": None,
                "bid_pr": bid_pr,
                "bid_size": bid_size,
                "ask_pr": ask_pr,
                "ask_size": ask_size,
                "execution_id": None,
                "partition": "Q"
            }
        else:
            # unknown rec_type
            return bad_record()

    except Exception:
        return bad_record()

# === 3. JSON parser (normalized to common event) ===
def parse_json(line: str):
    try:
        rec = json.loads(line)
        rec_type = rec.get("event_type") or rec.get("rec_type") or "B"
        rec_type = rec_type.upper()

        trade_dt      = rec.get("trade_dt") or rec.get("trade_date")
        symbol        = rec.get("symbol")
        exchange      = rec.get("exchange")
        event_tm      = rec.get("event_tm")
        event_seq_nb  = rec.get("event_seq_nb")
        arrival_tm    = rec.get("file_tm") or datetime.utcnow().isoformat()

        base = {
            "trade_dt": trade_dt,
            "rec_type": rec_type,
            "symbol": symbol,
            "exchange": exchange,
            "event_tm": event_tm,
            "event_seq_nb": int(event_seq_nb) if event_seq_nb is not None else None,
            "arrival_tm": arrival_tm,
            "trade_pr": None,
            "trade_size": None,
            "bid_pr": None,
            "bid_size": None,
            "ask_pr": None,
            "ask_size": None,
            "execution_id": rec.get("execution_id"),
            "partition": rec_type if rec_type in ("T", "Q") else "B"
        }

        if rec_type == "T":
            base["trade_pr"] = float(rec.get("trade_pr")) if rec.get("trade_pr") is not None else None
            base["trade_size"] = int(rec.get("trade_size")) if rec.get("trade_size") is not None else None
        elif rec_type == "Q":
            base["bid_pr"]   = float(rec.get("bid_pr")) if rec.get("bid_pr") is not None else None
            base["bid_size"] = int(rec.get("bid_size")) if rec.get("bid_size") is not None else None
            base["ask_pr"]   = float(rec.get("ask_pr")) if rec.get("ask_pr") is not None else None
            base["ask_size"] = int(rec.get("ask_size")) if rec.get("ask_size") is not None else None

        return base

    except Exception:
        return bad_record()

# === 4. Paths ===
base_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/data"
csv_path = f"{base_path}/csv/*/*/*.txt"
json_path = f"{base_path}/json/*/*/*.txt"
output_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/output_dir/"

# === 5. Load, parse, DF-ify ===
csv_rdd = spark.sparkContext.textFile(csv_path).map(parse_csv).filter(lambda r: r is not None)
json_rdd = spark.sparkContext.textFile(json_path).map(parse_json).filter(lambda r: r is not None)

csv_df = spark.createDataFrame(csv_rdd, schema=schema)
json_df = spark.createDataFrame(json_rdd, schema=schema)

combined_df = csv_df.unionByName(json_df, allowMissingColumns=True)

# === 6. Audit columns ===
combined_df = combined_df.withColumn("source_path", input_file_name())
combined_df = combined_df.withColumn("source_file", regexp_extract("source_path", r"([^/]+)$", 1))
combined_df = combined_df.withColumn("ingest_ts", current_timestamp())

# === 7. Write partitioned ===
combined_count = combined_df.count()
print("Combined Count:", combined_count)

if combined_count > 0:
    combined_df.groupBy("partition").count().show()
    combined_df.write.partitionBy("partition").mode("overwrite").parquet(output_path)
    print(f"✅ Data written successfully to: {output_path}")
else:
    print("⚠️ No data to write – check parser output.")

combined_df.printSchema()
