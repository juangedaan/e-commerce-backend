# 🛍️ Social Commerce Backend & Recommendation Engine

This project simulates a **social commerce platform** backend with integrated user profiles, product catalogs, order processing, and a machine learning-based recommendation engine.

It is designed with **modular services**, high availability, **horizontal scalability**, and **sub-second API performance** in mind.

![Architecture Diagram](assets/diagram.png)

---

## 🚀 Features

- **FastAPI-based backend** with RESTful APIs
- **User Management**, Product Catalog, and Purchase Workflow modules
- **Basic ML-based recommendation engine** using user similarity
- **Exponential backoff and API rate limiting** for stability under high load
- **PostgreSQL** for structured data storage
- **AWS-ready** with EC2, RDS, S3, and CloudFront support
- **Real-time engagement hooks** and modular architecture for future feature growth

---

## 🧱 Architecture Overview

- **Client Applications:** Web or mobile frontend using REST APIs
- **FastAPI Backend:** Modular services for User, Product, Order, and Recommendation
- **PostgreSQL:** Stores users, products, and purchase data
- **Recommendation Engine:** Trained on interaction matrix and provides item suggestions
- **AWS Services:** Hosts infrastructure with EC2, RDS, S3, and CloudFront

---

## 📂 Folder Structure

```
e-commerce/
├── README.md
├── requirements.txt
├── dev-requirements.txt
├── .gitignore
├── .gitattributes
├── pytest.ini
├── assets/
│   ├── diagram.png
│   └── load_products.py
├── recommendation/
│   └── engine/
│       ├── recommender.py
│       └── utils.py
├── deployment/
│   ├── README.md
│   └── aws-deployment.md
├── backend/
│   ├── Makefile
│   ├── docker-compose.yml
│   ├── docker-compose.production.yml
│   ├── Dockerfile
│   ├── Dockerfile.production
│   ├── .flake8
│   ├── .mypy.ini
│   ├── .pre-commit-config.yaml
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db/
│   │   │   ├── init_db.py
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   └── utils.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── product_service.py
│   │   │   └── purchase_service.py
│   │   ├── api/
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── purchase.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── purchase.py
│   │   └── __init__.py  (optional)
│   └── tests/
│       ├── conftest.py
│       ├── test_users.py
│       ├── test_products.py
│       ├── test_purchases.py
│       └── test_user_service.py
```

---

## ⚙️ Setup Instructions

### 🧑‍💻 Prerequisites

- Python 3.9+
- PostgreSQL running locally or in AWS RDS
- Docker (optional, for local deployment)
- AWS CLI (optional, for deployment)

### 🔧 Local Setup

1. Clone the repo

```bash
git clone https://github.com/juangedaan/social-commerce-backend.git
cd social-commerce-backend
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set environment variables

Create a `.env` file in `backend/` and add:

```dotenv
DATABASE_URL=postgresql://username:password@localhost:5432/socialdb
AWS_REGION=us-west-2
```

5. Run the app

```bash
uvicorn backend.app.main:app --reload
```

6. Access API docs

Navigate to [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 ML Recommendation Engine

- Uses a simple **user-based collaborative filtering** approach
- Input: Simulated `user-product` interaction matrix
- Output: Product suggestions per user via `/recommendations/{user_id}` endpoint
- Engine trained with `scikit-learn`

---

## 🗂️ Dataset

This project uses a real-world e-commerce dataset to populate the product catalog and simulate user-product interactions:

- **Dataset Source:** [Amazon Products CSV - Luminati eCommerce Dataset Samples](https://github.com/luminati-io/eCommerce-dataset-samples/blob/main/amazon-products.csv)
- **Contents:** Thousands of product entries including name, category, price, rating, and other metadata fields.

Products will be imported into PostgreSQL during the database initialization phase.

---

## ✅ API Highlights

| Endpoint                      | Description                      |
|------------------------------|----------------------------------|
| `POST /users/`               | Create a user                    |
| `GET /products/`             | List all products                |
| `POST /orders/`              | Submit a purchase                |
| `GET /recommendations/{id}`  | Get product recommendations      |

---

## 🔐 Resilience & Performance

- **Rate limiting** with API throttles
- **Exponential backoff** on retry logic
- Query optimization for sub-second latency
- Horizontally scalable design across AWS regions

---

# 🚀 Quickstart Guide

## 📦 Setup Environment

```bash
pip install -r requirements.txt -r dev-requirements.txt
```

## 🏗️ Run Locally (Dev Mode)

```bash
cd backend
docker-compose up --build
```
The API will be available at [http://localhost:8000](http://localhost:8000).

## 🧪 Run Tests

```bash
make test
```
Or generate an HTML test report:

```bash
make test-html
```

## ☁️ Deploy to AWS

See [deployment/aws-deployment.md](deployment/aws-deployment.md) for detailed cloud deployment instructions.

---

## 📄 License

MIT License © Juan Moreno
