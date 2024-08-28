provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-bucket-nametest71387tr892r98"  # Ensure this name is globally unique
  acl    = "private"

  tags = {
    Name        = "My Bucket"
    Environment = "Dev"
  }
}
