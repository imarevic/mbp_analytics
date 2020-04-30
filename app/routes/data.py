from flask_cors import CORS
from flask import jsonify
from flask import (
    Blueprint, request
)

bp = Blueprint('data', __name__, url_prefix='/data')
CORS(bp)

# data index endpoint
@bp.route('/', methods=['GET'])
def data_endpoint():
    # return that data source is ok
    return "Status: OK: This is the json datasource for mbp-analytics app"

# data search endpoint
@bp.route('/search', methods=['POST'])
def data_search():
    # return data table titles
    return jsonify(['Info Data', 'Friends Data', 'Profile Data', 'LK Data' ])

# data query endpoint
# post request has following content:
# 'targets': [{'target': 'series name', 'refId': 'A', 'type': 'table'}]
# so we will check what type of data is sent (table vs. time series)
# we only need table type data so time series response is not implemented
@bp.route('/query', methods=['POST'])
def data_query():
    # check for table type
    if request.json['targets'][0]['type'] == 'table':
        series = request.json['targets'][0]['target']
        # add data to body
        bodies = {'Info Data': [{
        "columns":[
          {"text":"Time","type":"time"},
          {"text":"Country","type":"string"},
          {"text":"Number","type":"number"}
        ],
        "rows":[
          [1234567,"SE",123],
          [1234567,"DE",231],
          [1234567,"US",321]
        ],
        "type":"table"
        }], 'Friends Data': [{
        "columns":[
          {"text":"Time","type":"time"},
          {"text":"Country","type":"string"},
          {"text":"Number","type":"number"}
        ],
        "rows":[
          [1234567,"BE",123],
          [1234567,"GE",231],
          [1234567,"PS",321]
        ],
        "type":"table"
        }]}

        # create response object and return it
        return jsonify(bodies[series])
