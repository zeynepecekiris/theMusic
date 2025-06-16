from flask import Flask, render_template
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get Strapi configuration from environment variables
STRAPI_URL = os.getenv('STRAPI_URL')
STRAPI_TOKEN = os.getenv('STRAPI_TOKEN')

@app.route("/")
def home():
    url = f"{STRAPI_URL}/api/isims"
    headers = {
        'Authorization': f'Bearer {STRAPI_TOKEN}'
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        print(">> Gelen veri:", data)  
        menuler = [item for item in data.get("data", [])]

        return render_template("index.html", menuler=menuler)
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
        return render_template("index.html", menuler=[])


@app.route("/menu")
def menu():
    url = f"{STRAPI_URL}/api/isims"
    headers = {
        'Authorization': f'Bearer {STRAPI_TOKEN}'
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        print(">> Gelen veri:", data)  
        menuler = [item["attributes"] for item in data.get("data", [])]

        return render_template("menu.html", menuler=menuler)
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
        return render_template("menu.html", menuler=[])

if __name__ == "__main__":
    app.run(debug=True, port=5008
            )
