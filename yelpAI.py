from flask import Flask
from flask import request
from flask import make_response
import os

import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("webhook called")
    req = request.get_json(silent=True, force=True)

    print(json.dumps(req, indent=4))

    res = {
        "speech": "lots of option bro",
        "displayText": "lots of options bro",
        "source": "sirishs-stuff"
    }

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("starting app on post %d" %port)
    app.run(debug=False, port=port, host='0.0.0.0')