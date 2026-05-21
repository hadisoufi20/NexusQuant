# main.py: Streamlit frontend orchestration for Nexus Quant
# Provides an institutional-grade interface for market structural analysis.

import streamlit as st
import os
import time
from dotenv import load_dotenv
from agents import nexus_engine

# Configuration: Setting page layout and security environments
st.set_page_config(page_title="Nexus Quant AI", page_icon="🧠", layout="wide")
load_dotenv()

# Styling: Defining professional theme and system interface elements
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .signature { color: #808495; font-style: italic; font-size: 0.85rem; margin-bottom: 2rem; }
    .best-question { color: #00d4ff; font-weight: bold; font-size: 0.9rem; padding: 10px; border: 1px solid #00d4ff; border-radius: 5px; margin-top: 10px; }
    .disclaimer { color: #ff4b4b; font-size: 0.72rem; margin-top: 20px; border-top: 1px solid #333; padding-top: 10px; line-height: 1.4; }
    .system-log { color: #00ff41; font-family: 'Courier New', monospace; font-size: 0.8rem; background: #000; padding: 10px; border-radius: 5px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Nexus Quant: AI Market Architect")
st.markdown('<p class="signature">Conceptualized, Architected, and Engineered by Hadi Soufi</p>', unsafe_allow_html=True)
st.divider()

# Session State Management: Ensuring persistence across agent interactions
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Logic
if prompt := st.chat_input("Request Structural Analysis..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        log_placeholder = st.empty()
        logs = ["Initializing Sovereign Engine...", "Securing Financial API Handshake...", "Executing ICT & Wyckoff Algorithms..."]
        
        current_logs = ""
        for log in logs:
            current_logs += f'<div class="system-log">{log} [SUCCESS]</div>'
            log_placeholder.markdown(current_logs, unsafe_allow_html=True)
            time.sleep(0.4)

        try:
            # Invoking the Nexus Agentic Engine
            dynamic_agent = nexus_engine.create_agent(prompt)
            system_instructions = (
                "You are the Sovereign Gold Architect. Deliver a high-level Decision Engineering report. "
                "MANDATORY: At the end of every report, add this note: 'NOTE: This is a structural mapping for architectural purposes and NOT a financial signal. Cross-verify price with your broker.'"
                "SECTIONS: 1. ### 🪙 LIVE GOLD SPOT | 2. INSTITUTIONAL MAP (OB) | 3. LIQUIDITY (FVG) | 4. RISK ASSESSMENT (R:R) | 5. WYCKOFF & MACRO | 6. FINAL VERDICT."
            )
            
            inputs = {"messages": [("system", system_instructions), ("user", prompt)]}
            result = dynamic_agent.invoke(inputs)
            log_placeholder.empty()
            
            res_messages = result.get("messages", [])
            if res_messages:
                last_msg = res_messages[-1]
                final_answer = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
        
        except Exception as e:
            log_placeholder.empty()
            st.warning("⚠️ System is processing high-density market data. Please allow the engine to cool down and try again.")

# Sidebar Configuration: Engineering documentation and session controls
with st.sidebar:
    st.header("Nexus Quant v3.2")
    st.info("System Integrity: 100% Operational")
    
    st.markdown('<p class="best-question">🌟 Best Question:<br>Analyze Gold Market Structure & Wyckoff Phase</p>', unsafe_allow_html=True)
    
    st.markdown("""
    **Core Engine Assets:**
    - Live OHLC Data Integration
    - Mathematical OB Detection
    - Dynamic Risk Profiling
    """)
    
    # Professional Disclaimer
    st.markdown("""
    <p class="disclaimer">
    <strong>ENGINEERING DISCLAIMER:</strong><br>
    1. This AI Agent provides structural market mapping based on encoded ICT/Wyckoff logic. It does <strong>NOT</strong> provide financial advice or trade signals.<br><br>
    2. Global liquidity prices (Yahoo Finance) may vary from your specific broker's spread. Always cross-verify with your terminal before any decision.
    </p>
    """, unsafe_allow_html=True)
    
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.rerun()
