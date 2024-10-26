# monitor_script.py
from src.monitoring.model_monitoring import ModelMonitor
import pickle
import pandas as pd

# Load the model and reference data
with open("src/model/catboost_model.pkl", "rb") as f:
    model = pickle.load(f)

reference_data = pd.read_csv("data/cleaned/cleaned_data.csv")

# Initialize monitoring instance
monitor = ModelMonitor(model=model, reference_data=reference_data, bucket_name="your-s3-bucket")

# Load new/current data (replace with actual data path)
monitor.load_current_data("data/test/current_data.csv")

# Generate and save data drift report
monitor.generate_data_drift_report()
monitor.save_report_to_s3("data_drift_report")

# Generate and save performance report
monitor.generate_performance_report()
monitor.save_report_to_s3("performance_report")

# Optionally print metrics
data_drift_metrics = monitor.monitor_data_drift()
performance_metrics = monitor.monitor_performance()

print("Data Drift Metrics:", data_drift_metrics)
print("Performance Metrics:", performance_metrics)
