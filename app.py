from flask import Flask, request
from flask_cors import CORS, cross_origin
import classify as AllSkyAI
import json

app = Flask(__name__)
cors = CORS(app)


@app.route('/classifylive', methods=['GET'])
def predict_bw():
    color_mode = request.args.get('type')
    if color_mode == 'bw':
        result = AllSkyAI.classify_bw_live()
        return result
    elif color_mode == 'color':
        result = AllSkyAI.classify_color_live()
        return result
    else:
        return json.dumps({"Error": "Please specify a color mode - 'classify?type=bw' or 'classify?type=color'"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
