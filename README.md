# OpenSea ETL Pipeline

This project implements an **ETL (Extract, Transform, Load)** pipeline to fetch, process, and store Ethereum-based collections data from the OpenSea API. The pipeline extracts data from the OpenSea Collections API, transforms it into a structured format, and loads it into a SQLite database.

---

## Features

- **Data Extraction**: Fetches Ethereum-based collections data from the OpenSea API.
- **Data Transformation**: Cleans and structures the raw data for storage.
- **Data Loading**: Stores the transformed data in a SQLite database.
- **Environment Variables**: Uses `.env` for secure API key management.
- **Data Lake**: Saves raw data in JSON format for backup and analysis.

---

## Prerequisites

Before running the pipeline, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ganjela/data-engineer-step-2.git
   cd data-engineer-step-2
2. **Install dependencies**:
   ```
   pip install -r requirements.txt
3. **Run main.py to see how it works**
   ```
   python3 main.py
