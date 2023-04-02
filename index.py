from flask import Flask, render_template, request
import pykakasi
import bisect


class App:
    def __init__(self) -> None:
        self.kks = pykakasi.kakasi()
        self.alp = set(
            [
                *[chr(ord("a") + i) for i in range(26)],
                *[chr(ord("A") + i) for i in range(26)],
                " ",
            ]
        )
        self.vowels = (
            open("./files/vowels.txt", "r", encoding="utf-8").read().splitlines()
        )
        self.lines_original = (
            open("./files/original.txt", "r", encoding="utf-8").read().splitlines()
        )

    def get_romaji(self, text):
        result = self.kks.convert(text)
        return " ".join([item["hepburn"] for item in result])

    def get_vowels(self, text):
        vowels = set(["a", "i", "u", "e", "o", "A", "I", "U", "E", "O"])
        res = []

        for i in range(len(text)):
            t = text[i]
            if t in vowels:
                res.append(t)
            elif (t == "n" or t == "N") and (
                (
                    i != (len(text) - 1)
                    and (text[i + 1] not in vowels or text[i + 1] == "n")
                    or (i == (len(text) - 1) and t == "n")
                )
            ):
                res.append("n")
        return "".join(res)

    def search(self, text):
        romaji = self.get_vowels(self.get_romaji(text))
        left = bisect.bisect_left(self.vowels, romaji)  # 含む
        right = bisect.bisect_right(self.vowels, romaji)  # 含まない
        return self.lines_original[left:right]


app = Flask(__name__)


# ルーティング
@app.route("/")
def index():
    return render_template("index.html", items=[1, 2, 3, 4])


@app.route("/result", methods=["GET"])
def result_get():
    global rhyme_finder
    text = request.args.get("text", "")
    print("=======")
    print(text, "a")
    items = rhyme_finder.search(text)
    return render_template("result.html", text=text, items=items)


if __name__ == "__main__":
    rhyme_finder = App()
    app.run(port=8000, debug=True)
