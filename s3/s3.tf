provider "aws" {
  region = "us-east-1"  # Specify the AWS region
}
 
resource "aws_s3_bucket" "basic_bucket" {
  bucket = "my-simple-bucket-${random_id.bucket_suffix.hex}"  # Unique bucket name
  acl    = "private"  # Set the access control list
}
 
resource "random_id" "bucket_suffix" {
  byte_length = 2  # Generates a sufficiently unique suffix for the bucket name
}