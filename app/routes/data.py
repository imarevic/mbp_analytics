from flask_cors import CORS
from flask import jsonify
from ..scraping.logic import helpers as h
import sys
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
        bodies = h.load_obj('final_data')
        # create response object and return it
        return jsonify(bodies[series])
