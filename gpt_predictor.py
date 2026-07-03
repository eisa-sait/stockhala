from openai import OpenAI

client = OpenAI(api_key="sk-...yK0A")


def predict_best_stock(results):
    prompt = f"""
    You are an expert stock analyst.

    Here are shortlisted stocks:

    {results}

    Analyze them using:
    - Technicals
    - Risk
    - Fundamentals
    - Sentiment
    - Price potential

    Pick ONE stock with the highest probability of upside in the next 3-6 months.

    Return:
    1. Best stock
    2. Why
    3. Key risks
    4. Estimated upside %
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
