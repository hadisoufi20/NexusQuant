# Nexus Quant: Autonomous Market Execution Core

**Project Overview**
Nexus Quant is an agentic framework engineered to automate institutional-grade market analysis. The system implements a stateful, multi-agent architecture designed to minimize human bias and operational latency in structural market mapping. By integrating real-time macroeconomic data with encoded ICT (Inner Circle Trader) and Wyckoff logic, the framework provides a deterministic approach to liquidity and trend analysis.

**System Architecture & Methodology**
* **Orchestration Layer:** Utilizes `LangGraph` for recursive state management. This ensures that agentic workflows follow a deterministic path, preventing drift in complex multi-step reasoning cycles [Ref: `agents.py`].
* **Data Integration:** Features an abstraction layer for live financial data ingestion (`yfinance`). The core modules compute volatility-adjusted metrics (ATR-based) to filter high-probability structural setups [Ref: `tools.py`].
* **Algorithmic Logic:** Incorporates computational models for the automated detection of Order Blocks (OB) and Fair Value Gaps (FVG), translating subjective technical analysis into quantified systemic inputs.
* **Deployment & Monitoring:** Deployed via `Streamlit` with an embedded logging framework that prioritizes system integrity and runtime transparency.

**Technical Specifications**
* **Inference Engine:** `Groq (Llama-3.1-8b-instant)` — Selected for high-throughput, low-latency reasoning.
* **Orchestration Framework:** `LangChain` & `LangGraph` (v1.2+).
* **Quantitative Processing:** `Pandas` / `Numpy` for high-density matrix transformations.

**Engineering Philosophy**
The system is built on the principle of **"Guardrail-by-Design."** By separating structural mapping from speculative signaling, Nexus Quant maintains a high degree of operational precision, serving as a robust research tool for financial architecture.
