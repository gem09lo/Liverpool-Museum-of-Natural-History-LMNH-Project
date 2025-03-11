# Historical Pipeline

##  Overview - Data Extraction Pipeline
The historical pipeline extracts historical data from an AWS S3 bucket, transforms it, and loads it into a PostgreSQL database. This pipeline runs manually but is designed to be hosted on an EC2 instance so that it can continuously process incoming data if required.

## 🛠️ Getting Setup

1. **AWS credentials** Ensure you have a `.env` file with your AWS credentials (ACCESS_KEY_ID, SECRET_ACCESS_KEY).
2. **Requirements** Install necessary packages: `pip install -r requirements.txt`.
3. **Database Setup** Ensure your PostgreSQL database is set up: `psql museum schema.sql`
4. **Running the Pipeline** Run the pipeline: `python pipeline.py --bucket <bucket_name> --rows <number_of_rows_to_upload>` (optional argument `--logs`)


## 🗂️ Files Explained

- `README.md`
  - This is the file you are currently reading
- `extract.py`
  - Contains functions for connecting to S3, downloading files, and combining CSV files.
- `pipeline.py`
  - This is the main script of the pipeline. It downloads the data from S3, uploads and it into the PostgreSQL database. It also includes reading command-line arguments and logging.
- `schema.sql`
  - SQL script sets up the database schema. It creates the tables for storing exhibition feedback data, including ratings and request interactions.
- `lmnh_exhibition_combined.json`
  - A JSON file containing data about the museum exhibitions
- `lmnh_hist_data.csv`
  - This script contains data of the kiosk ratings that is uploaded to the database
- `analysis.ipynb`
  - This is a data exploration of the cleaned database using SQL queries.
- `advance_queries.sql`
  - More data exploration using more complex SQL queries.
- `main.tf`
  - Terraform script for AWS cloud deployment of pipeline.

# Terraform
The Terraform files in this folder will automatically deploy:
✅ An EC2 instance where the pipeline can run.
✅ A PostgreSQL RDS instance where data will be stored.
✅ A security group to control access.

# Infrastructure Architecture
The infrastructure works as follows:
- `EC2 Instance`: This is the virtual server where your pipeline (pipeline.py) will run. It extracts data from S3 and loads it into the PostgreSQL database.
- `RDS Database (PostgreSQL)`: This cloud-hosted database stores feedback data from the museum's visitor feedback kiosks.
- `Security Groups`: Protect the database and EC2 instance from unauthorized access.
- `S3 Bucket (optional)`: The data pipeline extracts historical data from S3.

