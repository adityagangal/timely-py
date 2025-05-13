# timely-py

## Introduction
This is the Python implementation of my timely-node backend. This porting is being done to ensure code can be easily maintained and understood by future maintainers. Partly to speed-up development because Python Supremacy!

This version uses Python | Fast-API | Beanie - Pydantic - Motor | MongoDB. 

The Android Front-End of the app is not uploaded because a few keys are present in my code, I don't feel comfortable posting them to github yet. :')


The other repo is present at [timely-node-mongo](https://github.com/RishiTiku/timely-node-mongo) and at [timely-node](https://github.com/RishiTiku/timely-node). I am sorry the first version is private because of keys present in testing and for them to be synced across devices, we directly used github with privacy.

The most challenging part of this project has been the schema design. Having conquered it, the rest of the development was easy. 

---

## System Design Summary

---

### **Objective**

Efficiently serve personalized, real-time event data (live and recurring) to users with **minimal latency**, **low memory usage**, and **scalable architecture**.

---

### **Core Design Principles**

* **Read Optimization**

  * Precompute and cache event data in **Redis**, structured as: date → [(batch_id, event)], batch_id → [(date, event)]
  * Enables fast lookup of all relevant events for any batch on a given date.

* **Write-Heavy Optimizations**

  * Writes go to **MongoDB** (source of truth).
  * On batch or event changes, Redis cache is **invalidated or updated** via a **push notification**.

* **Data Push to Clients**

  * On changes to user batch memberships, user-batch mapping in cache is updated.
  * Ensures **zero DB hits** for user-batch mapping reads.

---

### **Caching Strategy**

* Redis stores:
  * `user_id → [batch_ids]`
  * `batch_id → [event objects]`
* This ensures **Normalization over Duplication** preventing explosive and redundant users * events mapping.
* Optimized for 500K+ users with <100MB usage.
* Most requests served **entirely from Redis**.

---

### **Query Flow**

1. **User login** → Fetch from Redis: `user_id → batch_ids`
2. **Get events** → Fetch from Redis: `batch_id → [events]`
3. **Flatten events** → Serve to client (sorted, filtered)

---

### **Performance**

* Each read path (user → batches → events): **\~15-20ms**
* Can handle **500+ concurrent user reads/sec**
> 99% of read requests **served from Redis**

---

### **Scalability & Concurrency**

* Writes decoupled via **Redis-backed queues** (producer-consumer pattern)
* Optional: Add **priority queue** to prioritize writes over reads during spikes
* Supports **horizontal scaling** for both Redis and API server

---

### **Stack**

* **Backend**: FastAPI + MongoDB (writes)
* **Cache**: Redis (reads, queues)
* **Messaging**: Redis Pub/Sub for updates to client
* **Infra-ready**: Can scale reads and writes independently

---

### **Scalable To**

* 500K+ users
* 1000+ batches
* 10–20 batch associations per user
* 10–50 events per batch per week

---

## Intermediate mini victories
### Love making my app faster for best UX
![image](https://github.com/user-attachments/assets/26dabfb2-f181-4b63-a6d9-635475d4fab6)

0-1 ms per query... I'd love to keep it that way!

### The Mongo Schema Design
Schema design for this application has been a crucial part of its speed and ultimately its scalablity. It took 3 weeks and 4 iterations to make a Mongo friendly denormalised schema.
![image](https://github.com/user-attachments/assets/63e14450-69a8-4a77-8733-fbf2769bf333)

