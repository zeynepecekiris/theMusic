from flask import Flask, render_template
import requests


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    # Strapi Cloud URL'sini buraya ekleyin
    url = "https://your-project-name.strapi.cloud/api/isims"
    headers = {
        'Authorization': 'Bearer your-strapi-cloud-token'
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        print(">> Gelen veri:", data)  
        menuler = [item for item in data.get("data", [])]

        return render_template("menu.html", menuler=menuler)
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
        return render_template("menu.html", menuler=[])

if __name__ == "__main__":
    app.run(debug=True, port=5006)
