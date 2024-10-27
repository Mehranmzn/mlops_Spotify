
```sql
USE ROLE ACCOUNTADMIN;

-- Create the `transform` role
CREATE ROLE IF NOT EXISTS transform;
GRANT ROLE TRANSFORM TO ROLE ACCOUNTADMIN;

-- Create the default warehouse if necessary
CREATE WAREHOUSE IF NOT EXISTS SPOTIFY_POD;
GRANT OPERATE ON WAREHOUSE SPOTIFY_POD TO ROLE TRANSFORM;

-- Create the `dbt` user and assign to role
CREATE USER IF NOT EXISTS dbt
  PASSWORD='dbtPassword123'
  LOGIN_NAME='dbt'
  MUST_CHANGE_PASSWORD=FALSE
  DEFAULT_WAREHOUSE='SPOTIFY_POD'
  DEFAULT_ROLE='transform'
  DEFAULT_NAMESPACE='SPOTIFY.RAW'
  COMMENT='DBT user used for data transformation';
GRANT ROLE transform to USER dbt;

-- Create our database and schemas
CREATE DATABASE IF NOT EXISTS SPOTIFY;
CREATE SCHEMA IF NOT EXISTS SPOTIFY.RAW;

-- Set up permissions to role `transform`
GRANT ALL ON WAREHOUSE SPOTIFY_POD TO ROLE transform; 
GRANT ALL ON DATABASE SPOTIFY to ROLE transform;
GRANT ALL ON ALL SCHEMAS IN DATABASE SPOTIFY to ROLE transform;
GRANT ALL ON FUTURE SCHEMAS IN DATABASE SPOTIFY to ROLE transform;
GRANT ALL ON ALL TABLES IN SCHEMA SPOTIFY.RAW to ROLE transform;
GRANT ALL ON FUTURE TABLES IN SCHEMA SPOTIFY.RAW to ROLE transform;
```


```sql
USE WAREHOUSE SPOTIFY_POD;
USE DATABASE spotify;
USE SCHEMA RAW;

-- Create our three tables and import the data from S3
CREATE OR REPLACE TABLE dim_date (
    day_of_week VARCHAR(20),
    month VARCHAR(20),
    date_id NUMBER PRIMARY KEY  -- Use format YYYYMMDD

);

COPY INTO dim_date
FROM 's3://mymlops-project/dim_date.csv'
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1) ;


-- Dimension Table: dim_region
CREATE OR REPLACE TABLE dim_region (
    region VARCHAR(50),
    region_id INT AUTOINCREMENT PRIMARY KEY

);

-- Dimension Table: dim_show
CREATE OR REPLACE TABLE dim_show (
    publisher VARCHAR(100),
    explicit BOOLEAN,
    is_externally_hosted BOOLEAN,
    is_playable BOOLEAN,
    language VARCHAR(50),
    show_explicit BOOLEAN,            -- Renaming to avoid conflict
    show_is_externally_hosted BOOLEAN, -- Renaming to avoid conflict
    media_type VARCHAR(50),
    show_id INT AUTOINCREMENT PRIMARY KEY

);



-- Fact Table: fact_show_metrics
CREATE OR REPLACE TABLE fact_show_metrics (
    date_id INT,
    region_id INT,
    show_id INT,
    rating FLOAT,
    log10_duration FLOAT,
    log10_episodes FLOAT,
    PRIMARY KEY (date_id, region_id, show_id),  -- Composite primary key
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (show_id) REFERENCES dim_show(show_id)
);



-- Load data into dim_region
COPY INTO dim_region
FROM 's3://mymlops-project/dim_region.csv'
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);

-- Load data into dim_show
COPY INTO dim_show
FROM 's3://mymlops-project/dim_show.csv'
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);

-- Load data into fact_show_metrics
COPY INTO fact_show_metrics
FROM 's3://mymlops-project/fact_show_metrics.csv'
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);
```
