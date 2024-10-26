# ~/airflow/dags/catboost_train_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import mlflow
import mlflow.catboost
import boto3
from catboost import Pool, CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os


# Define DAG default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Initialize the S3 client
s3_client = boto3.client('s3')

# Define the DAG
with DAG(
    'catboost_training_pipeline',
    default_args=default_args,
    description='Train CatBoost model and log results to MLflow',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    def load_data():
        df = pd.read_csv("data/cleaned/cleaned_data.csv")
        return df

    def train_catboost_model(**kwargs):
        # Load data from previous task
        df = kwargs['ti'].xcom_pull(task_ids='load_data')
        main_label = 'rating'

        # Extract target variable 'y' as a 1D array
        y = df[main_label].values.reshape(-1)
        
        # Create the feature matrix 'X'
        X = df.drop(columns=[main_label])
        
        # Identify categorical columns
        cat_cols = df.select_dtypes(include=['object']).columns
        cat_cols_idx = [X.columns.get_loc(col) for col in cat_cols]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.5, random_state=0
        )

        # Define model parameters
        model_params = {
            'iterations': 100,
            'depth': 9,
            'learning_rate': 0.03,
            'early_stopping_rounds': 100,
            'loss_function': 'RMSE',
            'verbose': 0
        }

        # MLflow experiment tracking
        with mlflow.start_run() as run:
            # Log model parameters
            mlflow.log_params(model_params)

            # Initialize data pools
            train_pool = Pool(data=X_train, label=y_train, cat_features=cat_cols_idx)
            test_pool = Pool(data=X_test, label=y_test, cat_features=cat_cols_idx)

            # Train model
            model = CatBoostRegressor(**model_params)
            model.fit(train_pool, eval_set=test_pool)

            # Predictions
            y_train_pred = model.predict(train_pool)
            y_test_pred = model.predict(test_pool)

            # RMSE Metrics
            rmse_train = mean_squared_error(y_train, y_train_pred, squared=False)
            rmse_test = mean_squared_error(y_test, y_test_pred, squared=False)

            # Log metrics
            mlflow.log_metric("RMSE_train", rmse_train)
            mlflow.log_metric("RMSE_test", rmse_test)

            # Log model
            mlflow.catboost.log_model(model, "catboost_model")

            # Pass the MLflow run ID and model to the next task
            kwargs['ti'].xcom_push(key='mlflow_run_id', value=run.info.run_id)
            kwargs['ti'].xcom_push(key='model', value=model)
            print(f"RMSE - Train: {round(rmse_train, 3)}, Test: {round(rmse_test, 3)}")
            print(f"MLflow Run ID: {run.info.run_id}")

    def save_model_to_s3(**kwargs):
        model = kwargs['ti'].xcom_pull(task_ids='train_catboost_model', key='model')
        mlflow_run_id = kwargs['ti'].xcom_pull(task_ids='train_catboost_model', key='mlflow_run_id')
        model_key = f"models/catboost_model_{mlflow_run_id}.pkl"

        # Serialize model and upload to S3
        s3_client.put_object(
            Bucket="model-artifacts-bucket",
            Key=model_key,
            Body=model.save_model(model_key)  # Save the model locally before uploading
        )
        print(f"Model saved to S3 with key {os.getenv(['MODEL_KEY_S3'])}")

    # Define the tasks in the DAG
    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    train_catboost_model_task = PythonOperator(
        task_id='train_catboost_model',
        python_callable=train_catboost_model,
        provide_context=True,
    )

    save_model_task = PythonOperator(
        task_id='save_model_to_s3',
        python_callable=save_model_to_s3,
        provide_context=True,
    )

    # Define task dependencies
    load_data_task >> train_catboost_model_task >> save_model_task
