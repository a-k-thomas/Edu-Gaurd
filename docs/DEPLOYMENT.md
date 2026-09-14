# Deployment Guide

Complete instructions for deploying the Dropout Risk Prediction System.

## Local Development

### Using Docker Compose (Recommended)

```bash
# Clone/navigate to project
cd "Real Dropout Predicter"

# Start all services
docker-compose up -d

# Access services
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Postgres: localhost:5432
- Redis: localhost:6379

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

### Manual Setup

#### Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
export DATABASE_URL="postgresql://user:pass@localhost:5432/db"
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Generate synthetic data
python data/synthetic_generator.py

# Run server
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Access at http://localhost:3000
```

## Database Setup

### PostgreSQL

#### Installation
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

#### Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE dropout_db;
CREATE USER dropout_user WITH PASSWORD 'dropout_pass';
GRANT ALL PRIVILEGES ON DATABASE dropout_db TO dropout_user;

# Quit
\q
```

#### Create Tables
```bash
# Backend automatically creates tables on startup
python app/main.py
```

## Cloud Deployment

### AWS Deployment

#### Prerequisites
- AWS Account
- AWS CLI configured
- Docker & Docker Compose installed

#### Architecture
```
┌─────────────────────────────────────┐
│        CloudFront (CDN)             │
├─────────────────────────────────────┤
│    S3 (Frontend - Static Assets)    │
├─────────────────────────────────────┤
│    Application Load Balancer        │
├───────────────┬──────────────┬──────┤
│   EC2         │   EC2        │ EC2  │  (Backend API)
│   Backend     │   Backend    │      │
└───────────────┴──────────────┴──────┘
        │
┌───────┴──────────────────────────────┐
│  RDS PostgreSQL (Read Replica)       │
└──────────────────────────────────────┘
        │
┌───────┴──────────────────────────────┐
│  ElastiCache Redis (Multi-AZ)        │
└──────────────────────────────────────┘
```

#### Step 1: Create RDS Database
```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier dropout-postgres \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username dropout_user \
  --master-user-password "YOUR_SECURE_PASSWORD" \
  --allocated-storage 20 \
  --publicly-accessible false

# Get endpoint
aws rds describe-db-instances \
  --db-instance-identifier dropout-postgres \
  --query 'DBInstances[0].Endpoint.Address'
```

#### Step 2: Create ElastiCache Redis
```bash
# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id dropout-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1

# Get endpoint
aws elasticache describe-cache-clusters \
  --cache-cluster-id dropout-redis \
  --show-cache-node-info
```

#### Step 3: Create EC2 Instances
```bash
# Create security group
aws ec2 create-security-group \
  --group-name dropout-sg \
  --description "Dropout Predictor Security Group"

# Open ports
aws ec2 authorize-security-group-ingress \
  --group-name dropout-sg \
  --protocol tcp --port 8000 --cidr 0.0.0.0/0 \
  --protocol tcp --port 22 --cidr 0.0.0.0/0

# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.small \
  --key-name my-key \
  --security-groups dropout-sg \
  --user-data file://user-data.sh
```

#### Step 4: Deploy Backend
```bash
# SSH into EC2
ssh -i my-key.pem ec2-user@instance-ip

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -a -G docker ec2-user

# Clone repo
git clone https://github.com/yourusername/dropout-predictor.git
cd dropout-predictor

# Create .env
cat > .env << EOF
DATABASE_URL=postgresql://dropout_user:password@rds-endpoint:5432/dropout_db
REDIS_URL=redis://elasticache-endpoint:6379/0
DEBUG=False
EOF

# Run with Docker
docker build -t dropout-backend ./backend
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name dropout-backend \
  dropout-backend

# Setup Nginx reverse proxy
sudo yum install nginx -y
# Configure /etc/nginx/nginx.conf
sudo systemctl start nginx
```

#### Step 5: Deploy Frontend
```bash
# Build frontend
cd frontend
npm install
npm run build

# Upload to S3
aws s3 sync dist/ s3://my-dropout-predictor-bucket/ --delete

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id E1234ABCD \
  --paths "/*"
```

#### Step 6: Setup Load Balancer
```bash
# Create Application Load Balancer
aws elbv2 create-load-balancer \
  --name dropout-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx

# Create target group
aws elbv2 create-target-group \
  --name dropout-tg \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxx

# Register targets
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --targets Id=i-xxx Id=i-yyy
```

### Azure Deployment

#### Prerequisites
- Azure Subscription
- Azure CLI installed
- Docker installed

#### Deployment Steps
```bash
# Create resource group
az group create --name dropout-rg --location eastus

# Create Container Registry
az acr create --resource-group dropout-rg \
  --name dropoutregistry --sku Basic

# Create PostgreSQL Server
az postgres server create \
  --resource-group dropout-rg \
  --name dropout-postgres \
  --location eastus \
  --admin-user dropout_user \
  --admin-password "YOUR_PASSWORD"

# Create App Service Plan
az appservice plan create \
  --name dropout-plan \
  --resource-group dropout-rg \
  --is-linux --sku B1

# Create Web App
az webapp create \
  --resource-group dropout-rg \
  --plan dropout-plan \
  --name dropout-api \
  --deployment-container-image-name dropout-backend

# Deploy
az webapp up \
  --resource-group dropout-rg \
  --name dropout-api \
  --docker-registry-server-url https://dropoutregistry.azurecr.io
```

## Environment Configuration

### Production .env
```
# Database
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/dropout_db

# Security
SECRET_KEY=generate-secure-random-key-here
DEBUG=False

# Redis
REDIS_URL=redis://elasticache-endpoint:6379/0
CELERY_BROKER_URL=redis://elasticache-endpoint:6379/1

# SMS (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=auth_token_here
TWILIO_PHONE_NUMBER=+1234567890

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=app_password_here

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

## SSL/HTTPS Setup

### Using Let's Encrypt with Certbot
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com -d api.yourdomain.com

# Renew automatically
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring & Logging

### CloudWatch (AWS)
```bash
# View logs
aws logs tail /aws/ecs/dropout-api --follow

# Create alarms
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu \
  --alarm-description "Alert on high CPU" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

### Application Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/dropout-api.log'),
        logging.StreamHandler()
    ]
)
```

## Backup Strategy

### Database Backups
```bash
# Daily automated backups in RDS
aws rds modify-db-instance \
  --db-instance-identifier dropout-postgres \
  --backup-retention-period 30

# Manual backup
aws rds create-db-snapshot \
  --db-instance-identifier dropout-postgres \
  --db-snapshot-identifier dropout-backup-$(date +%Y%m%d)
```

### File Backups
```bash
# S3 backup bucket
aws s3 mb s3://dropout-backup-bucket
aws s3 sync /data/uploads s3://dropout-backup-bucket/ --delete
```

## Scaling Strategy

### Horizontal Scaling
1. Use Auto Scaling Groups
2. Add load balancing
3. Use RDS read replicas
4. Redis cluster mode

### Vertical Scaling
1. Upgrade instance types
2. Increase database resources
3. Optimize database queries
4. Implement caching

## CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker images
        run: docker-compose build
      - name: Push to Registry
        run: docker push myregistry/dropout-backend:latest
      - name: Deploy to AWS
        run: |
          aws ecs update-service --cluster main \
            --service dropout-api \
            --force-new-deployment
```

---

*Deployment Guide Version: 1.0.0*
*Last Updated: March 5, 2026*
