from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template('index.html')

@app.route("/company/<int:cid>")
def show_company(cid):
    return "company tree of %d" % cid


if __name__ == "__main__":
    app.debug = True
    app.run()

