# agents.py: Core multi-agent orchestration logic for Nexus Quant
# This module implements stateful workflows and deterministic reasoning cycles.

import operator
import os
from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from tools import tools_list

# Define the state architecture for the Nexus Quant agentic framework
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

class NexusEngine:
    """
    Sovereign Engine for autonomous market execution.
    Handles recursive state management and deterministic reasoning cycles.
    """
    def __init__(self, model_name="llama-3.1-8b-instant"):
        self.model_name = model_name
        # API key read from environment variable (GROQ_API_KEY)
        self.llm = ChatGroq(model=model_name, groq_api_key=os.getenv("GROQ_API_KEY"))
        self.tools = {t.name: t for t in tools_list}
        self.llm_with_tools = self.llm.bind_tools(tools_list)

    def create_agent(self, user_prompt: str):
        """
        Orchestrates the multi-agent workflow based on structural requirements.
        Implements a stateful approach to recursive market analysis.
        """
        # Workflow initialization
        workflow = StateGraph(AgentState)
        
        # Add nodes for agentic reasoning
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", self._execute_tools)
        
        # Define the structural flow
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", self._should_continue, {
            "continue": "tools",
            "end": END
        })
        workflow.add_edge("tools", "agent")
        
        return workflow.compile()

    def _call_model(self, state: AgentState):
        """
        Executes the LLM reasoning cycle. 
        Analyzes the current state and determines the next systemic action.
        """
        messages = state["messages"]
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def _execute_tools(self, state: AgentState):
        """
        Tool execution layer. 
        Processes financial data tools and returns results to the state machine.
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        # Tool call identification and execution
        tool_call = last_message.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        tool_func = self.tools[tool_name]
        result = tool_func.invoke(tool_args)
        
        # Return the observation to the agentic state
        return {"messages": [HumanMessage(content=str(result), name=tool_name)]}

    def _should_continue(self, state: AgentState):
        """
        Conditional routing logic for the state machine.
        Determines if the agent needs further tool intervention.
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        if last_message.tool_calls:
            return "continue"
        return "end"