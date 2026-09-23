# ADR-0002: Groq / llama-3.1-8b-instant as the inference endpoint

- **Status:** accepted
- **Date:** 2026-05-21

## Context

The agent does routing and narration, not heavy reasoning. Structural analysis is already computed in code.
Interactive use requires a response fast enough to keep the UI usable.

## Decision

Use `ChatGroq` with `llama-3.1-8b-instant` as the default model.

## Consequences

- Low latency keeps the Streamlit interaction responsive.
- A small model is adequate because the hard part (measurement) is deterministic code.
- The model is a configuration value (`model_name`), so it can be swapped without touching the graph.

## Alternatives considered

- **Larger hosted models** — rejected for this workload: more latency and cost for routing decisions.
- **Local inference** — rejected: deployment weight for a research tool.
