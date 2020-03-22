import os
import pandas as pd
from flask import Flask, render_template
from flask import request, Blueprint
from flask.json import jsonify

from main.service.es_service import ElasticClient
from main.service.w2vec_service import Word2VecClient

service_bp = Blueprint("service_bp", __name__)

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

es_service = ElasticClient()
w2v_client = Word2VecClient('main/models/model.pickle', 'main/models/facts.pickle')


@app.route('/', methods=('GET', 'POST'))
def search():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def response():
    query_string = request.form.get("search")

    true_result, false_result = top_w2v_top_elastic(query_string)

    return render_template('index.html', tables=[true_result.to_html(classes='res_tab'), false_result.to_html(classes='res_tab_false')],
                           titles=['na', 'Prawda', "Fałsz"])


def top_w2v_top_elastic(query_string):

    true_result_w2v, false_result_w2v = only_w2v(query_string, k=50)
    true_result_elastic, false_result_elastic = only_elastic(query_string)

    true_result = pd.concat([true_result_w2v.head(5), true_result_elastic.head(5)])
    false_result = pd.concat([false_result_w2v.head(2), false_result_elastic.head(2)])

    true_result = true_result.drop_duplicates(subset=['text'])
    false_result = false_result.drop_duplicates(subset=['text'])

    true_result.columns = ["Informacja prawdziwa", "Źródło"]
    false_result.columns = ["Fałsz"]

    return true_result, false_result


def only_w2v(query_string, k=10):

    result = w2v_client.find_top_matches(query_string, k)

    true_result = result.loc[result.is_true == True][["text", "source"]]
    # true_result.columns = ["Informacja prawdziwa", "Źródło"]

    false_result = result.loc[result.is_true == False][["text"]]
    # false_result.columns = ["Fałsz"]

    return true_result, false_result


def only_elastic(query_string):

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
    # true_result.columns = ["Informacja prawdziwa", "Źródło"]

    false_result = result.loc[result.is_true == 'FALSE'][["text"]]
    # false_result.columns = ["Fałsz"]

    return true_result, false_result
