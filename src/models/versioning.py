# src/models/versioning.py
import boto3
import pickle
import os

def get_model_version():
    # Simple versioning based on an incrementing file count; customize as needed
    version_file = "model_version.txt"
    if not os.path.exists(version_file):
        with open(version_file, 'w') as f:
            f.write("1")
        return 1
    else:
        with open(version_file, 'r+') as f:
            version = int(f.read().strip()) + 1
            f.seek(0)
            f.write(str(version))
            f.truncate()
        return version

def save_model_to_s3(s3_client, model, model_key, metadata, bucket_name="your-s3-bucket"):
    # Serialize the model
    model_data = pickle.dumps(model)
    
    # Save the model to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=model_key,
        Body=model_data,
        Metadata={k: str(v) for k, v in metadata.items()}
    )
    print(f"Model version {metadata['version']} saved to {bucket_name}/{model_key}")
