import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import DeploymentConfig

def validate_project_structure():
    """Validate the Netfolio project structure"""
    try:
        DeploymentConfig.validate_paths()
        print("✅ Project structure validated successfully")
    except ValueError as e:
        print(f"❌ Validation Error: {str(e)}")
        sys.exit(1)

def deploy_static_files():
    """Deploy static files to S3"""
    import boto3
    
    s3 = boto3.client('s3')
    static_files_path = DeploymentConfig.STATIC_FILES_PATH
    
    for root, dirs, files in os.walk(static_files_path):
        for file in files:
            file_path = os.path.join(root, file)
            s3_path = os.path.relpath(file_path, static_files_path)
            
            print(f"Uploading: {s3_path}")
            s3.upload_file(
                file_path,
                DeploymentConfig.S3_BUCKET_NAME,
                s3_path
            )

def main():
    print("Starting Netfolio deployment...")
    
    # Validate project structure
    validate_project_structure()
    
    # Deploy static files
    deploy_static_files()
    
    print("Deployment completed successfully!")

if __name__ == "__main__":
    main()
