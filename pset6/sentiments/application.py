from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import helpers

from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)

    name = screen_name.strip('@')

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 100)
    if tweets == None:
        return redirect(url_for("index"))

    # declare count variables
    count, positive_count, negative_count, neutral_count = 0, 0, 0, 0

    # get single tweets and count them
    for tweet in tweets:
        count += 1
        score = analyzer.analyze(tweet)
        if score > 0.0:
            positive_count += 1
        elif score < 0.0:
            negative_count += 1
        else:
            neutral_count += 1

    # get 100 percent
    positive, negative, neutral = positive_count / count * 100, negative_count / count * 100, neutral_count / count * 100

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=name)
