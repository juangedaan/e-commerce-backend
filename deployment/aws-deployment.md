# 🛰️ AWS Deployment Guide

## Social Commerce Backend & Recommendation Engine

---

## 📋 Prerequisites

- AWS Account
- IAM User with permissions:
  - EC2 (Launch, Manage Instances)
  - RDS (Create DB Instances)
  - S3 (Optional: for storing assets)
  - CloudFront (Optional: CDN)
- AWS CLI installed and configured (`aws configure`)
- Docker installed locally

---

## 🏗️ Architecture Overview

| Component | Service |
|-----------|---------|
| Backend API | EC2 Instance (Docker container) |
| Database | RDS (PostgreSQL) |
| Static assets (optional) | S3 + CloudFront |

---

## 🚀 Step-by-Step Deployment

### 1. Create the RDS PostgreSQL Instance

- Go to **RDS > Create Database**
- Choose **PostgreSQL**, Free Tier (if eligible)
- DB Settings:
  - DB Identifier: `socialcommerce-db`
  - Master username: `admin`
  - Password: `yourpassword`
- Connectivity:
  - Public access: **Yes**
  - VPC Security Group: allow port **5432**
- Launch the database.

✅ Save the **endpoint URL** (e.g., `socialcommerce-db.abcxyz.us-west-2.rds.amazonaws.com`).

---

### 2. Prepare Your EC2 Instance

- Go to **EC2 > Launch Instance**
- Choose:
  - AMI: Amazon Linux 2
  - Instance type: `t3.micro` or better
- Configure Security Group:
  - Allow ports **22 (SSH)** and **8000 (API Access)** from your IP
- Launch the instance and SSH into it:

```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

---

### 3. Install Docker on EC2

```bash
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
exit
```
(Reconnect SSH after `usermod`.)

✅ Docker should be ready now.

---

### 4. Upload and Run Your Project

#### Option 1: Build Locally and Push

Build a Docker image locally, push it to ECR, and pull it from EC2.

#### Option 2: Upload Code via SCP

```bash
scp -i your-key.pem -r * ec2-user@your-ec2-public-ip:/home/ec2-user/app
```

SSH again:

```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
cd app/backend
```

---

### 5. Set Environment Variables

Create a `.env` file on EC2 (`backend/.env`) like:

```dotenv
DATABASE_URL=postgresql://admin:yourpassword@your-rds-endpoint:5432/socialdb
AWS_REGION=us-west-2
```

---

### 6. Run with Docker Compose

Inside `/backend`:

```bash
docker-compose -f docker-compose.production.yml up --build -d
```

✅ This will:
- Spin up the FastAPI backend with Gunicorn
- Connect to your RDS database
- Serve the API on port **8000**

---

### 7. (Optional) Configure S3 and CloudFront for Static Files

- Upload any public static assets (like product images) to an S3 bucket.
- Create a CloudFront distribution pointing to the S3 bucket.

---

### 8. (Optional) Point a Domain Name

Use Route53 to create a domain alias pointing to your EC2 public IP or Elastic IP.

---

## ��️ Maintenance Tips

- **Auto-restart** containers with Docker `restart: always`.
- **Logs** can be inspected with:

```bash
docker logs container_name
```

- **Updates**:
  - SSH in
  - `git pull` if using Git
  - `docker-compose up --build -d` again

---

# 📦 Deployment Checklist

| Task | Status |
|-----|-------|
| RDS Postgres Created | ⬜ |
| EC2 Instance Created | ⬜ |
| Docker Installed | ⬜ |
| App Uploaded | ⬜ |
| Env Vars Set | ⬜ |
| Backend Running | ⬜ |

---

# ✅ Congratulations

Your **Social Commerce Backend** is live on AWS! 🚀

