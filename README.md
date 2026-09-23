# Nexus Quant — Autonomous Market Structure Analyzer

**Agentic research framework for market structural analysis (XAU/USD).**
Built with LangGraph, Groq (Llama 3.1), and ICT / Wyckoff logic.

## Project Overview

Nexus Quant is an agentic framework that automates market structural mapping. It implements a stateful,
multi-agent architecture designed to reduce human bias and operational latency by integrating market data with
encoded ICT (Inner Circle Trader) and Wyckoff logic, producing a deterministic approach to liquidity and trend
analysis.

## System Architecture & Methodology

| Layer | What it does | Reference |
|---|---|---|
| **Orchestration** | LangGraph `StateGraph` for recursive state management. Agentic workflows follow a deterministic path, preventing drift in multi-step reasoning cycles | [`agents.py`](agents.py) |
| **Data integration** | Abstraction layer for market data ingestion (`yfinance`). Volatility-adjusted (ATR-based) metrics filter structural setups | [`tools.py`](tools.py) |
| **Algorithmic logic** | Computational detection of Order Blocks (OB) and Fair Value Gaps (FVG) — turning subjective technical analysis into quantified system inputs | [`tools.py`](tools.py) |
| **Deployment & monitoring** | Streamlit interface with an embedded logging framework for runtime transparency | [`main.py`](main.py) |

## Technical Specifications

- **Inference engine:** Groq — Llama-3.1-8b-instant (selected for low-latency reasoning)
- **Orchestration:** LangChain / LangGraph
- **Quantitative processing:** pandas / NumPy
- **Interface:** Streamlit
- **Market data:** yfinance

## Engineering Philosophy — Guardrail by Design

The system separates structural mapping from speculative signalling. That separation follows the same discipline as
the ZVAKTHOR execution architecture: **the component that can influence a decision is not the component that
authorises it.**

## Quick Start

```bash
git clone https://github.com/hadisoufi20/NexusQuant.git
cd NexusQuant
pip install -r requirements.txt
cp .env.example .env        # then set GROQ_API_KEY
streamlit run main.py
```

Get a Groq API key at https://console.groq.com/keys.

## Status & Scope — read before use

- **Research and educational tool.** A market-structure analysis framework; it does not place orders.
- **No performance claims.** Nothing in this repository claims returns, profitability, or live trading results.
- **Public scope.** This repository publishes the structural and reasoning modules. High-frequency execution
  pipelines and production inference configuration remain proprietary.
- **Not investment advice.**

## Related

- **Architecture overview:** [hadisoufi20.github.io](https://hadisoufi20.github.io/)
- **Research — four SSRN working papers:** [ssrn.com/author=13197688](https://ssrn.com/author=13197688)
- **ORCID:** [0009-0009-4656-5983](https://orcid.org/0009-0009-4656-5983)
- **Author:** Hadi Soufi — AI systems architect, Founder of ZVAKTHOR

## License

Proprietary - all rights reserved. See [LICENSE](LICENSE). The code is published for review and
demonstration; no reuse licence is granted.
