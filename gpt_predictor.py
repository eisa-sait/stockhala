import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


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

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq Error: {str(e)}"
