# Load Balancer with Consistent Hashing - ICS 4104

## Overview

This project implements a custom load balancer using **consistent hashing** in a distributed systems context. It includes the ability to dynamically add/remove server containers, route requests intelligently, detect failures using heartbeat monitoring, and analyze load distribution performance.

The load balancer is built in **Python using Flask**, the backend servers are simple HTTP servers running Flask, and the entire system is containerized using **Docker** and orchestrated with **Docker Compose**.

---

## Features

* Consistent hashing with 512-slot ring
* Virtual nodes for better load balance (default K = 50)
* MD5-based request hashing
* Dynamic server addition/removal
* Failure detection via heartbeat
* REST API:

  * `GET /home?id=123` – route a request
  * `GET /rep` – get current replicas
  * `POST /add` – add servers
  * `DELETE /rm` – remove servers
* Performance analysis scripts for 10K requests and scaling test

---

## Challenges Faced

### 1. **Unfamiliarity with Docker and Server Dropping**

When restarting the project, old containers and networks were not cleaned up properly. This caused unexpected port conflicts and inconsistencies in container behavior. We learned that using `docker-compose down --volumes --remove-orphans` is critical when resetting a system.

### 2. **Route Mismatch During Testing**

During testing, an attempt was made to route requests to `/test` instead of the working `/home` endpoint. However, the `/test` route wasn’t implemented across all server containers, causing 404 errors and thousands of failed requests during analysis. The decision was made to revert to using only `/home` for both functionality and load testing.

### 3. **Severely Unbalanced Server Load**

Initial hashing logic using exponential formulas (e.g., `H(i) = i + 2^i + 17`) resulted in extremely skewed distributions, with one server handling over 96% of requests. This was resolved by switching to a new hash function using MD5 and increasing the number of virtual nodes per server. The new hash method was:

```python
h = hashlib.md5(str(i).encode()).hexdigest()
return int(h, 16) % self.num_slots
```

This greatly improved distribution and fairness across replicas.

---

## Load Distribution Analysis (Task 4)

### A-1: Load Distribution (10,000 Requests, 3 Servers)

* Server 1: 8003
* Server 2: 997
* Server 3: 1000
* Chart: `task4-a1-distribution.png`
* **Conclusion**: Imbalanced but greatly improved compared to original hash logic.

### A-2: Server Scaling (N = 2 to 6)

* Average requests per server tracked and plotted.
* Chart: `task4-a2-scaling.png`
* **Conclusion**: Consistent hashing scaled reasonably well when virtual nodes were increased to 50.

### A-3: Fault Tolerance

* Simulated failure by `docker stop server2`
* Heartbeat thread detected failure and removed server from ring
* Load balancer continued to function without interruption

### A-4: Alternative Hash Functions

* Switched to quadratic functions for both request and server hashing
* Re-ran tests and compared distribution to MD5-based logic
* Conclusion: MD5-based hashing offered better evenness with less tuning needed

---

## How to Run the Project

### 1. **Clone the project**

```bash
git clone <your-repo-url>
cd Load_balancer
```

### 2. **Build the containers**

```bash
docker-compose build
```

### 3. **Start the system**

```bash
docker-compose up
```

Leave this terminal open to show heartbeat and server logs.

### 4. **Send test request**

```bash
curl "http://localhost:5000/home?id=42"
```

### 5. **View current servers**

```bash
curl http://localhost:5000/rep
```

### 6. **Add server** (PowerShell)

```powershell
Invoke-WebRequest -Uri http://localhost:5000/add `
  -Method POST `
  -Body '{"n": 1, "hostnames": ["server4"]}' `
  -Headers @{"Content-Type" = "application/json"} `
  -UseBasicParsing
```

### 7. **Remove server** (PowerShell)

```powershell
Invoke-WebRequest -Uri http://localhost:5000/rm `
  -Method DELETE `
  -Body '{"ids": [2]}' `
  -Headers @{"Content-Type" = "application/json"} `
  -UseBasicParsing
```

---

## 📊 Run the Analysis Scripts

### Task 4-A1: 10K Requests Distribution

```bash
python test_load_distribution.py
```

### Task 4-A2: Scaling Test (N = 2 to 6)

```bash
python task4_a2_scaling_test.py
```

Charts will be saved as:

* `task4-a1-distribution.png`
* `task4-a2-scaling.png`

---

## Acknowledgments

Thanks to the ICS 4104 Distributed Systems course for pushing us through one of the most hands-on projects involving real-world infrastructure, deployment, and debugging skills.

---

## Cleanup

```bash
docker-compose down --volumes --remove-orphans
docker system prune -f
```

---

## Final Notes

* Use Postman or `curl` for API testing
* Always make sure containers are running before running analysis
* Check logs in Docker terminal for heartbeat feedback and routing decisions
