import boto3
import os

# Initialize S3 client
s3 = boto3.client('s3')

# Configuration
BUCKET_NAME = 'vedant-learning-raw-data'
BASE_PREFIX = 'healthcare/bronze'

# Files to upload
files_to_upload = [
    ('claims.csv', f'{BASE_PREFIX}/claims/claims.csv'),
    ('patients.csv', f'{BASE_PREFIX}/patients/patients.csv'),
    ('providers.csv', f'{BASE_PREFIX}/providers/providers.csv'),
    ('icd_codes.csv', f'{BASE_PREFIX}/icd_codes/icd_codes.csv')
]

print("="*50)
print("UPLOADING HEALTHCARE DATA TO S3")
print("="*50)
print(f"Bucket: {BUCKET_NAME}")
print(f"Base path: {BASE_PREFIX}\n")

# Upload each file
for local_file, s3_key in files_to_upload:
    local_path = f'../data/{local_file}'
    
    # Check file exists
    if not os.path.exists(local_path):
        print(f"❌ File not found: {local_path}")
        continue
    
    # Get file size
    file_size = os.path.getsize(local_path)
    size_kb = file_size / 1024
    
    print(f"Uploading {local_file} ({size_kb:.1f} KB)...")
    
    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
        print(f"  ✓ Uploaded to s3://{BUCKET_NAME}/{s3_key}\n")
    except Exception as e:
        print(f"  ❌ Error: {e}\n")

print("="*50)
print("UPLOAD COMPLETE!")
print("="*50)
print(f"\nVerify in AWS Console:")
print(f"S3 → {BUCKET_NAME} → healthcare/bronze/")
