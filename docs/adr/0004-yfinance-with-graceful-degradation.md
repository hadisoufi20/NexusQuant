# ADR-0004: yfinance as the data source, with graceful degradation

- **Status:** accepted
- **Date:** 2026-05-21

## Context

The tooling needs gold futures, a dollar index and a yield series with no infrastructure or paid feed.

## Decision

Use `yfinance`, and wrap every acquisition in `try/except` that returns an explicit error string.

## Consequences

- Zero infrastructure: no API key, no vendor contract.
- Provider outages degrade the answer instead of breaking the graph.
- Spread and timestamp differences against a broker terminal are expected; the disclaimer in the UI states this.

## Alternatives considered

- **Paid market-data vendor** — rejected for a research tool: cost and onboarding for no accuracy gain here.
- **Let exceptions propagate** — rejected: one provider blip would end the whole session.
