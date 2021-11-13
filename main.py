from flask import Flask, jsonify, request

from storage import all_articles, liked_articles, unliked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask('__name__')


@app.route("/get-articles")
def get_articles():
    movie_data = {
        "url": all_articles[0][11],
        "title": all_articles[0][12],
        "text": all_articles[0][13],
        "lang": all_articles[0][14],
        "total_events": all_articles[0][15]
    }
    return jsonify({
        "data": movie_data,
        "status": "success"
    })


@app.route("/liked-articles", methods=["POST"])
def like_articles():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201


@app.route("/unliked-article", methods=["POST"])
def unlike_article():
    article = all_articles[0]
    unliked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201


@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200


@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,
                           _ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200


if __name__ == "__main__":
    app.run()
