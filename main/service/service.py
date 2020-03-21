import os
import pandas as pd
from flask import Flask, render_template
from flask import request, Blueprint
from flask.json import jsonify

from main.service.es_service import ElasticClient

service_bp = Blueprint("service_bp", __name__)

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

es_service = ElasticClient()


@app.route('/', methods=('GET', 'POST'))
def search():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def response():
    query_string = request.form.get("search")

    r = es_service.free_text_search(query_string, start=0, size=10)
    result = [
        {
            # "id": hit.index,
            "text": hit.description,
            "source": hit.source,
            "is_true": hit.is_true
        }
        for hit in r
    ]

    if len(result) > 0:
        result = pd.DataFrame(result)
    else:
        result = pd.DataFrame(columns=["text", "source", "is_true"])

    true_result = result.loc[result.is_true == 'TRUE'][["text", "source"]]
    true_result.columns = ["Informacja prawdziwa", "Źródło"]

    false_result = result.loc[result.is_true == 'FALSE'][["text"]]
    false_result.columns = ["Fałsz"]

    return render_template('index.html', tables=[true_result.to_html(classes='res_tab'), false_result.to_html(classes='res_tab_false')],
                           titles=['na', 'Prawda', "Fałsz"])

