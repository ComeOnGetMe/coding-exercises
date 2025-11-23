# Take-Home Assignment  
## S3-Backed Key–Value Store Service (with Optional TTL)

**Estimated time:** 2–4 hours  
**Deliverable:** GitHub repo or zipped directory containing code + Docker setup  
**Languages allowed:** Any (Go / Python / Rust preferred but not required)  
**Evaluation focus:** API design, correctness, code quality, tests, observability, and containerization.

---

## 📘 Overview

Build a small HTTP service that functions as a persistent **key–value store**, backed by **S3 or an S3-compatible store** (e.g., MinIO).

Your service must expose the following HTTP APIs:

## 📌 Required Features

### **1. `PUT /kv/<key>`**
Stores a raw string value at the given key.

- Path parameter: `<key>`  
- Request body: raw text value  
- Must persist the value (in S3 or local S3-compatible storage)  
- Overwrite if the key already exists  
- **Response:**  
  - `200 OK`  
  - JSON object:  
    ```json
    {
      "key": "<key>",
      "size": <bytes_written>
    }
    ```

### **2. `GET /kv/<key>`**
Retrieves the stored value.

- **Response:**  
  - `200 OK` with the raw value in the body  
  - `404 Not Found` if the key does not exist

---

## ⭐ Optional Features (Choose Any Subset)

You may implement zero, one, or multiple of these. They are **bonus points only**.

- TTL on keys (`PUT /kv/<key>?ttl=30s`)  
- In-memory LRU cache  
- Key versioning  
- Prometheus metrics endpoint  
- Structured logging with request IDs  
- Graceful shutdown handling

---

## 📦 Persistence Requirements

Your service must store values in:

- An AWS S3 bucket **OR**
- A locally running S3-compatible service such as **MinIO** (via Docker)

Values must persist across container restarts.

---

## 🐳 Containerization Requirements

Your submission must include:

### **1. `Dockerfile`**
- Must build and run your service using Docker  
- No hardcoded credentials  

### **2. `docker-compose.yml`**
`docker-compose up` should launch:

- Your service  
- A MinIO container  
- Any other dependencies

### **3. Environment Variables**
All configuration must be passed via env vars, e.g.:

```
S3_ENDPOINT=
S3_BUCKET=
S3_ACCESS_KEY=
S3_SECRET_KEY=
PORT=
```
---

## 🧪 Testing Requirements

Provide at least:

- **Unit tests** for storage logic (including TTL, if implemented)

Nice-to-have:

- Integration tests  
- End-to-end HTTP tests  
- A `docker-compose run test` target  

---

## 📚 Repository Structure

Your repo should contain:

```
README.md
Dockerfile
docker-compose.yml
src/…
tests/…
```

### **README Must Include:**

- How to build the project  
- How to run it  
- Example cURL commands  
- Explanation of design choices  
- Description of any optional features implemented  

---

## 📊 Evaluation Criteria

| Category | What We're Looking For |
|---------|-------------------------|
| **Correctness** | API correctness, persistence behavior, edge cases |
| **Code Quality** | Clean structure, maintainable modules, naming clarity |
| **API Design** | Proper HTTP semantics, clear error messages |
| **Service Design** | Good abstractions, testability, scalability considerations |
| **Testing** | Meaningful unit/integration tests |
| **Dockerization** | Reproducible environment, no manual steps |
| **Optional Features** | Completeness, clarity, and value added |

---

## 🚀 Submission Instructions

Submit either:

- A link to a public GitHub repository **OR**
- A zipped project directory

We will run:

```
docker-compose up –build
```

Your service should start successfully and respond to `PUT` and `GET` requests as documented.

---

## ❓ Questions

You may ask clarifying questions if needed.  
You may also state assumptions—this is common in real production work.
