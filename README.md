# 🔗 Microservices CDC Testing Suite

[![CDC Pipeline](https://github.com/VladimirRamirez07/microservices-cdc-testing-suite/actions/workflows/cdc-pipeline.yml/badge.svg)](https://github.com/VladimirRamirez07/microservices-cdc-testing-suite/actions/workflows/cdc-pipeline.yml)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![Pact](https://img.shields.io/badge/Pact-Consumer--Driven-E43F5A?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMiAxNWwtNS01IDEuNDEtMS40MUwxMCAxNC4xN2w3LjU5LTcuNTlMMTkgOGwtOSA5eiIvPjwvc3ZnPg==)
![Docker](https://img.shields.io/badge/Docker-Pact%20Broker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-46%20tests-0A9EDC?logo=pytest&logoColor=white)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vladimir-ram%C3%ADrez-303a433ba)
![License](https://img.shields.io/badge/License-MIT-green)

> Production-grade **Consumer-Driven Contract (CDC) Testing** suite for microservices. Validates API communication between services **without deploying them all at the same time**, preventing breaking changes from reaching production.

---

## 📌 What is Consumer-Driven Contract Testing?

In a microservices architecture, services communicate through APIs. When a Provider changes its API without notifying Consumers, integrations break silently — often discovered only in production.

**CDC Testing solves this** by letting each Consumer define a **contract** describing exactly what it expects from a Provider. The Provider is then independently verified against every registered contract before any deployment.

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Consumer (OrderClient)                                │
│       │                                                 │
│       │  1. defines expectations                        │
│       ▼                                                 │
│   Pact Contract (JSON file)                             │
│       │                                                 │
│       │  2. published to Pact Broker                    │
│       ▼                                                 │
│   Provider (OrderService API)                           │
│       │                                                 │
│       │  3. verified against contract                   │
│       ▼                                                 │
│   ✅ Safe to deploy — or ❌ Breaking change detected   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🏗️ Project Structure

```
microservices-cdc-testing-suite/
│
├── 📁 consumer/
│   ├── src/
│   │   └── order_client.py           # HTTP client consuming the Order API
│   └── tests/
│       └── test_order_contract.py    # CDC tests — generates the Pact contract
│                                     # 23 contract interactions defined
│
├── 📁 provider/
│   ├── src/
│   │   └── order_service.py          # Flask REST API (the Provider)
│   └── tests/
│       └── test_provider_verify.py   # 23 provider verification tests
│
├── 📁 pacts/
│   └── OrderConsumer-OrderProvider-pact.json  # Generated contract
│
├── 📁 pact-broker/
│   └── docker-compose.yml            # Pact Broker + PostgreSQL
│
├── 📁 .github/workflows/
│   └── cdc-pipeline.yml              # CI/CD — 2 jobs, 46 tests total
│
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Contract Testing** | pactman 2.31 | CDC framework — Consumer & Provider |
| **Provider API** | Flask 3.0 | REST microservice (Order management) |
| **Consumer Client** | requests 2.32 | HTTP client consuming the Provider |
| **Test Runner** | pytest 8.3 + pytest-cov | Test execution and coverage |
| **Contract Storage** | Pact Broker + Docker | Contract versioning and history |
| **CI/CD** | GitHub Actions | Automated pipeline on every push |
| **Language** | Python 3.11+ | Core implementation language |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/orders` | List all orders |
| `GET` | `/orders?status={status}` | Filter orders by status |
| `GET` | `/orders/{id}` | Get a specific order |
| `POST` | `/orders` | Create a new order |
| `PATCH` | `/orders/{id}/status` | Update order status |
| `DELETE` | `/orders/{id}` | Delete an order |
| `GET` | `/health` | Health check |

**Valid statuses:** `pending` · `shipped` · `delivered` · `cancelled`

---

## 🧪 Test Coverage — 46 Tests

### Consumer Contract Tests (23)

| Category | Tests |
|---------|-------|
| `GET /orders/:id` | pending, shipped, delivered, cancelled, not found |
| `GET /orders` | all orders, filter by each status, invalid status |
| `POST /orders` | valid order, missing product, zero quantity, negative quantity |
| `PATCH /orders/:id/status` | to shipped, to delivered, to cancelled, not found, invalid status |
| `DELETE /orders/:id` | existing order, not found |
| `GET /health` | health check |

### Provider Verification Tests (23)
Mirror of every Consumer interaction — verifies the Provider honors **each contract interaction** independently.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip
- Docker Desktop (for Pact Broker)

### Installation

```bash
git clone https://github.com/VladimirRamirez07/microservices-cdc-testing-suite.git
cd microservices-cdc-testing-suite

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

---

## ▶️ Running the Tests

### Consumer — generates the Pact contract

```bash
pytest consumer/tests/test_order_contract.py -v
```

### Provider — verifies against the contract

```bash
pytest provider/tests/test_provider_verify.py -v
```

### Full suite — 46 tests

```bash
pytest consumer/tests/ provider/tests/ -v
```

**Expected result:**
```
46 passed in 48.34s
```

---

## 🐳 Pact Broker

Run the Pact Broker locally to store and version contracts:

```bash
cd pact-broker
docker-compose up -d
```

| | |
|--|--|
| **URL** | http://localhost:9292 |
| **Username** | admin |
| **Password** | admin |

---

## ⚙️ CI/CD Pipeline

The GitHub Actions pipeline triggers automatically on every push or pull request to `main`:

```
Push to main
     │
     ▼
┌─────────────────────┐
│  Job 1: Consumer    │  → runs 23 contract tests
│  Contract Tests     │  → uploads pact JSON as artifact
└────────┬────────────┘
         │ needs: consumer-tests
         ▼
┌─────────────────────┐
│  Job 2: Provider    │  → downloads pact artifact
│  Verification       │  → runs 23 verification tests
└─────────────────────┘
```

If the Provider breaks any contract interaction → **pipeline fails before deployment**.

---

## 📄 Contract Sample

```json
{
  "consumer": { "name": "OrderConsumer" },
  "provider": { "name": "OrderProvider" },
  "interactions": [
    {
      "description": "a request for a pending order",
      "providerState": "order 1 exists with status pending",
      "request": { "method": "GET", "path": "/orders/1" },
      "response": {
        "status": 200,
        "body": {
          "id": 1,
          "product": "Laptop",
          "quantity": 2,
          "status": "pending"
        }
      }
    }
  ]
}
```

---

## 🎯 Key Concepts Demonstrated

- ✅ Consumer-Driven Contract generation with **pactman**
- ✅ Full CRUD contract coverage (GET, POST, PATCH, DELETE)
- ✅ Validation and error handling contracts (400, 404 responses)
- ✅ Provider verification against all consumer interactions
- ✅ Independent microservice testing — no joint deployment needed
- ✅ Contract as CI/CD artifact passed between pipeline jobs
- ✅ Pact Broker for contract storage and versioning with **Docker**
- ✅ Automated breaking-change detection on every push

---

## 👤 Author

**Vladimir Ramirez** — QA Engineer

[![GitHub](https://img.shields.io/badge/GitHub-VladimirRamirez07-181717?logo=github)](https://github.com/VladimirRamirez07)