from flask import Flask, render_template
import requests
import config
import os
from PIL import Image, ImageDraw, ImageFont
import datetime
from random import randint
import io
import base64
from memehandler import MemeHandler


# ------------- Setup Flask app -----------------------------#

app = Flask(__name__)
if not config.SECRET_KEY:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    font = "/app/Impact.ttf"
else:
    app.config['SECRET_KEY'] = config.SECRET_KEY
    font = "Impact.ttf"

# -------------- Plans for a possible Trump version -----------------------#
# with requests.get(url=TRUMP_URL, headers=TRUMP_HEADER) as response:
#     response.raise_for_status()
#     print(response.json())
#     t_quote = response.json()["value"]
#
# yoda_params = {"text": t_quote}
#
# with requests.get(YODA_URL, params=yoda_params, headers=YODA_HEADERS) as response:
#     response.raise_for_status()
#     print(response.json())
#

@app.context_processor
def inject_now():
    return {'current_year': datetime.date.today().strftime("%Y")}

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/meme", methods=["GET", "POST"])
def meme():
    meme = MemeHandler()

    return render_template("index.html", img_data=meme.img_data.decode('utf-8'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)