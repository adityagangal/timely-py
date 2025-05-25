# timely-py

## Introduction
This is the Python implementation of my timely-node backend. This porting is being done to ensure code can be easily maintained and understood by future maintainers. Partly to speed-up development because Python Supremacy!

This version uses Python | Fast-API | Beanie - Pydantic - Motor | MongoDB. 

The Android Front-End of the app is not uploaded because a few keys are present in my code, I don't feel comfortable posting them to github yet. :')


The other repo is present at [timely-node-mongo](https://github.com/RishiTiku/timely-node-mongo) and at [timely-node](https://github.com/RishiTiku/timely-node). I am sorry the first version is private because of keys present in testing and for them to be synced across devices, we directly used github with privacy.

The most challenging part of this project has been the schema design. Having conquered it, the rest of the development was easy. 

---

## System Design Summary
![SystemDesign drawio](https://github.com/user-attachments/assets/bd725e1f-6da2-4cd5-9ff3-e88d2199b2dd)

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
#### After populating DB with 10K Users, 200 batches and 10K Events
![image](https://github.com/user-attachments/assets/9b7ef5bf-2f70-42bb-806b-cf8c8cf6ebdd)
#### 100K Students, 50K Faculties, 2K Batches, 100K Events, Duplication Ratios :- Batches: Events = 1: ~100, Users: Batches = 1: ~7
These ratios signify data duplication due to denormalization, Event documents are the heavy ones.
![image](https://github.com/user-attachments/assets/92c5df90-1ed7-4b00-b80d-a43a2f4ed2ee)

No caching yet. Just Denormalization along with indexing. 0-2 ms per query is peak UX. Instant reads.

### The Mongo Schema Design
Schema design for this application has been a crucial part of its speed and ultimately its scalablity. It took 3 weeks and 4 iterations to make a Mongo friendly denormalised schema.
![image](https://github.com/user-attachments/assets/63e14450-69a8-4a77-8733-fbf2769bf333)

