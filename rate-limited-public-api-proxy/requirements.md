# Take-Home Assignment

## Rate-Limited Public API Proxy Service

**Estimated time:** 2–4 hours  
**Deliverable:** GitHub repo or zipped project with Docker setup  
**Languages allowed:** Any (Go / Python / Rust preferred but not required)  
**Evaluation focus:** API design, correctness, code quality, rate limiting, caching, observability, containerization

---

## 📘 Overview

Build a small HTTP service that proxies requests to a public API and adds **per-client rate limiting**, **response caching**, and **basic observability**.

The goal is to simulate building a safe, production-ready API gateway.

Your service will:  
- Accept incoming requests from clients  
- Forward them to an external public API  
- Enforce per-client rate limits  
- Cache results to reduce load  
- Expose Prometheus-compatible metrics

---

## 📌 Required Features

### **1. Proxy Endpoint: `GET /proxy`**

Your service should accept:

**Request:**  
```
GET /proxy?url=<ENCODED_URL>
```
Example:
```
/proxy?url=https%3A%2F%2Fapi.github.com%2Frepos%2Ftorvalds%2Flinux
```

**Behavior:**
1. Extract the `url` parameter  
2. Validate that it's an HTTP/HTTPS URL  
3. Forward the request to that URL  
4. Return the upstream response to the client  
5. Apply per-client **rate limiting**  
6. Apply **read-through caching** based on the full URL

**Client Identity Definition:**  
Use **client IP address** (`X-Forwarded-For` allowed) unless you implement a different scheme.

**Response:**  
- `200 OK` with upstream response body  
- Proper error code on failures  
- Include a header `X-Cache: HIT|MISS`

---

## ⭐ Required Feature: Per-Client Rate Limiting

Implement a **token bucket** or **leaky bucket** rate limiter.

Minimum requirement:
Each client IP is limited to:
* 10 requests per minute, AND
* 2 requests per second

If the client exceeds the limit:

```
429 Too Many Requests
Retry-After: 
```
Rate limiter may be in-memory or Redis-based.  
(If using Redis, include it in docker-compose.)

---

## ⭐ Required Feature: Response Caching

Implement read-through caching:

- Cache key: the full target URL  
- Cache value: the full HTTP response body  
- Cache expiration: 30 seconds (fixed)

If cached:

```
X-Cache: HIT
```

If fetched from upstream:
```
X-Cache: MISS
```

Cache may be:

- In-memory cache (LRU or TTL-based), **OR**
- Redis (recommended for higher-level candidates)

---

## ⭐ Required Feature: Metrics Endpoint

Expose:
```
GET /metrics
```

The endpoint must expose Prometheus text format metrics, including:

- Request count  
- Upstream latency histogram  
- Cache hit/miss counters  
- Rate limit rejection count  

Example metric names:
```
proxy_requests_total
proxy_cache_hits_total
proxy_cache_misses_total
proxy_rate_limited_total
proxy_upstream_latency_seconds_bucket
```
---

## 📦 Containerization Requirements

Your project must include:

### **1. `Dockerfile`**
- Builds and runs your service  
- No hardcoded credentials or absolute paths

### **2. `docker-compose.yml`**
`docker-compose up` should start:

- Your service  
- Optional Redis or other cache backend  
- Optional Prometheus container (if you set it up, not required)

### **3. Environment Variables**

Example:
```
PORT=
CACHE_BACKEND=memory|redis
REDIS_HOST=
REDIS_PORT=
RATE_LIMIT_RPS=2
RATE_LIMIT_RPM=10
```


---

## 🧪 Testing Requirements

At minimum include **unit tests** for:

- Rate limiter  
- Cache layer  
- Input validation of proxy URL  
- Error handling for upstream failures  

Nice-to-have:

- Integration tests (end-to-end proxy flow)  
- Docker-based tests via `docker-compose run test`  

---

## 📚 Repository Structure

A typical structure:

```
README.md
Dockerfile
docker-compose.yml
src/…
tests/…
```

### Your `README.md` must include:

- How to run via Docker  
- Example `curl` commands  
- Explanation of rate limiter implementation  
- Explanation of caching logic  
- Anything optional that you added  

---

## 📊 Evaluation Criteria

| Category | What We're Looking For |
|---------|-------------------------|
| **Correctness** | Proxy behavior, caching behavior, rate limit enforcement |
| **Code Quality** | Clear structure, modularity, readable code |
| **API Design** | Proper HTTP semantics, correct status codes |
| **Service Design** | Configurability, testability, reliability |
| **Testing** | Quality of tests and coverage of important paths |
| **Dockerization** | Reproducible environment, ease of use |
| **Observability** | Useful metrics, logs, traceability |

---

## 🚀 Submission Instructions

Submit either:

- A GitHub repo **OR**  
- A zipped repo

We will run:
```
docker-compose up –build
```

Your service should:

- Start successfully  
- Enforce rate limits  
- Cache results  
- Proxy external requests  
- Expose `/metrics`  

---

## ❓ Questions

If something is unclear or underspecified, make reasonable assumptions and include them in your README.

---
