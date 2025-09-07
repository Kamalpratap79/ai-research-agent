import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv(""))

def summarize_content(contents, summary_type="bullet"):
    texts = [item.get('text', '') for item in contents]
    prompt = f"Summarize the following content in {summary_type} format:\n" + "\n".join(texts)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
