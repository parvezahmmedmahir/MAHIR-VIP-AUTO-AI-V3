# 🤖 MAHIR VIP AUTO AI V4 - The "Closed Candle" History Upgrade

> **State-of-the-Art Hybrid Trading Engine**  
> Blends Real Market Data (Yahoo Finance) with Professional OTC Simulation for Quotex.  
> **Exclusive Feature:** Focuses STRICTLY on Closed Candle Patterns (3 Black Crows / 3 White Soldiers).

[![Hybrid Engine](https://img.shields.io/badge/Engine-Hybrid%20Real%2FOTC-success)]()
[![Strategy](https://img.shields.io/badge/Strategy-3%20Black%20Crows-blue)]()
[![Websocket](https://img.shields.io/badge/Data-Passive%20Miner-orange)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green)]()

---

## 🚀 Key Innovations in V4

### 1. 🧠 Hybrid Data Engine
We solved the "Quotex OTC Problem" by building a dual-core engine:
- **⚡ Real Market Core:** Connects to **Yahoo Finance** for 50+ Major assets (EURUSD, BTC, DOGE, SHIB). This ensures your signals are based on Global Market Truth.
- **🤖 Smart OTC Core:** For fake assets (e.g., `TRUMP_OTC`), we use a **Volatility Clustering Simulator**. It generates price action that scientifically mimics the "Wicks" and "Trends" of the Quotex Algo.

### 2. 🕯️ "Closed Candle" Architecture
The system is built to ignore "running" candles which are volatile and deceptive.
- **History Miner:** The background WebSocket process passively listens for "Closed Candle" events.
- **Data Integrity:** Only fully formed candles are analyzed.

### 3. 🎯 Specific Strategy Focus
We removed all generic indicators (RSI, Bollinger) to focus 100% on **Price Action Patterns**:
- **Three Black Crows (Bearish):** Detects 3 consecutive powerful red candles.
- **Three White Soldiers (Bullish):** Detects 3 consecutive powerful green candles.

### 4. 💎 Transparent "Glass" UI
The user interface now shows you the **Logic** behind every signal:
- Displays **Strategy Name** (e.g., "Three White Soldiers").
- Displays **Data Source** (e.g., "⚡ Real Market" vs "🤖 OTC Algo").
- Visual "Scanning" animation.

---

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.8+
- Internet Connection

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Hybrid Engine
```bash
python main.py
```

### Step 3: Access Interface
Open your browser to:  
👉 **http://localhost:5000**

---

## 📂 Project Structure

```
MAHIR-VIP-AI-1/
├── main.py                 # The Brain. Runs Flask Server + WS Collector.
├── quotex_api.py           # The Logic. Contains 'PatternEngine' & 'SmartOTCEngine'.
├── quotex_live_api.py      # The Connector. Fetches Real Data (Yahoo) + Hybrid Mapping.
├── quotex_websocket.py     # The Miner. Silent background process for history.
├── index.html              # The Face. Premium Glassmorphism UI.
├── config.py               # Settings. Asset lists and parameters.
└── requirements.txt        # Dependencies.
```

---

## 📊 Supported Assets Logic

| Asset Type | Source | Example | Quality |
|:---|:---|:---|:---|
| **Forex (Major)** | ⚡ Real Market (Yahoo) | `EURUSD`, `GBPUSD` | ⭐⭐⭐⭐⭐ (Real) |
| **Crypto (Big)** | ⚡ Real Market (Yahoo) | `BTCUSD`, `ETHUSD` | ⭐⭐⭐⭐⭐ (Real) |
| **Meme Coins** | ⚡ Real Market (Yahoo) | `SHIB`, `PEPE`, `DOGE` | ⭐⭐⭐⭐⭐ (Real) |
| **Stocks** | ⚡ Real Market (Yahoo) | `MSFT`, `TSLA` | ⭐⭐⭐⭐⭐ (Real) |
| **Quotex OTC** | 🤖 Smart Simulation | `TRUMP_OTC` | ⭐⭐⭐⭐ (Algo Mimic) |

---

## ⚠️ Disclaimer
**Educational Tool Only.**  
This software is designed to analyze market patterns using algorithms. Trading Binary Options involves high risk.  
- **"Real Market"** data is sourced from public feeds (Yahoo Finance).  
- **"OTC Algo"** data is a mathematical simulation because OTC markets do not exist publicly.

---

**Made with 💛 by MAHIR VIP**  
*The Best or Nothing.*
