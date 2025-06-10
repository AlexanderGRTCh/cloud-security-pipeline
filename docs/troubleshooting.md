# Troubleshooting

This file covers common issues encountered while working with the Cloud Security Pipeline project and how to resolve them.

## 1. Pipeline Fails on Bandit or Trivy Scan

**Problem:** The CI/CD pipeline fails because Bandit or Trivy found vulnerabilities.  
**Solution:**  
- For demo/testing, add `--exit-zero` to the Bandit command to avoid failing the build.
- Review the scan logs in GitHub Actions for specific issues.
- Fix code or Dockerfile vulnerabilities before production deployment.

## 2. Permission Denied Copying .git Files

**Problem:** Pipeline fails with permission errors copying files to EC2.  
**Solution:**  
- Make sure the deploy step excludes the `.git` directory (e.g., use `--exclude='.git'` with rsync).

## 3. Docker Permission Error (docker.sock)

**Problem:** Docker commands fail on EC2 with "permission denied while trying to connect to the Docker daemon socket".  
**Solution:**  
- SSH into the EC2 instance and run:  
  `sudo usermod -aG docker <your-username>`  
- Log out and back in, or restart the instance to apply group changes.

## 4. Port 5000 Not Reachable

**Problem:** You cannot access the Flask app in the browser at `http://<EC2-IP>:5000`.  
**Solution:**  
- Ensure the security group allows inbound traffic on port 5000.
- Confirm the Flask app is running inside Docker.
- Check Docker logs with `docker logs flask_app` on EC2 for errors.

## 5. SSH Connection Fails

**Problem:** Cannot connect to EC2 instance via SSH.  
**Solution:**  
- Verify you are using the correct public IP, username (`ubuntu`), and key.
- Ensure port 22 is open in the security group.
- Check your local firewall or VPN is not blocking SSH.

## 6. Terraform Apply Fails

**Problem:** Terraform shows errors or cannot create resources.  
**Solution:**  
- Double-check AWS credentials.
- Ensure your IAM user has sufficient permissions.
- Look at the Terraform error message for missing variables or AWS limits.

## 7. GitHub Actions Secrets Not Working

**Problem:** Pipeline can't connect to EC2 or deploys fail.  
**Solution:**  
- Make sure all required secrets are added in GitHub repository settings:
  - `EC2_SSH_KEY`
  - `EC2_USER`
  - `EC2_HOST`
- Secrets must have no extra spaces or newlines.

## 8. Port Tester Script Shows Open Ports That Should Be Closed

**Problem:** Port tester script (`scripts/port_tester.py`) detects unexpected open ports.  
**Solution:**  
- Double-check your security group configuration in `main.tf` to ensure only necessary ports are open.
- Re-run `terraform apply` to update rules if needed.

## Further Help

- Review GitHub Actions workflow logs for detailed error messages.
- Check AWS Console for instance and security group status.
- Use the [setup_guide.md](./setup_guide.md) for end-to-end instructions.
