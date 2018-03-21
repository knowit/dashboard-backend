# -*- coding: utf-8 -*-


import flask
import requests
import yaml
from werkzeug.contrib.cache import SimpleCache

app = flask.Flask(__name__)

cache = SimpleCache()

_SECRET_PROP_OSLOBYSYKKEL_API_TOKEN = 'oslobysykkel_api_token'


def get_from_cache(key, function, cache_timeout=10):
    if cache.has(key):
        return cache.get(key)
    else:
        content = function()
        cache.set(key, content, timeout=cache_timeout)
        return content


def read_secrets_file():
    with open('secrets.yaml') as f:
        content = yaml.load(f)
    assert _SECRET_PROP_OSLOBYSYKKEL_API_TOKEN in content
    return content


def dict_to_response_with_cors(data):
    response = flask.jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/oslobysykkel', methods=['GET'])
def oslobysykkel_status():
    def get_status():
        url = 'https://oslobysykkel.no/api/v1/stations/availability'
        headers = {'Client-Identifier': secrets[_SECRET_PROP_OSLOBYSYKKEL_API_TOKEN]}
        return requests.get(url, headers=headers).json()

    data = get_from_cache('oslobysykkel', get_status)
    return dict_to_response_with_cors(data)


@app.route('/meetingrooms', methods=['GET'])
def meetingrooms():
    data = get_from_cache('meetingrooms', lambda: requests.get('http://10.205.0.5:4422/rooms').json())
    return dict_to_response_with_cors(data)


@app.route('/kantinemeny', methods=['GET'])
def kantinemeny():
    data = get_from_cache('kantinemeny', lambda: requests.get(
        'https://us-central1-knowit-cloud-9b7de.cloudfunctions.net/getMenuForDay').json(), cache_timeout=60 * 10)
    return dict_to_response_with_cors(data)


if __name__ == '__main__':
    secrets = read_secrets_file()
    # app.debug = True
    app.run(port=8000)
