from flask import request, Blueprint, Flask
from main.service.es_service import ElasticClient
from flask.json import jsonify


service_bp = Blueprint("service_bp", __name__)

app = Flask(__name__)
es_service = ElasticClient()


@app.route("/api/findnews", methods=["POST"])
def similarity_measure() -> str:

    request_dict = request.get_json()
    start = request_dict["from"]
    size = request_dict["size"]

    query_string = request_dict["text"]

    r = es_service.free_text_search(query_string, start=start, size=size)
    result = [
        {
            "id": hit.index,
            "text": hit.description
        }
        for hit in r
    ]

    return jsonify(result)