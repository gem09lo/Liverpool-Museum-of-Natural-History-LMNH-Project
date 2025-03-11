# Live Data Pipeline - Kafka Consumer for LMNH Feedback Pipeline

##  Overview
This script consumes messages from a Kafka topic related to the Liverpool Museum of Natural History (LMNH) feedback system. The messages contain visitor interactions, including exhibition ratings and assistance requests, collected from the museum's feedback kiosks. Valid messages are parsed and uploaded to an RDS PostgreSQL database, where they are stored in rating_interaction and request_interaction tables.

## Features
- Consumes messages from a Kafka topic (lmnh by default).
- Validates message content, including timestamps, exhibition sites, and ratings.
- Uploads valid data into a PostgreSQL database.
- Logs processed messages and warns about invalid messages, either to the terminal or a log file.

## Prerequisites
- `Kafka cluster`: You must have access to a running Kafka cluster, and ensure the `.env` file contains the necessary Kafka configuration.
- `PostgreSQL RDS database`: Set up a PostgreSQL database to store the exhibition feedback data. The `.env.prod` file should contain the RDS credentials.
- `Terraform`: Used to create the PostgreSQL RDS database.

## 🗂️ Files Explained

- `README.md`
  - This is the file you are currently reading
- `consumer.py`
  - Main pipeline for live data. Creating Kafka consumer and consume messages, clean transactions, and upload validated messages to database.
- `test_consumer.py`
  - Test file for consumer.py
- `consumer_earliest.py`
  - Experimenting with Kafka consuming messages in batch. 

## 🛠️ Getting Setup
1. **Install dependencies**
Create a virtual environment (optional but recommended):
`python -m venv venv`
`source venv/bin/activate`
Install required Python packages: 
`pip install -r requirements.txt`
2. **Environment Setup**
`.env` file: This file contains the Kafka configuration (bootstrap servers, credentials, etc.).
`.env.prod` file: This file contains sensitive information about the PostgreSQL RDS connection (e.g., DATABASE_USERNAME, DATABASE_PASSWORD, etc.).


## Setting Up the PostgreSQL Database
To set up the PostgreSQL database, you will need to:

1. **Create the RDS instance**
Run the following commands using Terraform:
`terraform init`
`terraform plan`
`terraform apply`
This will provision the necessary AWS resources, including the RDS instance for the museum's feedback data.

2. **Apply the database schema** 
After creating the RDS instance, load the schema using the following command: 
`psql -h <RDS_HOST> -p 5432 -U <db-username> -d postgres -f schema.sql`
This will set up the required tables for storing exhibition feedback data, including rating_interaction and request_interaction.

3. **Running the Kafka Consumer**
The consumer.py script connects to Kafka, retrieves and validates messages, and uploads valid data to the PostgreSQL database.

Running the Script
To start consuming messages, run the following: `python consumer.py`

Optional Arguments
Log invalid messages to file: You can log invalid messages to a consumer_errors.txt file using the --logs argument: `python consumer.py --logs`

## Message Validation
The script validates the following fields in Kafka messages:

- Timestamp (at): Must be a valid date and time, within the museum's operating hours (8:45 AM - 6:15 PM), and not from the future.
- Site (site): Must correspond to a valid exhibition site (values 0 to 5).
- Rating (val): Must be between -1 and 4. A rating of -1 requires a type value for request interactions.
- Logging
    - Terminal logging: By default, logs will be printed to the terminal.
    - File logging: Use the --logs argument to log invalid messages to a file (consumer_errors.txt).