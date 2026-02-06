
# Smart Inventory Assistant 📦

A high-performance demonstration of **Context Optimization** using the **ScaleDown API**. This project features a modern full-stack architecture designed to reduce LLM costs and latency by compressing data before processing.

---

## 🚀 Overview

This system showcases how to efficiently handle large inventory datasets within an AI-driven interface. By using ScaleDown, the application compresses raw inventory context, ensuring the LLM receives only the most critical information—saving tokens, reducing costs, and improving response accuracy.

### Key Features

* **Context Optimization:** Real-time data compression via ScaleDown API.
* **Modern UI:** A sleek React + Tailwind CSS dashboard with dark mode.
* **FastAPI Backend:** Robust Python-based API with SQLite integration.
* **Live Metrics:** Dynamic visualization of token savings and compression ratios.

---

## 🛠️ Prerequisites

* **Python:** 3.9+
* **Node.js:** Latest LTS version (includes npm)
* **ScaleDown API Key:** Set as an environment variable `SCALEDOWN_KEY` or configure directly in `ai_logic.py`.

---

## ⚙️ Installation & Setup

### 1. Backend (FastAPI)

Navigate to the root directory and run:

```bash
# Install Python Dependencies
pip install -r requirements.txt

# Start the Backend Server
uvicorn main:app --reload
```

* Server URL: `http://localhost:8000`
* Note: `inventory.db` will be automatically generated and seeded on the first run.

### 2. Frontend (React)

Navigate to the frontend directory and run:

```bash
cd frontend

# Install Node Modules
npm install

# Start the Development Server
npm run dev
```

* UI URL: `http://localhost:5173`

---

## 🖥️ Demo Script for Supervisor

### Showcase 1: The Premium UI

* Open the dashboard and highlight the Dark Mode aesthetic.
* Display the "Live Inventory" table, explaining that this mimics a real-world enterprise SaaS tool.

### Showcase 2: Context Optimization (The Core Feature)

* **Action:** Type a query in the Chat box, e.g., "Which products need restocking?"
* **Observation:** Watch the "ScaleDown Savings" card animate.
* **Talking Points:**
  * "We sent the raw data (~Token count) to ScaleDown."
  * "It compressed the context by X% before sending it to the LLM."
  * "This saves roughly 80% of API costs in a production environment."

### Showcase 3: "Hallucination Check"

* **Action:** Ask about a product NOT in the table, e.g., "Do we have any Laptops?"
* **Result:** The system analyzes the compressed context (which contains only relevant items) and correctly says "No."
* **Insight:** This proves that optimization doesn't just save money; it improves accuracy by removing "noise" from the prompt.

---

## 🔧 Troubleshooting

* **Backend Connection Error:** Ensure `uvicorn` is running on port `8000`.
* **ScaleDown Error:** Check if `SCALEDOWN_KEY` is correct in `ai_logic.py`. If no key is provided, the system defaults to a fallback simulation for demo purposes.

---
