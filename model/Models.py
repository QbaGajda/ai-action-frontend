import requests
import json


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def healthcheck(self):
        """Sprawdzanie statusu API"""
        try:
            response = requests.get(f"{self.base_url}/healthcheck")
            if response.status_code == 200:
                return "API działa poprawnie!"
            else:
                return f"Błąd: {response.status_code}"
        except Exception as e:
            return f"Problem z połączeniem: {str(e)}"

    def generate_text(self, prompt, max_tokens=2000, temperature=0.7):
        """Generowanie tekstu za pomocą GPT-4 (POST)"""
        url = f"{self.base_url}/openai/generate"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                return response.json().get("response", "Brak odpowiedzi")
            else:
                return f"Błąd: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Problem z połączeniem: {str(e)}"

    def generate_groq_text(self, prompt, max_tokens=200, temperature=0.7):
        """Generowanie tekstu za pomocą Groq (POST)"""
        url = f"{self.base_url}/groq/generate"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                return response.json().get("response", "Brak odpowiedzi")
            else:
                return f"Błąd: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Problem z połączeniem: {str(e)}"