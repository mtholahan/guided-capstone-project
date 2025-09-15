# Guided Capstone Project


## 📖 Abstract
This guided capstone focuses on designing and implementing an end-to-end data pipeline to process and analyze high-frequency equity market data. The simulated client, Spring Capital, is an investment bank that depends on real-time analytics for trade and quote data across multiple exchanges. The engineering goal is to create a scalable platform that ingests raw trade and quote records, applies daily ETL processes, and generates key financial indicators to support decision-making.

The pipeline design spans multiple stages:

* Schema design: normalized trade and quote tables with composite keys for efficient querying.

* Data ingestion: parsing semi-structured daily exchange files (CSV and JSON) to extract valid records and discard malformed ones.

* Batch load: an end-of-day process that consolidates daily submissions, resolves late-arriving corrections, and ensures only the most current records persist.

* Analytical ETL: deriving business-critical metrics, including latest trade price, rolling 30-minute average, and bid/ask price movements relative to prior day close.

* Orchestration: scheduling jobs with retry logic and status tracking to guarantee operational reliability.

By the end of the project, the platform demonstrates scalable, fault-tolerant data engineering practices, combining database design, PySpark data ingestion, and workflow orchestration. This project bridges foundational design skills with applied big data engineering in a realistic financial services context.























*Generated automatically via Python + Jinja2 + SQL Server table `tblMiniProjectProgress` on 09-14-2025 23:37:22*