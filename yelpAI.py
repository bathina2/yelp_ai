from flask import Flask
from flask import request
from flask import make_response
import os
import requests

import json

YELP_API_KEY = 'Bearer gkzhK-V_tETl4oGoJxj9m1O6wPVigFP1oAHcDF2di22wCxeE_22X6jYJ09nn2vGEpK5mE63-Kjsx4X8ysO7b2tJ4GXwmYeVahkoy-OiNDAbgNM7A_GXwaqDk9T59WnYx'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("webhook called")
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    res = process_request(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def process_request(req):
    if req.get("result").get("action") == "find-places-to-eat":
        return find_places_to_eat(req)
    else:
        return {}


def find_places_to_eat(req):
    city = req.get("result").get("parameters").get("geo-city")
    if city:
        if not city:
            return {}
        payload = {'location': city,
                   'radius': 8000,
                   'categories': 'food',
                   'sort_by': 'rating',
                   'limit': 10}
        response = business_search(payload)
        #print(response)
        if response:
            speech_str = "The top ten place to eat in " + city + " are: "
            businesses = response.get('businesses')
            for business in businesses:
                speech_str = speech_str + " " + business['name'] + ","
            speech_str = speech_str[:-1]
            return make_speech_response(speech_str)
        else:
            return {}
    else:
        return {}


def make_speech_response(speech_str):
    return {
        "speech": speech_str,
        "displayText": speech_str,
        "source": "yelp-ai"
    }


def business_search(payload):
    headers = {'Authorization': YELP_API_KEY}
    r = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=payload)
    if r.status_code != 200:
        return {}
    else:
        return r.json()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("starting app on post %d" %port)
    app.run(debug=False, port=port, host='0.0.0.0')