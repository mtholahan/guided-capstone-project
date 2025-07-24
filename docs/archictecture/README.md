- ## 📊 Equity Market Data Pipeline – Capstone Part 1

  This diagram visualizes the architecture of a scalable data pipeline designed to ingest, validate, and process equity market data — specifically daily trade and quote data — using Azure cloud services and the medallion architecture pattern (Bronze → Silver → Gold).

  ### 🔧 Pipeline Stages

  **1. Raw Input (Top Lane)**

  - Azure Data Factory orchestrates ingestion of source files (CSV and JSON), Spark-based processing, validation logic, and downstream ETL operations.
  - Elastic cloud compute (e.g., Azure Databricks or HDInsight) ensures scalability to billions of records.

  **2. Processing & Orchestration (Middle Lane)**

  - Raw data is first written to the **Bronze Table**, then cleaned, validated, and joined into the **Silver Table**.
  - Records that fail schema validation are dropped from the pipeline but logged to a **Staging Blob** for observability.
  - Validated records are loaded into partitioned **Daily Trade** and **Daily Quote** tables, then enriched and curated into a **Gold Table**.

  **3. Storage & Output (Bottom Lane)**

  - A daily ETL job outputs an **Analytics Copy** of curated data for reporting.
  - The final **Quote-Trade Analytical** table is persisted to an analytical store for Power BI dashboards and ad hoc analysis.

  ### 🧱 Key Architecture Patterns

  - **Medallion Tables:** Follows the Bronze/Silver/Gold Lakehouse architecture.
  - **Partitioning Strategy:** Daily partitioned tables optimize performance for high-frequency queries.
  - **Observability:** Schema rejections are tracked in the staging layer for debugging and QA.
  - **Cloud-Native Scalability:** Built on Azure Data Factory + Spark on elastic compute.