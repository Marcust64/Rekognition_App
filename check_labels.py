from dotenv import load_dotenv
import os
import boto3

#Loads AWS credentials from .env
load_dotenv()

#Boto3 uses the Rekognition service, manually passes keys from .env
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

#Scans images and return labels of greater than 75% of confidence
def detect_labels_from_s3(bucket_name, image_name):
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': image_name
            }
        },
        MaxLabels=10,
        MinConfidence=75
    )

    print(f"\nLabels detected in '{image_name}':\n")
    for label in response['Labels']:
        print(f"🟢 {label['Name']} ({label['Confidence']:.2f}%)")

if __name__ == "__main__":
    bucket = "imagestorage6594"
    image = input("Enter the image file name in S3 (e.g., dog.jpg): ")

    detect_labels_from_s3(bucket, image)
