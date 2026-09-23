# ADR-0001: Use a LangGraph StateGraph for orchestration

- **Status:** accepted
- **Date:** 2026-05-21

## Context

The system needs multi-step reasoning: decide what to measure, run the measurement, then interpret the
result. Naive chaining of model calls makes the number of steps unpredictable and the failure path invisible.

## Decision

Orchestrate with an explicit LangGraph `StateGraph` containing two nodes (`agent`, `tools`) and one
conditional edge driven by `_should_continue`.

## Consequences

- The possible execution paths are finite and readable in `agents.py`.
- The transcript is append-only (`Annotated[..., operator.add]`), so the reasoning path can be replayed.
- Adding a capability means adding a node or a tool, not rewriting a prompt chain.

## Alternatives considered

- **Single prompt with all data injected** — rejected: no control over which measurement runs, and the whole data payload always consumes context.
- **Hand-written while-loop over the model** — rejected: reimplements the graph with less visibility.
