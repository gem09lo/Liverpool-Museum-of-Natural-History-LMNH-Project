# Museum Visitors Feedback Data Engineering Project

##  Overview 
The Liverpool Museum of Natural History (LMNH) has undertaken an initiative to collect real-time feedback from its visitors through "Smiley Face Survey Kiosks" placed at exhibition exits. These kiosks allow visitors to rate their experience on a scale of five points (from 😡 to 😀) and include additional options like requesting assistance or reporting emergencies. The goal of this project was to address the museum's previous challenges of manual feedback collection and a lack of actionable insights.

# Project Aims
By implementing this data pipeline, LMNH aims to:
- Improve visitor engagement by monitoring satisfaction levels across all exhibitions.
- Enhance visitor safety with real-time processing of assistance or emergency requests.
- Provide key stakeholders (Exhibitions Manager and Head of Security) with near real-time updated dashboards for reliable decision-making.

This project was completed over two weeks and was split into two stages: processing historical data to build the foundation of the ETL (Extract, Transform, Load) pipeline during the first week, and integrating real-time live data during the second week.

## Project Structure
This project is structured into four primary components (each folder contains an individual README.md):
1. **Historical Data Pipeline** 
   Built to clean and process historical feedback data to establish the foundation for reporting and analysis.
2. **Live Data Pipeline** 
   Real-time pipeline that collects live feedback data from kiosks and updates the database continuously for up-to-date insights and reporting.
3. **Dashboard** 
   An interactive visual dashboard created to assist stakeholders in monitoring satisfaction and safety metrics.
4. **Automation & Setup Scripts** 
   Bash scripts to streamline setup tasks like creating virtual environments, installing dependencies, and deploying changes to a Git repository.

## Key Tools & Technologies
- **Programming Language**: Python
- **Data Streaming**: Kafka
- **Data Storage**: PostgreSQL (AWS RDS)
- **Automation**: Terraform (for provisioning AWS resources)
- **ETL**: Python modules for extraction (extract.py), transformation, and loading
- **Data Visualisation**: Tableau
- **Orchestration & Deployment**:
  - EC2 instance for continuous pipeline execution
  - Bash scripts for setup automation
- **AWS Resources**:
  - S3 (historical data storage)
  - EC2 (real-time pipeline)
  - RDS PostgreSQL (database for structured data)

## Folder Organisation
- **[pipeline]** Historical data pipeline scripts and related files: 
  This folder contains code for processing historical feedback data into the PostgreSQL database.
- **[live_pipeline]** Real-time data pipeline scripts: 
  This folder includes the consumer.py script, which acts as a Kafka consumer to validate and process live feedback data.
- **[dashboard]** Tableau dashboards:
  Contains visualisations and metrics for stakeholders alongside design wireframes and recommendations.
- **[bash]** Setup automation scripts: 
  Bash scripts for creating virtual environments, installing requirements, and staging changes for deployment on GitHub.

## 🛠️ Getting Setup

1. **AWS credentials** Ensure you have a `.env` file with your AWS credentials (ACCESS_KEY_ID, SECRET_ACCESS_KEY).
2. **Requirements** Install necessary packages: `pip install -r requirements.txt`.
3. **Database Setup** Ensure your PostgreSQL database is set up: `psql museum schema.sql`
4. **Running the Pipeline** Run the pipeline: `python pipeline.py --bucket <bucket_name> --rows <number_of_rows_to_upload>` (optional argument `--logs`)

## Setup Instructions
#### Setting up the Historical Data Pipeline
1. **Clone the Repository** 
   Clone the project repository to your local machine: 
   
bash
   git clone <REPO_URL>
   
2. **Environment Setup** 
   > Create a .env file containing AWS credentials (ACCESS_KEY_ID, SECRET_ACCESS_KEY).
3. **Install Dependencies** 
   Use a virtual environment (optional but recommended): 
   
bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r pipeline/requirements.txt
   
4. **Database Setup** 
   Create the necessary PostgreSQL tables using the schema: 
   ```bash
psql -h <RDS_HOST> -U <DB_USERNAME> -d postgres -f pipeline/schema.sql
   

1. **Run the Pipeline**  
   Execute the historical data ETL pipeline:  
   ```bash
   python pipeline/pipeline.py --bucket <BUCKET_NAME> --rows <NUM_ROWS> --logs


#### Setting up the Live Data Pipeline
1. **Kafka Setup** 
   Ensure you have access to a running Kafka Cluster and set configurations in .env.prod for Kafka and PostgreSQL credentials.
2. **Install Dependencies** 
   Install requirements for the live pipeline: 
   
bash
   pip install -r live_pipeline/requirements.txt
   
3. **Terraform Resource Provisioning** 
   Create necessary AWS resources with Terraform: 
   
bash
   cd live_pipeline/terraform
   terraform init
   terraform apply
   
4. **Run the Live Consumer** 
   Start processing live feedback data by running: 
   
bash
   python live_pipeline/consumer.py --logs
   
#### Setting up the Dashboard
1. Use Tableau to open the dashboard file located in the dashboard folder.
2. Connect Tableau to your PostgreSQL database to visualise feedback and safety metrics.
---
### Folder Structure and Key Files
#### [pipeline]
- pipeline.py: Main script for historical ETL pipeline (S3 → PostgreSQL). 
- schema.sql: Defines PostgreSQL database structure. 
- extract.py: Functions for data extraction and combining CSV files. 
- requirements.txt: Python dependencies for the pipeline. 
#### [live_pipeline]
- consumer.py: Main Kafka consumer script for live feedback ingestion. 
- terraform/: Scripts for provisioning AWS infrastructure.
#### [dashboard]
- tableau_visualisation.twbx: Interactive analysis dashboard for stakeholders. 
- recommendations.md: Strategies for improving visitor engagement using feedback insights.
