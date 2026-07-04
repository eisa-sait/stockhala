import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def explain_stock(stock_data):
    prompt = f"""
    Analyze this stock:

    Ticker: {stock_data['Ticker']}
    Risk: {stock_data['Risk %']}
    Confidence: {stock_data['Confidence %']}
    Signal: {stock_data['Signal']}
    Sentiment: {stock_data['Sentiment']}
    P/E: {stock_data['P/E']}
    ROE: {stock_data['ROE']}
    Debt Ratio: {stock_data['Debt Ratio']}
    Dividend Yield: {stock_data['Dividend Yield']}
    Current Price: {stock_data['Current Price']}
    Target Price: {stock_data['Target Price']}

    Explain:
    1. Why this stock is ranked high
    2. Short-term view
    3. Long-term view
    4. Key risks
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq Error: {str(e)}"
