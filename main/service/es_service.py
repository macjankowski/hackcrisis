from main.elastic.elasticsearch_client import ElasticsearchClientPS


class ElasticClient:

    @staticmethod
    def free_text_search(text, start=0, size=10):
        elastic_client = ElasticsearchClientPS.create_from_config("config.ini")
        r = elastic_client.free_search(
            text, start=start, size=size
        )
        return r
