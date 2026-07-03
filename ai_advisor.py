import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
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
    Target Price: {stock_data['Target Price']}

    Explain:
    1. Why this stock is ranked high
    2. Short-term view
    3. Long-term view
    4. Key risks
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"GPT Error: {str(e)}"
