"""Structural tests for the NexusEngine agent graph.

These build the LangGraph workflow and exercise the routing function only.
No model call and no network access happen here: the engine is constructed
with a placeholder API key and the graph is never executed.
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("GROQ_API_KEY", "placeholder-key-for-tests")

from agents import NexusEngine  # noqa: E402


class _Message:
    def __init__(self, tool_calls=None):
        self.tool_calls = tool_calls if tool_calls is not None else []


def test_engine_builds_the_expected_graph():
    graph = NexusEngine().create_agent("analyse gold market structure").get_graph()

    assert {"agent", "tools"} <= set(graph.nodes), set(graph.nodes)

    agent_targets = {edge.target for edge in graph.edges if edge.source == "agent"}
    assert agent_targets, "the agent node has no outgoing edges"
    assert any("tools" in str(target) for target in agent_targets), agent_targets

    tool_targets = {edge.target for edge in graph.edges if edge.source == "tools"}
    assert any("agent" in str(target) for target in tool_targets), tool_targets


def test_routing_continues_when_a_tool_is_requested():
    engine = NexusEngine()
    state = {"messages": [_Message([{"name": "get_gold_architect_data", "args": {"symbol": "GC=F"}}])]}
    assert engine._should_continue(state) == "continue"


def test_routing_ends_when_no_tool_is_requested():
    engine = NexusEngine()
    assert engine._should_continue({"messages": [_Message([])]}) == "end"
