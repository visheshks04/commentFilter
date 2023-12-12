from flask import Flask, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

COMMENTS_API_URL = 'https://app.ylytic.com/ylytic/test'


def filter_comments(comments, filters):
    filtered_comments = comments

    search_author = filters.get('search_author')
    at_from = filters.get('at_from')
    at_to = filters.get('at_to')
    like_from = filters.get('like_from')
    like_to = filters.get('like_to')
    reply_from = filters.get('reply_from')
    reply_to = filters.get('reply_to')
    search_text = filters.get('search_text')

    if search_author:
        filtered_comments = [comment for comment in filtered_comments if
                             search_author.lower() in comment.get('author', '').lower()]

    if at_from:
        at_from_date_object = datetime.strptime(at_from, "%d-%m-%Y")
        filtered_comments = [comment for comment in filtered_comments if datetime.strptime(comment.get('at'), "%a, %d %b %Y %H:%M:%S %Z") >= at_from_date_object]

    if at_to:
        at_to_date_object = datetime.strptime(at_to, "%d-%m-%Y")
        filtered_comments = [comment for comment in filtered_comments if datetime.strptime(comment.get('at'), "%a, %d %b %Y %H:%M:%S %Z") <= at_to_date_object]

    if like_from:
        filtered_comments = [comment for comment in filtered_comments if
                             comment.get('like') and comment.get('like') >= int(like_from)]

    if like_to:
        filtered_comments = [comment for comment in filtered_comments if
                             comment.get('like') and comment.get('like') <= int(like_to)]

    if reply_from:
        filtered_comments = [comment for comment in filtered_comments if
                             comment.get('reply') and comment.get('reply') >= int(reply_from)]

    if reply_to:
        filtered_comments = [comment for comment in filtered_comments if
                             comment.get('reply') and comment.get('reply') <= int(reply_to)]

    if search_text:
        filtered_comments = [comment for comment in filtered_comments if
                             search_text.lower() in comment.get('text', '').lower()]

    return filtered_comments


@app.route('/search', methods=['GET'])
def search_comments():
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    filters = {
        'search_author': search_author,
        'at_from': at_from,
        'at_to': at_to,
        'like_from': like_from,
        'like_to': like_to,
        'reply_from': reply_from,
        'reply_to': reply_to,
        'search_text': search_text
    }

    response = requests.get(COMMENTS_API_URL)

    if response.status_code == 200:
        comments = response.json()['comments']

        filtered_comments = filter_comments(comments, filters)

        return jsonify(filtered_comments)
    else:
        return jsonify({'message': 'Failed to fetch comments'}), 500


if __name__ == '__main__':
    app.run(debug=True)
