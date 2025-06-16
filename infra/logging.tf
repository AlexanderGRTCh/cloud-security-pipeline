data "aws_caller_identity" "current" {}
# Create an S3 bucket to store CloudTrail logs
resource "aws_s3_bucket" "trail_bucket" {
  bucket        = "cloud-trailing-024061-bucket" 
  force_destroy = true                                 # Allows Terraform to delete bucket even if it has objects (for easy cleanup)
}

# Create a CloudTrail to record all AWS API calls
resource "aws_cloudtrail" "main" {
  name                          = "main-cloudtrail"         # Name of the CloudTrail
  s3_bucket_name                = aws_s3_bucket.trail_bucket.id # Store logs in the S3 bucket 
  include_global_service_events = true                       # Log global services (like IAM)
  is_multi_region_trail         = true                       # Record API activity in all AWS regions
  enable_log_file_validation    = true                       # Add extra security: CloudTrail can verify log file integrity
}

resource "aws_guardduty_detector" "main" {
  enable = true
}

resource "aws_s3_bucket_policy" "trail_bucket_policy" {
  bucket = aws_s3_bucket.trail_bucket.id    # Attach this policy to our CloudTrail S3 bucket

  policy = jsonencode({
    Version = "2012-10-17",                 # Policy language version (standard, always use this)
    Statement = [
      {
        Sid = "AWSCloudTrailAclCheck",      # Statement ID (CloudTrail ACL check permission)
        Effect = "Allow",                   # Allow the following action
        Principal = {
          Service = "cloudtrail.amazonaws.com"  # AWS CloudTrail service is the principal (who gets permission)
        },
        Action = "s3:GetBucketAcl",         # CloudTrail needs to read bucket ACL (required by AWS)
        Resource = aws_s3_bucket.trail_bucket.arn # The bucket itself (not objects inside)
      },
      {
        Sid = "AWSCloudTrailWrite",         # Statement ID (CloudTrail write permission)
        Effect = "Allow",                   # Allow the following action
        Principal = {
          Service = "cloudtrail.amazonaws.com"   # AWS CloudTrail service is the principal
        },
        Action = "s3:PutObject",            # Allow CloudTrail to write logs into the bucket
        Resource = "${aws_s3_bucket.trail_bucket.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*", 
        # AWS recommends writing logs to AWSLogs/{AccountID}/*
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control" # Require full control for bucket owner (security best practice)
          }
        }
      }
    ]
  })
}
