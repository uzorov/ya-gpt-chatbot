import requests
from requests import Response
import os
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

apikey = os.getenv("APIKEY")
sa_id = os.getenv("SERVICEACID")


headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Api-Key {apikey}'
}


def send_message(message: str) -> Response:
    data = {
        "modelUri": f"gpt://{sa_id}/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Отвечай как можно более кратко"
            },
            {
                "role": "user",
                "text": message
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    return response
