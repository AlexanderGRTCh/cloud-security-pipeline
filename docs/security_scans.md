# Security Scans

This project uses automated security scanning tools integrated into the CI/CD pipeline to ensure code and container security before deployment.

## 1. Bandit (Python Security Scanner)

Bandit is an open-source tool that performs static analysis of Python code to identify common security issues, such as command injection, hardcoded secrets, unsafe function usage, and insecure code patterns.

How Bandit is used in this project:
- Runs automatically in the GitHub Actions workflow before deployment.
- Scans the app directory for vulnerabilities using: bandit -r app/
- If critical issues are found, Bandit will report them in the pipeline logs.
- For demo purposes, the pipeline may be configured with --exit-zero so it does not fail on known vulnerabilities in intentionally insecure code.

What Bandit checks for:
- Shell injection vulnerabilities (e.g., use of os.system or os.popen)
- Hardcoded passwords and keys
- Insecure use of subprocess, eval, exec
- Weak cryptography
- Server binding to all interfaces

## 2. Trivy (Docker Image Vulnerability Scanner)

Trivy is an open-source scanner for container images, filesystems, and code repositories. It checks Docker images for known vulnerabilities in operating system packages and language libraries.

How Trivy is used in this project:
- Runs automatically in the CI/CD workflow after the Docker image is built on the EC2 server.
- Scans the built image using: ./trivy image flask_app
- Trivy outputs a vulnerability report to the pipeline logs.

What Trivy checks for:
- Operating system package vulnerabilities (CVEs)
- Application library vulnerabilities (Python, Node.js, etc.)
- Exposed secrets or misconfigurations in Docker images

## 3. Review and Results

- Security scan results are visible in the GitHub Actions pipeline logs for each build and deployment.
- Critical vulnerabilities should be fixed before moving to production.
- For educational/demo use, scan results may not block deployment, but all issues are still logged and reviewed.

## 4. Manual Usage

You can also run these tools locally for development or audit purposes:

To run Bandit locally:
pip install bandit
bandit -r app/

To run Trivy locally:
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh
./trivy image flask_app

Refer to the official Bandit and Trivy documentation for advanced options and interpreting results.
