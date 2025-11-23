# High-Level Design & Folder Structure

## 📁 Proposed Folder Structure

```
s3-backed-kv-store-service/
├── README.md                    # Project documentation
├── Dockerfile                   # Container definition for the service
├── docker-compose.yml          # Orchestration (service + MinIO)
├── pyproject.toml              # Python project config & dependencies
├── requirements.txt            # Python dependencies (if using pip)
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration management
│   ├── api/                    # HTTP API layer
│   │   ├── __init__.py
│   │   ├── routes.py           # Route definitions
│   │   ├── handlers.py         # Request handlers
│   │   └── middleware.py       # Middleware (logging, metrics, etc.)
│   ├── storage/                # Storage abstraction layer
│   │   ├── __init__.py
│   │   ├── s3_client.py        # S3 client wrapper
│   │   ├── kv_store.py         # Key-value store interface & implementation
│   │   └── cache.py            # LRU cache (optional feature)
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── kv_item.py          # KV item model (with TTL support)
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── logger.py           # Structured logging setup
│       └── metrics.py          # Prometheus metrics (optional)
│
└── tests/                      # Test suite
    ├── __init__.py
    ├── conftest.py             # Pytest fixtures
    ├── unit/                   # Unit tests
    │   ├── __init__.py
    │   ├── test_storage.py     # Storage layer tests
    │   ├── test_kv_store.py    # KV store logic tests
    │   └── test_handlers.py    # Handler tests
    ├── integration/            # Integration tests
    │   ├── __init__.py
    │   ├── test_api.py         # HTTP API tests
    │   └── test_s3_integration.py  # S3 integration tests
    └── e2e/                    # End-to-end tests
        ├── __init__.py
        └── test_e2e.py         # Full workflow tests
```

## 🏗️ High-Level Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                    HTTP API Layer                       │
│  (FastAPI/Flask) - Routes, Handlers, Middleware        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              KV Store Service Layer                     │
│  - Business logic (TTL validation, versioning)         │
│  - Cache management (LRU if implemented)               │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Storage Abstraction Layer                  │
│  - S3 client wrapper                                    │
│  - Error handling & retries                             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              S3/MinIO Backend                           │
│  - Object storage                                       │
└─────────────────────────────────────────────────────────┘
```

### Key Design Decisions

#### 1. **Layered Architecture**
   - **API Layer**: Handles HTTP requests/responses, validation
   - **Service Layer**: Business logic, TTL management, caching
   - **Storage Layer**: S3 abstraction, handles persistence
   - **Benefits**: Separation of concerns, testability, maintainability

#### 2. **Storage Abstraction**
   - Abstract interface for storage operations
   - S3 implementation using `boto3` (AWS SDK)
   - Easy to swap implementations or add adapters
   - Handles S3-specific concerns (buckets, object keys, errors)

#### 3. **Configuration Management**
   - Environment variables for all config (no hardcoded values)
   - Centralized config module with validation
   - Supports both AWS S3 and MinIO endpoints

#### 4. **Optional Features Design**
   - **TTL**: Store expiration timestamp in metadata or object metadata
   - **LRU Cache**: In-memory cache layer before S3 access
   - **Versioning**: Append version suffix to S3 object keys
   - **Metrics**: Prometheus client for observability
   - **Logging**: Structured JSON logging with request IDs
   - **Graceful Shutdown**: Signal handlers for clean shutdown

#### 5. **Error Handling**
   - Consistent error responses
   - Proper HTTP status codes
   - Logging of errors with context

#### 6. **Testing Strategy**
   - **Unit Tests**: Mock S3 client, test business logic in isolation
   - **Integration Tests**: Test against real MinIO instance
   - **E2E Tests**: Full HTTP workflow tests

## 🔧 Technology Stack (Python)

- **Web Framework**: FastAPI (async, auto-docs) or Flask (simpler)
- **S3 Client**: `boto3` (AWS SDK)
- **Testing**: `pytest`, `pytest-asyncio` (if using FastAPI)
- **HTTP Client for Tests**: `httpx` or `requests`
- **Logging**: `structlog` or standard `logging` with JSON formatter
- **Metrics**: `prometheus-client` (optional)
- **Cache**: `cachetools` for LRU cache (optional)

## 📋 API Design

### PUT /kv/<key>
- **Input**: Raw text body
- **Query Params**: `ttl` (optional, e.g., `?ttl=30s`)
- **Output**: JSON with key and size
- **Storage**: Store as S3 object with key as object name
- **Metadata**: Store TTL expiration time in object metadata

### GET /kv/<key>
- **Input**: Key path parameter
- **Output**: Raw text body (200) or 404
- **Cache**: Check LRU cache first (if implemented)
- **TTL Check**: Validate expiration before returning (if TTL implemented)

## 🔄 Data Flow

### PUT Request Flow:
```
HTTP Request → Handler → KV Store Service → Cache Update → S3 Storage → Response
```

### GET Request Flow:
```
HTTP Request → Handler → Cache Check → KV Store Service → S3 Storage → TTL Validation → Response
```

## 🐳 Docker Strategy

- **Service Container**: Python app, exposes port (configurable)
- **MinIO Container**: S3-compatible storage, pre-configured bucket
- **Network**: Both containers on same Docker network
- **Volumes**: MinIO data persistence
- **Environment**: All config via env vars, no secrets in code

## 🧪 Testing Approach

1. **Unit Tests**: Mock boto3 S3 client, test logic without real storage
2. **Integration Tests**: Use test MinIO instance, verify S3 operations
3. **E2E Tests**: Full docker-compose setup, HTTP requests to service

## 📊 Observability (Optional Features)

- **Metrics**: Request count, latency, error rate, cache hit rate
- **Logging**: Request ID per request, structured JSON logs
- **Health Check**: `/health` endpoint for container orchestration

