# Healthcare Claims Analytics Pipeline

End-to-end data engineering project analyzing healthcare insurance claims using AWS Glue, PySpark, and Athena.

## Project Overview

**Domain:** Healthcare Insurance (Cigna/HCSC use case)  
**Data Volume:** 11,210 rows across 4 normalized tables  
**Architecture:** Medallion (Bronze → Silver → Gold)  
**Tech Stack:** AWS S3, Glue, PySpark, Athena, Python

## Business Problem

Insurance companies process millions of claims annually and need to:
- Identify high-cost claims for case management
- Detect fraud patterns
- Optimize provider networks
- Stratify patient risk for interventions

## Architecture
```
Bronze Layer (S3)          Silver Layer (S3)              Gold Layer (S3)
Raw CSV Data      →     Enriched Parquet Data    →    Analytics Tables
----------------        ---------------------        ------------------
- claims.csv            • Claims + Patients          • High-cost claims
- patients.csv          • + Providers                • Provider performance
- providers.csv         • + ICD codes                • Fraud indicators
- icd_codes.csv         • + Calculated fields        • Diagnosis analysis
                                                      • Regional metrics
                                                      • Patient risk scores
```

## Data Model

**Star Schema:**
- **Fact Table:** Claims (10,000 rows)
- **Dimensions:** Patients (1,000), Providers (200), ICD Codes (10)

**Key Metrics:**
- Total Claims: 10,000
- Total Cost: $188.4M
- Approval Rate: 85.3%
- Avg Cost per Patient: $188,351

## Key Insights

### 1. High-Cost Claims
- Top 1% of claims = $100K+ (all breast cancer treatment)
- 229 claims flagged as high fraud risk
- OUT_OF_NETWORK claims 15-20% more expensive

### 2. Provider Performance
- 200 providers analyzed
- Denial rates: 4-20% (South Kurt Medical Center = 19.7% red flag)
- High-volume providers process 60+ claims

### 3. Patient Risk
- 646 patients (64.6%) classified as High or Critical risk
- Critical patients average 16-18 claims, $311K-$478K lifetime cost
- All critical patients age 73-85 with chronic conditions

### 4. Cost Analysis
- Breast Cancer (C50.9): $88.9M total (most expensive)
- Cholesterol (E78.5): $794K total (cheapest)
- Approval rates consistent: 83-87% across all diagnoses

## Technologies Used

**AWS Services:**
- S3 (Data Lake)
- Glue (ETL, Data Catalog, Interactive Sessions)
- Athena (SQL Analytics)
- IAM (Security)

**Languages & Tools:**
- Python 3.12 (Faker, Boto3)
- PySpark (Glue 4.0)
- SQL (Athena queries)
- Jupyter Notebooks

## Project Structure
```
healthcare-claims-pipeline/
├── data-generator/
│   ├── generate_healthcare_data.py    # Synthetic data generation
│   └── upload_to_s3.py                # S3 upload script
├── data/
│   ├── claims.csv
│   ├── patients.csv
│   ├── providers.csv
│   └── icd_codes.csv
├── notebooks/
│   └── healthcare_bronze_to_gold.ipynb  # PySpark transformations
└── README.md
```

## How to Run

### Prerequisites
- AWS Account (us-east-1 region)
- AWS CLI configured
- Python 3.12+
- Jupyter with AWS Glue Sessions

### Step 1: Generate Data
```bash
cd data-generator
python3 generate_healthcare_data.py
```

### Step 2: Upload to S3
```bash
python3 upload_to_s3.py
```

### Step 3: Run Glue Crawler
- Create crawler pointing to `s3://bucket/healthcare/bronze/`
- Run crawler to catalog Bronze tables

### Step 4: PySpark Transformations
```bash
cd ../notebooks
jupyter notebook
# Open healthcare_bronze_to_gold.ipynb
# Run all cells
```

### Step 5: Catalog Gold Layer
- Create crawler pointing to `s3://bucket/healthcare/gold/`
- Run crawler to catalog Gold analytics tables

### Step 6: Query with Athena
- Open Athena console
- Run SQL queries against Gold tables

## Sample SQL Queries

**Executive Summary:**
```sql
SELECT 
    COUNT(DISTINCT claim_id) as total_claims,
    ROUND(AVG(CAST(claim_amount AS DOUBLE)), 2) as avg_claim_amount,
    ROUND(SUM(CAST(claim_amount AS DOUBLE)), 2) as total_cost
FROM healthcare_db.claims
WHERE claim_id != 'claim_id';
```

**Top Diagnoses by Cost:**
```sql
SELECT diagnosis_code, total_claims, total_cost
FROM healthcare_db.gold_diagnosis_cost_analysis
ORDER BY total_cost DESC
LIMIT 10;
```

## Results & Deliverables

✅ **Bronze Layer:** 4 tables, 11,210 rows in S3  
✅ **Silver Layer:** Enriched dataset with 30 columns  
✅ **Gold Layer:** 6 analytics KPI tables  
✅ **Glue Data Catalog:** 10 tables cataloged  
✅ **Athena Queries:** 5 production SQL queries  

## Business Value

**For Insurance Companies:**
- Identify $88.9M in cancer treatment costs (top priority for case management)
- Flag 229 fraudulent claims (potential $25M+ savings)
- Prioritize 193 critical-risk patients for interventions
- Optimize provider network (remove high-denial-rate providers)

## Author

Vedant Achole  
Data Engineer  
[LinkedIn](#) | [GitHub](https://github.com/VedantVAchole)

## License

MIT License - Educational Project
