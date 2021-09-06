from flask import Flask, render_template
import requests
import config
import os
from PIL import Image, ImageDraw, ImageFont
import datetime
from random import randint
import io
import base64

YODA_URL = "https://api.funtranslations.com/translate/yoda.json"
KANYE_URL = "https://api.kanye.rest/"
YODA_API_KEY = "O_PZYqJ_ymGYQ2fqCGGS5QeF"
YODA_HEADERS = {'X-FunTranslations-Api-Secret': YODA_API_KEY}
TRUMP_URL = "https://api.tronalddump.io/random/quote"

TRUMP_HEADER = {'Accept': 'application/hal+json'}



# ------------- Setup Flask app -----------------------------#

app = Flask(__name__)
if not config.SECRET_KEY:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
else:
    app.config['SECRET_KEY'] = config.SECRET_KEY



def get_k_quote():
    with requests.get(url=KANYE_URL) as response:
        response.raise_for_status()
        return response.json()["quote"]


def get_y_quote(k_quote):

    yoda_params = {"text": k_quote}

    with requests.get(YODA_URL, params=yoda_params, headers=YODA_HEADERS) as response:
        response.raise_for_status()
        y_quote = response.json()["contents"]["translated"]
        return y_quote



def draw_meme(y_quote):
    temp_no = randint(1, 3)
    print(temp_no)
    q1 = None
    with Image.open(f"kanyodtemp{temp_no}.jpeg") as base:
        if len(y_quote) <= 30:
            fnt = ImageFont.truetype("impact.ttf", 60)
        elif len(y_quote) <= 45:
            fnt = ImageFont.truetype("impact.ttf", 50)
        elif len(y_quote) > 45:
            fnt = ImageFont.truetype("impact.ttf", 40)
            q_list = y_quote.split(",")
            q1 = q_list[0] + ","
            q2 = q_list[1]
            if len(q1) > 50 or len(q2) > 50:
                fnt = ImageFont.truetype("impact.ttf", 30)
        if q1:
            d1 = ImageDraw.Draw(base)
            d1.text((500, 100), text=q1, fill=(255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0), font=fnt, align="center", anchor="ms")
            d2 = ImageDraw.Draw(base)
            d2.text((500, 600), text=q2, fill=(255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0), font=fnt, align="center", anchor="ms")

        else:
            d = ImageDraw.Draw(base)
            d.text((500, 100), text=y_quote, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0), font=fnt, align="center", anchor="ms")
        data = io.BytesIO()
        base.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        return encoded_img_data


# for i in range(10):
#     k_quote = get_k_quote()
#     y_quote = get_y_quote(k_quote)
#
#     while "," not in y_quote or len(y_quote) > 90:
#         k_quote = get_k_quote()
#         y_quote = get_y_quote(k_quote)
#
#     draw_meme(y_quote, i)

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

    k_quote = get_k_quote()
    y_quote = get_y_quote(k_quote)

    while "," not in y_quote or len(y_quote) > 110:
        k_quote = get_k_quote()
        y_quote = get_y_quote(k_quote)

    img_data = draw_meme(y_quote)

    return render_template("index.html", img_data=img_data.decode('utf-8'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)