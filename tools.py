from langchain_core.tools import tool
import yfinance as yf
import pandas as pd

@tool
def get_gold_architect_data(symbol: str):
    """Macro Tool: Fetches live financial data for Gold, DXY, and Bond Yields."""
    try:
        gold = yf.Ticker("GC=F").history(period="5d")
        curr_price = gold['Close'].iloc[-1]
        
        gold_long = yf.Ticker("GC=F").history(period="20d")
        atr = (gold_long['High'] - gold_long['Low']).rolling(window=14).mean().iloc[-1]
        
        dxy = yf.Ticker("DX-Y.NYB").history(period="2d")
        tnx = yf.Ticker("^TNX").history(period="2d")

        return (f"SPOT: ${curr_price:.2f} | ATR: {atr:.2f}\n"
                f"DXY: {dxy['Close'].iloc[-1]:.2f} | US10Y: {tnx['Close'].iloc[-1]:.2f}%")
    except Exception as e:
        return f"Macro Error: Data acquisition failed."

@tool
def get_wyckoff_structure(symbol: str):
    """Advanced Tool: ICT & Wyckoff structural analysis engine."""
    try:
        data = yf.Ticker("GC=F").history(period="60d", interval="4h")
        if len(data) < 15: return "Insufficient data for structural mapping."
        
        current_price = data['Close'].iloc[-1]
        bullish_fvgs, bearish_fvgs = [], []
        
        for i in range(2, len(data)):
            if data['Low'].iloc[i-2] > data['High'].iloc[i]:
                bearish_fvgs.append(f"{data['High'].iloc[i]:.1f}-{data['Low'].iloc[i-2]:.1f}")
            elif data['High'].iloc[i-2] < data['Low'].iloc[i]:
                bullish_fvgs.append(f"{data['High'].iloc[i-2]:.1f}-{data['Low'].iloc[i]:.1f}")
        
        bull_ob, bear_ob = 0, 0
        for i in range(1, len(data)-1):
            if (data['Close'].iloc[i+1] - data['Open'].iloc[i+1]) > abs(data['Open'].iloc[i]-data['Close'].iloc[i])*2:
                bull_ob = data['High'].iloc[i]
            elif (data['Close'].iloc[i+1] - data['Open'].iloc[i+1]) < -abs(data['Open'].iloc[i]-data['Close'].iloc[i])*2:
                bear_ob = data['Low'].iloc[i]

        return (f"PRC: {current_price:.1f} | OB_S: {bear_ob:.1f} | OB_D: {bull_ob:.1f}\n"
                f"FVG_U: {bearish_fvgs[-1] if bearish_fvgs else 'N/A'}\n"
                f"FVG_L: {bullish_fvgs[-1] if bullish_fvgs else 'N/A'}")
    except Exception as e:
        return "Structure Error: Engine recalibrating."

tools_list = [get_gold_architect_data, get_wyckoff_structure]
