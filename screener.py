import yfinance as yf
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from textblob import TextBlob


def calculate_risk(data):
    volatility = data["Close"].pct_change().std() * 100
    return round(volatility, 2)


def calculate_confidence(data):
    sma = SMAIndicator(data["Close"], window=20).sma_indicator()

    if data["Close"].iloc[-1] > sma.iloc[-1]:
        return 85
    else:
        return 55


def get_signal(data):
    rsi = RSIIndicator(data["Close"], window=14).rsi()
    macd = MACD(data["Close"])

    latest_rsi = rsi.iloc[-1]
    latest_macd = macd.macd().iloc[-1]
    latest_signal = macd.macd_signal().iloc[-1]

    if latest_rsi < 30 and latest_macd > latest_signal:
        return "BUY"
    elif latest_rsi > 70 and latest_macd < latest_signal:
        return "SELL"
    else:
        return "HOLD"


def get_news_sentiment(stock):
    news = stock.news

    if not news:
        return "Neutral", 50

    scores = []

    for item in news[:5]:
        title = item.get("title", "")
        polarity = TextBlob(title).sentiment.polarity
        scores.append(polarity)

    avg_score = sum(scores) / len(scores)

    if avg_score > 0.2:
        return "Bullish", 80
    elif avg_score < -0.2:
        return "Bearish", 20
    else:
        return "Neutral", 50


def analyze_stock(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")

    if hist.empty:
        return None

    risk = calculate_risk(hist)
    confidence = calculate_confidence(hist)
    signal = get_signal(hist)
    sentiment, sentiment_score = get_news_sentiment(stock)

    info = stock.info

    pe_ratio = info.get("trailingPE", 0)
    roe = info.get("returnOnEquity", 0)
    debt_ratio = info.get("debtToEquity", 0)
    dividend_yield = info.get("dividendYield", 0)

    fundamental_score = 0

    if pe_ratio and pe_ratio < 25:
        fundamental_score += 20

    if roe and roe > 0.15:
        fundamental_score += 20

    if debt_ratio and debt_ratio < 50:
        fundamental_score += 20

    if dividend_yield and dividend_yield > 0.02:
        fundamental_score += 20

    current_price = hist["Close"].iloc[-1]
    stop_loss = round(current_price * 0.95, 2)
    target_price = round(current_price * 1.10, 2)

    return {
        "ticker": ticker,
        "risk": risk,
        "confidence": confidence,
        "signal": signal,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "pe_ratio": pe_ratio,
        "roe": roe,
        "debt_ratio": debt_ratio,
        "dividend_yield": dividend_yield,
        "fundamental_score": fundamental_score,
        "current_price": current_price,
        "stop_loss": stop_loss,
        "target_price": target_price,
        "info": info,
        "history": hist
    }