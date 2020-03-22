import logging
import unittest

from main.service.w2vec_service import Word2VecClient


class TestW2VClient(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.w2v_client = Word2VecClient('../../main/models/model.pickle', '../../main/models/facts.pickle')
        logging.info("Setup")

    def test_search(self):
        matches = self.w2v_client.find_top_matches("komary, psy, zwierzęta")
        print(matches)
        assert matches.shape[0] > 0
