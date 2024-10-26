# src/monitoring/model_monitoring.py
import pandas as pd
import boto3
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, RegressionPreset
from evidently.metrics import ColumnDriftMetric, RegressionPerformanceMetric
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, RegressionPerformanceTab
from evidently.model_monitoring import ModelMonitoring
from evidently.model_monitoring.monitors import DataDriftMonitor, RegressionPerformanceMonitor
import pickle

s3_client = boto3.client("s3")

class ModelMonitor:
    def __init__(self, model, reference_data, bucket_name="your-s3-bucket"):
        self.model = model
        self.reference_data = reference_data
        self.bucket_name = bucket_name
        self.current_data = None
        self.report = None

    def load_current_data(self, file_path):
        """Load the current data for prediction and monitoring."""
        self.current_data = pd.read_csv(file_path)

    def generate_data_drift_report(self):
        """Generate a data drift report using Evidently."""
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=self.reference_data, current_data=self.current_data)
        self.report = report

    def generate_performance_report(self):
        """Generate a performance report using Evidently for regression models."""
        # Assume `rating` is the target variable
        y_true = self.current_data['rating']
        X_current = self.current_data.drop(columns=['rating'])
        
        # Predict on current data
        y_pred = self.model.predict(X_current)
        self.current_data['predictions'] = y_pred
        
        report = Report(metrics=[RegressionPreset()])
        report.run(reference_data=self.reference_data, current_data=self.current_data)
        self.report = report

    def save_report_to_s3(self, report_name):
        """Save the Evidently report as an HTML file and upload to S3."""
        report_html = f"{report_name}.html"
        self.report.save_html(report_html)

        s3_client.upload_file(report_html, self.bucket_name, f"monitoring_reports/{report_html}")
        print(f"Report saved to S3 as monitoring_reports/{report_html}")

    def monitor_data_drift(self):
        """Run and return data drift monitoring metrics."""
        monitoring = ModelMonitoring(monitors=[DataDriftMonitor()])
        monitoring.execute(reference_data=self.reference_data, current_data=self.current_data)
        results = monitoring.metrics().get()
        return results

    def monitor_performance(self):
        """Run and return performance monitoring metrics for regression models."""
        monitoring = ModelMonitoring(monitors=[RegressionPerformanceMonitor()])
        monitoring.execute(reference_data=self.reference_data, current_data=self.current_data)
        results = monitoring.metrics().get()
        return results
