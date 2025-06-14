from flask import Flask, render_template
import requests


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    url = "http://localhost:1337/api/isims"
    response = requests.get(url)
    data = response.json()
    
    print(">> Gelen veri:", data)  # debug için
    menuler = [item for item in data.get("data", [])]

    return render_template("menu.html", menuler=menuler)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
