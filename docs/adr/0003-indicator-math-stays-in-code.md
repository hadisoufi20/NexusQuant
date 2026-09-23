# ADR-0003: Indicator math stays in code; the model only routes and explains

- **Status:** accepted
- **Date:** 2026-05-21

## Context

An LLM can be asked to "compute" an ATR or spot a Fair Value Gap. Doing so makes the output
non-reproducible: the same market data can yield different numbers between runs.

## Decision

Every number is produced by deterministic Python in `tools.py`. The model's only powers are selecting a
tool and describing its output.

## Consequences

- Identical inputs produce identical measurements.
- The measurements are unit-testable without any model in the loop (see `tests/test_tools.py`).
- The model cannot silently invent a level that the data does not contain.

## Alternatives considered

- **Prompt the model with raw OHLC data** — rejected: non-reproducible output and context waste.
- **Model computes, code sanity-checks** — rejected: the check would have to duplicate the computation anyway.
