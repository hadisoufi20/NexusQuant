"""Unit tests for the Nexus Quant market-data tools.

yfinance is replaced with deterministic frames, so the structural logic
(Fair Value Gap and Order Block detection) and the error handling are
exercised without any network access.
"""
import os
import sys

import pandas as pd
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tools  # noqa: E402

COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def _frame(rows):
    return pd.DataFrame(rows, columns=COLUMNS)


class FakeTicker:
    """Minimal stand-in for yfinance.Ticker keyed by (period, interval)."""

    def __init__(self, frames):
        self._frames = frames

    def history(self, period=None, interval=None):
        if (period, interval) in self._frames:
            return self._frames[(period, interval)]
        for (p, _i), frame in self._frames.items():
            if p == period:
                return frame
        raise ValueError("no fixture data for period=%s interval=%s" % (period, interval))


class RaisingTicker:
    def history(self, *args, **kwargs):
        raise RuntimeError("data source unavailable")


def _install_tickers(monkeypatch, mapping):
    def factory(symbol):
        if symbol not in mapping:
            raise AssertionError("unexpected symbol requested: %s" % symbol)
        return mapping[symbol]

    monkeypatch.setattr(tools.yf, "Ticker", factory)


# --------------------------------------------------------------------- registry

def test_tool_registry_contract():
    names = sorted(t.name for t in tools.tools_list)
    assert names == ["get_gold_architect_data", "get_wyckoff_structure"]
    for entry in tools.tools_list:
        assert entry.description.strip(), "%s has no description" % entry.name


# ----------------------------------------------------------------- macro tool

def test_macro_tool_output_format(monkeypatch):
    gold = _frame([(100, 105, 95, 102, 10)] * 20)          # ATR = 10.00, last close = 102
    dxy = _frame([(100, 101, 99, 100.5, 1)] * 2)
    tnx = _frame([(4.1, 4.2, 4.0, 4.15, 1)] * 2)
    _install_tickers(monkeypatch, {
        "GC=F": FakeTicker({("5d", None): gold, ("20d", None): gold}),
        "DX-Y.NYB": FakeTicker({("2d", None): dxy}),
        "^TNX": FakeTicker({("2d", None): tnx}),
    })

    out = tools.get_gold_architect_data.invoke({"symbol": "GC=F"})

    assert out.startswith("SPOT: $102.00 | ATR: 10.00"), out
    assert "DXY: 100.50" in out
    assert "US10Y: 4.15%" in out


def test_macro_tool_reports_data_failure_instead_of_raising(monkeypatch):
    _install_tickers(monkeypatch, {"GC=F": RaisingTicker()})

    out = tools.get_gold_architect_data.invoke({"symbol": "GC=F"})

    assert out == "Macro Error: Data acquisition failed."


# ------------------------------------------------------------- structure tool

def _structure_frame():
    """16 bars: exactly one bullish FVG and one bull order block."""
    neutral = (100, 100.5, 99.5, 100, 1)
    rows = [neutral] * 16
    rows[0] = (100, 90, 89, 100, 1)      # makes High[0] = 90  -> bullish FVG against Low[2]
    rows[2] = (100, 100.5, 110, 100, 1)  # Low[2] = 110
    rows[3] = (100, 120, 99.5, 100, 1)   # High[3] = 120, zero body
    rows[4] = (100, 130, 99.5, 110, 1)   # +10 body -> identifies High[3] as the bull OB
    return _frame(rows)


def test_structure_tool_detects_fvg_and_order_block(monkeypatch):
    frame = _structure_frame()
    _install_tickers(monkeypatch, {"GC=F": FakeTicker({("60d", "4h"): frame})})

    out = tools.get_wyckoff_structure.invoke({"symbol": "GC=F"})
    lines = out.splitlines()

    assert lines[0] == "PRC: 100.0 | OB_S: 0.0 | OB_D: 120.0", out
    assert lines[1] == "FVG_U: N/A", out          # no bearish FVG in this series
    assert lines[2] == "FVG_L: 90.0-110.0", out   # bullish FVG = High[i-2] .. Low[i]


def test_structure_tool_rejects_short_series(monkeypatch):
    short = _frame([(100, 101, 99, 100, 1)] * 10)
    _install_tickers(monkeypatch, {"GC=F": FakeTicker({("60d", "4h"): short})})

    out = tools.get_wyckoff_structure.invoke({"symbol": "GC=F"})

    assert out == "Insufficient data for structural mapping."


def test_structure_tool_reports_failure_instead_of_raising(monkeypatch):
    _install_tickers(monkeypatch, {"GC=F": RaisingTicker()})

    out = tools.get_wyckoff_structure.invoke({"symbol": "GC=F"})

    assert out == "Structure Error: Engine recalibrating."
