from PIL import Image, ImageDraw, ImageFont
import requests
import spacy
import io
import base64
from random import randint


YODA_URL = "https://api.funtranslations.com/translate/yoda.json"
KANYE_URL = "https://api.kanye.rest/"
YODA_API_KEY = "O_PZYqJ_ymGYQ2fqCGGS5QeF"
YODA_HEADERS = {'X-FunTranslations-Api-Secret': YODA_API_KEY}
TRUMP_URL = "https://api.tronalddump.io/random/quote"

TRUMP_HEADER = {'Accept': 'application/hal+json'}
FNT = ImageFont.truetype("Impact.ttf", 80)
NLP = spacy.load("en_core_web_sm")


class MemeHandler:
    def __init__(self):
        self.k_quote = []
        self.y_quote = []
        self.t_width = 0
        self.t_height = 0
        self.img_data = None
        self.get_k_quote()
        self.get_y_quote()
        self.generate_meme()

    def get_k_quote(self):
        with requests.get(url=KANYE_URL) as response:
            response.raise_for_status()
            quote = response.json()["quote"]
            q_doc = NLP(quote)
            k_quote = list(q_doc.sents)
            if len(k_quote) > 2:
                self.get_k_quote()
            else:
                self.k_quote = k_quote

    def get_y_quote(self):
        q_list_1 = []
        for q in self.k_quote:
            q = str(q)
            print(q)
            yoda_params = {"text": q}

            with requests.get(YODA_URL, params=yoda_params, headers=YODA_HEADERS) as response:
                response.raise_for_status()
                y_quote = response.json()["contents"]["translated"]
                q_list_1.append(y_quote)
        if len(q_list_1) == 1:
            if "," not in q_list_1[0]:
                self.get_k_quote()
                self.get_y_quote()
                return
            else:
                q_list_1 = q_list_1[0].split(",")
                q_list_1 = [(q_list_1[0] + ","), q_list_1[1]]
        for quote in q_list_1:
            if len(quote) > 85:
                spaces = quote.count(" ")
                if spaces % 2 == 0:
                    spaces = int(spaces / 2)
                else:
                    spaces = int((spaces + 1) / 2)
                quote = quote.split(" ")
                self.y_quote.append(" ".join(quote[:spaces]))
                self.y_quote.append(" ".join(quote[spaces:]))
            else:
                self.y_quote.append(quote)

    def generate_meme(self):
        txt = Image.new("RGBA", (3000, 100), (0, 0, 0, 0))
        y = 50
        line_no = 1
        for line in self.y_quote:
            width, height = ImageDraw.Draw(txt).textsize(
                text=line, font=FNT,
                stroke_width=1)
            if width > self.t_width:
                self.t_width = width
                self.t_height = height
        with Image.open(f"kanyodtemp{randint(1, 3)}.jpeg").convert("RGBA") as base:
            for line in self.y_quote:
                txt = Image.new("RGBA", (3000, 100), (0, 0, 0, 0))
                d = ImageDraw.Draw(txt)
                if self.t_width >= 900:
                    d.text((1500, 50), text=line, fill=(255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0), font=FNT, align="center", anchor="mm")
                    w_diff = (3000 - self.t_width) / 2
                    new_height = int(round(100 * (900 / self.t_width), 0))
                    text = txt.crop((w_diff, 0, (self.t_width + w_diff), 100)).resize((900, new_height)).convert("RGBA")
                    base.paste(text, ((1000 - 900) // 2, y), mask=text)
                else:
                    d.text((1500, 50), text=line, fill=(255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0), font=FNT, align="center", anchor="mm")
                    w_diff = (3000 - self.t_width) / 2
                    text = txt.crop((w_diff, 0, (self.t_width + w_diff), 100)).convert("RGBA")
                    base.paste(text, ((1000 - self.t_width) // 2, y), mask=text)
                if len(self.y_quote) == 2:
                    y += 500
                else:
                    if line_no == 2:
                        y += 450
                    else:
                        y += 75
                    line_no += 1


            data = io.BytesIO()
            base.save(data, "PNG")
            self.img_data = base64.b64encode(data.getvalue())


