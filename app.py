import streamlit as st
import pandas as pd
from screener import analyze_stock
from shariah import is_shariah_compliant
from ai_advisor import explain_stock
from gpt_predictor import predict_best_stock

st.title("StockHalal V11")

# Inputs
country = st.selectbox("Select Market", ["India", "US"])
risk_limit = st.slider("Risk Level", 0, 100, 60)
confidence_limit = st.slider("Confidence Level", 0, 100, 80)

investment_amount = st.number_input(
    "Enter Investment Amount (₹/$)",
    min_value=1000,
    value=10000
)

watchlist_stock = st.text_input(
    "Enter stock for alert (example: ITC.NS)"
)

# Load stocks
if country == "India":
    stock_data = pd.read_csv("stocks.csv")
    stocks = stock_data["Ticker"].tolist()
else:
    stocks = [
        "AAPL",
        "MSFT",
        "TSLA",
        "NVDA",
        "GOOGL"
    ]

# Main Scanner
if st.button("Scan Stocks"):
    results = []

    for ticker in stocks:
        result = analyze_stock(ticker)

        if result:
            shariah = is_shariah_compliant(result["info"])

            if not shariah:
                continue

            if (
                result["risk"] <= risk_limit
                and result["confidence"] >= confidence_limit
                and result["current_price"] <= investment_amount
            ):

                score = (
                    result["confidence"]
                    - result["risk"]
                    + (20 if result["signal"] == "BUY" else 0)
                    + result["sentiment_score"]
                    + result["fundamental_score"]
                )

                results.append({
                    "Ticker": ticker,
                    "Risk %": result["risk"],
                    "Confidence %": result["confidence"],
                    "Signal": result["signal"],
                    "Sentiment": result["sentiment"],
                    "P/E": result["pe_ratio"],
                    "ROE": result["roe"],
                    "Debt Ratio": result["debt_ratio"],
                    "Dividend Yield": result["dividend_yield"],
                    "Fundamental Score": result["fundamental_score"],
                    "Current Price": result["current_price"],
                    "Stop Loss": result["stop_loss"],
                    "Target Price": result["target_price"],
                    "Shariah": "Yes",
                    "Score": score,
                    "History": result["history"]
                })

    if len(results) > 0:
        # Sort by score
        results = sorted(results, key=lambda x: x["Score"], reverse=True)

        best_stock = results[0]

        # Best stock display
        st.success(
            f"🏆 Best Stock Today: {best_stock['Ticker']} | "
            f"Buy: {round(best_stock['Current Price'], 2)} | "
            f"SL: {best_stock['Stop Loss']} | "
            f"Target: {best_stock['Target Price']} | "
            f"Signal: {best_stock['Signal']} | "
            f"Sentiment: {best_stock['Sentiment']}"
        )

        # Chart
        st.subheader(f"Price Chart: {best_stock['Ticker']}")
        st.line_chart(best_stock["History"]["Close"])

        # AI Stock Explanation
        st.subheader("AI Analysis")

        if st.button("Explain Best Stock"):
            ai_response = explain_stock(best_stock)
            st.write(ai_response)

        # GPT Conviction Pick
        st.subheader("GPT Conviction Pick")

        if st.button("Get GPT Prediction"):
            gpt_pick = predict_best_stock(results[:5])
            st.write(gpt_pick)

        # Portfolio Allocation
        st.subheader("Portfolio Allocation")

        top_stocks = results[:5]
        total_score = sum(stock["Score"] for stock in top_stocks)

        allocation_data = []

        for stock in top_stocks:
            allocation = (
                stock["Score"] / total_score
            ) * investment_amount

            quantity = int(allocation // stock["Current Price"])

            allocation_data.append({
                "Ticker": stock["Ticker"],
                "Allocate": round(allocation, 2),
                "Shares": quantity
            })

        st.table(allocation_data)

        # Full Results
        st.subheader("Full Ranked List")
        st.table(results)

    else:
        st.write("No matching affordable Shariah-compliant stocks found.")

# Watchlist Alerts
if watchlist_stock:
    watch_result = analyze_stock(watchlist_stock)

    if watch_result:
        st.subheader("Watchlist Alert")

        if watch_result["signal"] == "BUY":
            st.error(
                f"🚨 BUY ALERT: {watchlist_stock} | "
                f"Buy: {round(watch_result['current_price'], 2)} | "
                f"SL: {watch_result['stop_loss']} | "
                f"Target: {watch_result['target_price']}"
            )
        else:
            st.info(
                f"{watchlist_stock} is currently {watch_result['signal']}"
            )
