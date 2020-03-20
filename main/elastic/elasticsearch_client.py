import logging

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
from elasticsearch_dsl import Search
import configparser


class ElasticsearchClientPS:

    @classmethod
    def create_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        es_host = config.get("elastic", "es_host")
        es_port = config.getint("elastic", "es_port", fallback=9200)
        es_scheme = config.get("elastic", "es_scheme", fallback=None)
        es_index_name = config.get("elastic", "es_index_name")

        self.index_name = es_index_name

        instance = ElasticsearchClientPS(
            host=es_host,
            index_name=es_index_name,
            port=es_port,
            scheme=es_scheme
        )

        return instance

    def __init__(
            self,
            host,
            index_name,
            port=9200,
            username="",
            password="",
            scheme=None
    ):

        """
        :param host: host_name or ip
        :param index_name: elasticsearch index name
        :param port: by default it is 9200
        :param username:
        :param password:
        :param scheme: set this to "https" if ssl is used
        """
        self.client = Elasticsearch(hosts=[host],
                                    http_auth=(username, password),
                                    scheme=scheme,
                                    port=port,
                                    )
        self.index_name = index_name

    def free_search(self, query_string, start=0, size=10):

        q = Q("match", description={"query": query_string, "fuzziness":3})

        s = Search(using=self.client, index=self.index_name).extra(from_=start, size=size).query(q).sort('_score')

        response = s.execute()
        r = response.hits

        logging.info("Found {} news".format(r.total))
        return r
