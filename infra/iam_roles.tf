# Create an IAM Role for EC2, allowing only EC2 instances to assume it
resource "aws_iam_role" "ec2_instance_role" {
  name = "ec2_instance_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Define a policy granting only minimal permissions (least privilege) to EC2
resource "aws_iam_policy" "ec2_least_privilege" {
  name = "ec2_least_privilege_policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

# Attach the minimal-permission policy to the EC2 role
resource "aws_iam_role_policy_attachment" "attach_least_privilege" {
  role       = aws_iam_role.ec2_instance_role.name
  policy_arn = aws_iam_policy.ec2_least_privilege.arn
}

# Create an instance profile so the EC2 instance can use the role
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2_instance_role.name
}
