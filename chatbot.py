import json
import os
import pandas as pd

from flask import Flask
from flask import request
from flask import make_response
from sqlalchemy import create_engine

# Flask app should start in global layout
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):               
    if req.get("queryResult").get("action") != 'Course':
        return {}
    result = req.get("queryResult")
    usersay = result.get("queryText")
    parameter = result.get("parameters")
        
    fulfillmentText = ''
    if parameter.get("teacher"):
        data = pd.read_sql('select * from teacher where name = ?',con=engine,params=[usersay[:-2]])
        for i in data.index:
            fulfillmentText += '【'
            for j in data.loc[i]:
                fulfillmentText += (str(j) + '\n')
                fulfillmentText += '/'
            fulfillmentText += '】'

    if parameter.get("course"):
        data = pd.read_sql('select * from course where co_name = ?',con=engine,params=[usersay[:-2]])
        for i in data.index:
            fulfillmentText += '【'
            for j in data.loc[i]:
                fulfillmentText += str(j) + '   \n'
                fulfillmentText += '/'
            fulfillmentText += '】'

    if parameter.get("comment"):
        data = pd.read_sql('select * from comment where name = ?',con=engine,params=[usersay[0:3]])
        for i in data.index:
            fulfillmentText += '【'
            for j in data.loc[i]:
                fulfillmentText += str(j)
                fulfillmentText += '/'

            fulfillmentText += '】'
    print("Response:")
    print(fulfillmentText)
    # 回傳
    return {
        "fulfillmentText": fulfillmentText,
        "fulfillmentText": fulfillmentText,
        # "payload": {},
        # "outputContexts": [],
        "source": "agent"
    }


if __name__ == "__main__":
    engine = create_engine('sqlite:///comment.db')
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
