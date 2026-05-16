# 🔗 Microservices CDC Testing Suite

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Pact](https://img.shields.io/badge/Pact-Consumer--Driven-purple)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions)
![Docker](https://img.shields.io/badge/Broker-Docker-2496ED?logo=docker)
![Tests](https://img.shields.io/badge/Tests-3%20passed-brightgreen)

A production-grade **Consumer-Driven Contract (CDC) Testing** suite for microservices, built with Python, Pact, Flask, and GitHub Actions. Validates API communication between microservices **without deploying them all at the same time**.

---

## 📌 What is CDC Testing?

Consumer-Driven Contract Testing is a technique that ensures microservices can communicate with each other correctly. Instead of expensive end-to-end tests, each **Consumer** defines a **contract** describing what it expects from a **Provider**. The Provider is then independently verified against that contract.

```
Consumer (OrderClient)
    │
    │  defines expectations
    ▼
Pact Contract (JSON)
    │
    │  verified against
    ▼
Provider (OrderService / Flask API)
```

---

## 🏗️ Architecture

```
microservices-cdc-testing-suite/
├── consumer/
│   ├── src/order_client.py          # HTTP client consuming the Order API
│   └── tests/test_order_contract.py # CDC tests — generates the Pact contract
├── provider/
│   ├── src/order_service.py         # Flask REST API (the Provider)
│   └── tests/test_provider_verify.py# Verifies Provider against the contract
├── pact-broker/
│   └── docker-compose.yml           # Pact Broker for contract storage
├── pacts/
│   └── OrderConsumer-OrderProvider-pact.json
├── .github/workflows/
│   └── cdc-pipeline.yml             # CI/CD pipeline
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **pactman** | CDC testing framework (Consumer & Provider) |
| **Flask** | Provider microservice REST API |
| **requests** | Consumer HTTP client |
| **pytest** | Test runner |
| **Docker + Pact Broker** | Contract storage and history |
| **GitHub Actions** | CI/CD pipeline automation |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip
- Docker (for Pact Broker)

### Installation

```bash
git clone https://github.com/VladimirRamirez07/microservices-cdc-testing-suite.git
cd microservices-cdc-testing-suite

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

---

## ▶️ Running the Tests

### 1. Consumer Contract Tests
Generates the Pact contract file in `/pacts`:

```bash
pytest consumer/tests/test_order_contract.py -v
```

### 2. Provider Verification Tests
Verifies the Provider honors the contract:

```bash
pytest provider/tests/test_provider_verify.py -v
```

### 3. Full Suite

```bash
pytest consumer/tests/ provider/tests/ -v
```

Expected output:
```
consumer/tests/test_order_contract.py::test_get_existing_order     PASSED
consumer/tests/test_order_contract.py::test_get_nonexistent_order  PASSED
provider/tests/test_provider_verify.py::test_provider_honors_consumer_pact PASSED

3 passed in 5.22s
```

---

## 🐳 Pact Broker (Local)

Run the Pact Broker locally with Docker:

```bash
cd pact-broker
docker-compose up -d
```

Access the UI at: `http://localhost:9292`
Credentials: `admin / admin`

---

## ⚙️ CI/CD Pipeline

The GitHub Actions pipeline runs automatically on every push or pull request to `main`:

1. **Consumer Job** — runs CDC tests and generates the Pact contract
2. **Provider Job** — downloads the contract artifact and verifies the Provider against it

```
Push to main
    │
    ▼
Consumer Contract Tests ──► Upload pact artifact
    │
    ▼
Provider Verification Tests ◄── Download pact artifact
```

---

## 📄 Contract Example

The generated contract (`pacts/OrderConsumer-OrderProvider-pact.json`) describes the agreed interaction:

```json
{
  "consumer": { "name": "OrderConsumer" },
  "provider": { "name": "OrderProvider" },
  "interactions": [
    {
      "description": "a request for order 1",
      "request": { "method": "GET", "path": "/orders/1" },
      "response": {
        "status": 200,
        "body": { "id": 1, "product": "Laptop", "quantity": 2, "status": "pending" }
      }
    }
  ]
}
```

---

## 🎯 Key Concepts Demonstrated

- ✅ Consumer-Driven Contract generation with **pactman**
- ✅ Provider verification against consumer contracts
- ✅ Independent microservice testing without full deployment
- ✅ Contract as artifact passed through CI/CD stages
- ✅ Pact Broker for contract storage and versioning
- ✅ Full pipeline automation with **GitHub Actions**

---

## 👤 Author

**Vladimir Ramirez** — QA Engineer
[GitHub](https://github.com/VladimirRamirez07)