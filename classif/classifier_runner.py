from core_modules.election_news_classifier.election_classifier import SemanticFeatureExtractor
from logger import setup_logging

__author__ = 'pralav'
def classify_news(path='/news_classified.pkl',articles=None,logging=None):
    vec_name="new_vectorizers.pkl"
    mod_name="new_models.pkl"
    kbest_name="new_kbests.pkl"
    sem = SemanticFeatureExtractor(logging=logging,vec_name=vec_name,model_name=mod_name,kbest_name=kbest_name)
    # sem.train_examples()
    sem.classify_db_articles_batch(reset=False,limit=5000)

if __name__ == '__main__':

    logging=setup_logging()
    classify_news(logging=logging)