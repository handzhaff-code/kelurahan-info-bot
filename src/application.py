# Library - module
from flask import Flask, jsonify, request
from storage import get_all_article, get_article, updates_articles, create_article, delete_articles_db

# Code
app = Flask(__name__)

@app.route("/api/articles", methods=["GET"])
def get_articles():
    articles = get_all_article()

    return jsonify(articles)

@app.route("/api/articles/<string:article_id>", methods=["GET"])
def get_a_article(article_id):
    article = get_article(article_id)

    if article is None:
        return jsonify({
            "success" : True,
            "message" : "Article cannot be found",
            "response" : None
        }), 404 # Return result data and status code 200,404 etc

    return jsonify({
        "success" : True,
        "message" : "Article successfuly found !",
        "response" : article
    }), 200

@app.route("/api/articles", methods=["PATCH"])
def patch_article():
    data = request.get_json()

    try:
        state = updates_articles(data)

        if state is True:
            return jsonify({
                "success" : True,
                "message" : "Data has been updated"
            }), 200 # Perfectly done
        elif state is False:
            return jsonify({
                "success" : False,
                "message" : "ID cannot be found"
            }), 404 # Client error
        
    except Exception as error:
        return jsonify({
            "success" : True,
            "message" : str(error)
        }), 500 # Server error 

@app.route("/api/articles", methods=["POST"])
def post_article():
    data = request.get_json()
    result = create_article(data)

    try:
        if result is False:
            return jsonify({
                "success" : False,
                "message" : "ID already exist"
            }), 404
        elif result is True:
            return jsonify({
                "success" : True,
                "message" : "New article succefully added"
            }), 200
    except Exception as err:
        return jsonify({
            "success" : False,
            "message" : err
        }), 500

@app.route("/api/articles/<string:article_id>", methods=["DELETE"])
def delete_article(article_id):
    result = delete_articles_db(article_id)

    try:
        if result is True:
            return jsonify({
                "success" : True,
                "message" : "Succesfully delete article"
            }), 200
        elif result is False:
            return jsonify({
                "success" : False,
                "message" : "ID cannot found, delete failed"
            }), 404
    except Exception as err:
        return jsonify({
                "success" : False,
                "message" : err
            }), 500


if __name__ == "__main__":
    app.run(debug=True)