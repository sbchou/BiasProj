import math

__author__ = 'pralav'
import traceback
from core_modules.election_news_classifier import *
from database.db_utils import get_annot_articles, get_articles_list_batch, \
    get_non_annotated_article_count, update_news_classification, reset_news_classification
from settings import MODELS
from utils import Utils
from sklearn import linear_model, svm, ensemble
from time import time
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, roc_curve, auc, precision_recall_fscore_support, confusion_matrix, \
    precision_recall_curve

import pylab as pl
# from key_entities_extractor.ner_extractor import *


from sklearn.cross_validation import train_test_split
from numpy import array
import scipy.sparse as sp
#
import numpy as np
from sklearn import cross_validation

stoplists = ["lot", "many", "most", "done", "do", "doing", "know", "knew", "actual", "actually", "specific",
             "something", "everything", "everyday", "thing", "isnt", "wasnt", "hasnt", "hadnt", "isn't", "wasn't",
             "hasn't", "hadn't", "wouldn't", "shouldn't", "wasn", "hadn", "hasn", "couldn", "wouldn", "couldn't",
             "shouldnt", "couldnt", "wouldnt", "a", "about", "above", "'s", "i'm", "'m", "'re", "re", "according",
             "across", "'nt", "'ve", "actually", "adj", "after", "afterwards", "again", "against", "all", "almost",
             "alone", "along", "already", "also", "although", "always", "among", "amongst", "an", "and", "another",
             "any", "anybody", "anyhow", "anyone", "anything", "anywhere", "are", "area", "areas", "aren't", "around",
             "as", "ask", "asked", "asking", "asks", "at", "away", "b", "back", "backed", "backing", "backs", "be",
             "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "began", "begin",
             "beginning", "behind", "being", "beings", "below", "beside", "besides", "best", "better", "between",
             "beyond", "big", "billion", "both", "but", "by", "c", "came", "can", "can't", "cannot", "caption", "case",
             "cases", "certain", "certainly", "clear", "clearly", "co", "come", "could", "couldn't", "d", "did",
             "didn't", "differ", "different", "differently", "do", "does", "doesn't", "don't", "done", "down", "downed",
             "downing", "downs", "during", "e", "each", "early", "eg", "eight", "eighty", "either", "else", "elsewhere",
             "end", "ended", "ending", "ends", "enough", "etc", "even", "evenly", "ever", "every", "everybody",
             "everyone", "everything", "everywhere", "except", "f", "face", "faces", "fact", "facts", "far", "felt",
             "few", "fifty", "find", "finds", "first", "five", "for", "former", "formerly", "forty", "found ", "four",
             "from", "further", "furthered", "furthering", "furthers", "g", "gave", "general", "generally", "get",
             "gets", "give", "given", "gives", "go", "going", "good", "goods", "got", "great", "greater", "greatest",
             "group", "grouped", "grouping", "groups", "h", "had", "has", "hasn't", "have", "haven't", "having", "he",
             "he'd", "he'll", "he's", "hence", "her", "here", "here's", "hereafter", "hereby", "herein", "hereupon",
             "hers", "herself", "high", "higher", "highest", "him", "himself", "his", "how", "however", "hundred", "nt",
             "ve", "i", "i'd", "i'll", "i'm", "i've", "ie", "if", "important", "in", "inc", "indeed", "instead",
             "interest", "interested", "interesting", "interests", "into", "is", "isn't", "it", "it's", "its", "itself",
             "j", "just", "k", "l", "large", "largely", "last", "later", "latest", "latter", "latterly", "least",
             "less", "let", "let's", "lets", "like", "likely", "long", "longer", "longest", "ltd", "m", "made", "make",
             "makes", "making", "man", "many", "may", "maybe", "me", "meantime", "meanwhile", "member", "members",
             "men", "might", "million", "miss", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "must", "my",
             "myself", "n", "namely", "necessary", "need", "needed", "needing", "needs", "neither", "never",
             "nevertheless", "new", "newer", "newest", "next", "nine", "ninety", "no", "nobody", "non", "none",
             "nonetheless", "noone", "nor", "not", "nothing", "now", "nowhere", "number", "numbers", "o", "of", "off",
             "often", "old", "older", "oldest", "on", "once", "one", "one's", "only", "onto", "open", "opened", "opens",
             "or", "order", "ordered", "ordering", "orders", "other", "others", "otherwise", "our", "ours", "ourselves",
             "out", "over", "overall", "own", "p", "part", "parted", "parting", "parts", "per", "perhaps", "place",
             "places", "point", "pointed", "pointing", "points", "possible", "present", "presented", "presenting",
             "presents", "problem", "problems", "put", "puts", "q", "quite", "r", "rather", "really", "recent",
             "recently", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", "second", "seconds",
             "see", "seem", "seemed", "seeming", "seems", "seven", "seventy", "several", "she", "she'd", "she'll",
             "she's", "should", "shouldn't", "show", "showed", "showing", "shows", "sides", "since", "six", "sixty",
             "small", "smaller", "smallest", "so", "some", "somebody", "somehow", "someone", "something", "sometime",
             "sometimes", "somewhere", "state", "states", "still", "stop", "such", "sure", "t", "take", "taken",
             "taking", "ten", "than", "that", "that'll", "that's", "that've", "the", "their", "them", "themselves",
             "then", "thence", "there", "there'd", "there'll", "there're", "there's", "there've", "thereafter",
             "thereby", "therefore", "therein", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've",
             "thing", "things", "think", "thinks", "thirty", "this", "those", "though", "thought", "thoughts",
             "thousand", "three", "through", "throughout", "thru", "thus", "to", "today", "together", "too", "took",
             "toward", "towards", "trillion", "turn", "turned", "turning", "turns", "twenty", "two", "u", "under",
             "unless", "unlike", "unlikely", "until", "up", "upon", "us", "use", "used", "uses", "using", "v", "very",
             "via", "w", "want", "wanted", "wanting", "wants", "was", "wasn't", "way", "ways", "we", "we'd", "we'll",
             "we're", "we've", "well", "wells", "were", "weren't", "what", "what'll", "what's", "what've", "whatever",
             "when", "whence", "whenever", "where", "where's", "whereafter", "whereas", "whereby", "wherein",
             "whereupon", "wherever", "whether", "which", "while", "whither", "who", "who'd", "who'll", "who's",
             "whoever", "whole", "whom", "whomever", "whose", "why", "will", "with", "within", "without", "won't",
             "work", "worked", "working", "works", "yeah", "would", "wouldn't", "x", "y", "year", "years", "yes", "yet",
             "you", "you'd", "you'll", "you're", "you've", "young", "younger", "youngest", "your", "yours", "yourself",
             "yourselves", "z"]


class SemanticFeatureExtractor(object):
    def __init__(self,logging,vec_name=VECTORIZER_PATH,model_name=NEWS_CLASS_MODEL_PATH,kbest_name=KBEST_PATH):

        self.logger=logging.getLogger(__name__)
        self.utils=Utils(logging)
        self.vec_name='%s/%s'%(self.utils.get_path(MODELS,MODULE),vec_name)
        self.model_name='%s/%s'%(self.utils.get_path(MODELS,MODULE),model_name)
        self.kbestpath='%s/%s'%(self.utils.get_path(MODELS,MODULE),kbest_name)
        self.load_models()



    def load_models(self):

        try:
            self.vectorizer = self.utils.load_file(self.vec_name)
            self.models = self.utils.load_file(self.model_name)
            self.ch2 = self.utils.load_file(self.kbestpath)
        except:
            self.vectorizer = None
            self.models = None
            self.ch2 = None



    def classify_db_articles_batch(self,reset=False,limit=5000):
        news_full={}
        self.logger.info("Counting articles to be classified")
        if reset:
            reset_news_classification()
        counts=get_non_annotated_article_count()
        total_articles= int([x for x in counts][0][0])
        self.logger.info("Total No. of articles to be classified:%d"%total_articles)
        num_batches=int(math.ceil((total_articles)/int(limit)))
        l=0
        while True:
            if l%10==0:
                self.logger.info("Processing Batch:%d of %d"%(l,(num_batches+1)))
            articles = get_articles_list_batch(limit=limit,offset=0)
            headlines = []
            bodies = []
            urls = []
            times=[]
            a_ids=[]
            contents=[]



            for article in articles:
                # print article
                headlines.append(article.title)
                bodies.append(article.body)
                urls.append(article.url)
                times.append(article.date_written)
                a_ids.append(article.id)
                if article.body is None or len(article.body.strip())==0:
                    contents.append("%s\n%s"%(article.title,article.description))
                else:
                    contents.append("%s\n%s"%(article.title,article.body))
            if len(contents)==0:
                break
            self.batch_classify_news(contents,urls,a_ids)
            l+=1


        # cPickle.dump(news_full, open(OUTPUT + output_file_name, 'w'))



    def ngrams_data(self, data_train, labels_train, mn=1, mx=3, binary=False, donorm=False, stopwords=True,
                    verbose=True, analyzer_char=False):
        f = data_train

        if donorm:
            f = self.normalize(f)

        ftrain = f
        labelss = []
        for y in labels_train:
            labelss.append(y if y > 0 else 0)

        y_train = np.array(labelss)

        analyzer_type = 'word'
        if analyzer_char:
            analyzer_type = 'char'

        if binary:
            vectorizer = CountVectorizer(ngram_range=(mn, mx), binary=True, stop_words=stoplists)
        elif stopwords:
            vectorizer = TfidfVectorizer(ngram_range=(mn, mx), stop_words=stoplists, analyzer=analyzer_type,
                                         sublinear_tf=True)
        else:
            vectorizer = TfidfVectorizer(ngram_range=(mn, mx), sublinear_tf=True, analyzer=analyzer_type,
                                         stop_words=stoplists)

        if verbose:
            print "extracting ngrams... where n is [%d,%d]" % (mn, mx)

        X_train = vectorizer.fit_transform(ftrain)
        self.vectorizer=vectorizer

        return X_train, y_train, vectorizer

    def get_chi_transform(self, X):

        return self.ch2.transform(X)

    def get_vector(self, X_train, y_train, nm):

        numFts = nm
        if numFts < X_train.shape[1]:
            ch2 = SelectKBest(chi2, k=numFts)
            X_train = ch2.fit_transform(X_train, y_train)
            self.utils.save_file(ch2,self.kbestpath)
            # cPickle.dump(ch2, open(self.kbestpath, 'w'))
            assert sp.issparse(X_train)
            self.ch2=ch2
        #
        # data_train, data_test, labels_train, labels_test = train_test_split(X_train, y_train, test_size=0.25,
        #                                                                     random_state=100)
        return X_train, y_train#, labels_test



    def run_classifiers(self, X_train, y_train, X_test, y_test=None, verbose=True):

        models = [

            linear_model.LogisticRegression(C=1),
            # ensemble.RandomForestClassifier(n_estimators=500, n_jobs=4, max_features=100, max_depth=2, min_samples_split=35,
            #                                 random_state=0),
            # ensemble.RandomForestClassifier(n_estimators=500, n_jobs=4, max_features=0.1, max_depth=50,
            #                                 min_samples_split=15, random_state=0), \
            # ensemble.GradientBoostingClassifier(n_estimators=500, subsample=0.25, min_samples_split=10,
            #                                     random_state=500), \
            ]
        dense = [True] * len(models)
        X_train = X_train.toarray()
        X_test = X_test.toarray()
        X_train_dense = X_train  # .toarray()
        X_test_dense = X_test  # .toarray()

        preds = []
        for ndx, model in enumerate(models):
            t0 = time()
            print "Training: ", model, 20 * '_'
            if dense[ndx]:
                model.fit(X_train_dense, y_train)
                pred = model.predict_proba(X_test_dense)

            else:
                model.fit(X_train, y_train)
                pred = model.predict_proba(X_test)

            y_pred = model.predict(X_test)
            print "Training time: %0.3fs" % (time() - t0)
            print 'Training Accuracy:', model.score(X_train, y_train)
            preds.append(array(pred[:, 1]))
            print 'Test Score:', model.score(X_test, y_test)
            print 'Precision,Recall,F1,Support:', precision_recall_fscore_support(y_test, y_pred, average='weighted')
            print 'Confusion matrix:', confusion_matrix(y_test, y_pred)
        self.utils.save_file(models,self.model_name)
        # cPickle.dump(models, open(self.model_name, 'w'))


    def roc(self, predicted_y, y_tst):
        print y_tst.shape, (predicted_y).shape
        fpr, tpr, thresholds = roc_curve(np.squeeze(y_tst), np.squeeze(predicted_y[:, 1]))
        roc_auc = auc(fpr, tpr)
        print "Area under the ROC curve : %f" % roc_auc

        # Plot ROC curve
        pl.clf()
        pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        pl.plot([0, 1], [0, 1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic example')
        pl.legend(loc="lower right")
        pl.show()

    def cross_validate(self, X_tr, y_tr):
        param_grid = [
            {'C': [1, 10, 100, 500, 1000]},
            # {'C': [1, 10, 100, 500, 1000]},
            # [{'max_features': [0.01,], 'max_depth': [2, 5,10,20]}]
        ]
        models = [
            linear_model.LogisticRegression(C=1),
            # , svm.SVC(C=1),
            # ensemble.RandomForestClassifier(n_estimators=500, n_jobs=4)

        ]
        X_tr = X_tr.todense()
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X_tr, y_tr, test_size=0.25,
                                                                             random_state=100)
        scores = ['precision', 'recall']
        for j in range(0, len(models)):
            for score in scores:
                print("# Tuning hyper-parameters for %s" % score)
                print()
                ens = models[j]  # linear_model.LogisticRegression(C=5)#
                clf = GridSearchCV(ens, param_grid[j], cv=5, verbose=3)
                clf.fit(X_train, y_train)

                print("Best parameters set found on development set:")
                print()
                print(clf.best_params_)
                print()
                print("Grid scores on development set:")
                print()
                for params, mean_score, scores in clf.grid_scores_:
                    print("%0.3f (+/-%0.03f) for %r"
                          % (mean_score, scores.std() * 2, params))
                print()

                print("Detailed classification report:")
                print()
                print("The model is trained on the full development set.")
                print("The scores are computed on the full evaluation set.")
                print()
                y_true, y_pred = y_test, clf.predict(X_test)
                print(classification_report(y_true, y_pred))
                print()

    def prec_rec(self, y_pred, y_true):
        precision, recall, thresholds = precision_recall_curve(np.squeeze(y_true), np.squeeze(y_pred[:, 1]))
        area = auc(recall, precision)
        print "Area Under Curve: %0.2f" % area

        pl.clf()
        pl.plot(recall, precision, label='Precision-Recall curve')
        pl.xlabel('Recall')
        pl.ylabel('Precision')
        pl.ylim([0.0, 1.05])
        pl.xlim([0.0, 1.0])
        pl.title('Precision-Recall example: AUC=%0.2f' % area)
        pl.legend(loc="lower left")
        pl.show()

    def train_examples(self):
        data, labels = [], []
        try:
            articles = get_annot_articles()
            for article in articles:
                title=article['title'] if article['title'] is not None else ''
                body=article['body'] if article['body'] is not None else ''
                # desc=article['description'] if article['description'] is not None else ''
                data.append(title + " " +" "+body)
                labels.append(article['annotation'])
            data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.25,
                                                                                random_state=100)#(data, labels, nm=20000)
            X_train, y_train, vectorizer = self.ngrams_data(data_train, labels_train,binary=True)
            data_train, labels_train = self.get_vector(X_train, y_train, nm=20000)
            X_test=self.vectorizer.transform(data_test)
            print X_test.shape
            data_test=self.get_chi_transform(X_test)
            labelss=[]
            for y in labels_test:
                labelss.append(y if y > 0 else 0)
            labels_test=np.array(labelss)

            print data_train.shape, data_test.shape, labels_train.shape, labels_test.shape
            self.cross_validate(data_train,labels_train)
            self.run_classifiers(data_train, labels_train, data_test, labels_test)
            self.utils.save_file(vectorizer,self.vec_name)
            # cPickle.dump(vectorizer, open(self.vec_name, 'w'))
            self.load_models()

        except:
            traceback.print_exc()


    def batch_classify_news(self, contents,urls,a_id):
        self.logger.info("Classifying news batch with size:%d..."%len(contents))
        if not isinstance(contents, list):
            contents = [contents]
        batches = int(math.ceil(len(contents) / 500))
        if len(contents)>0 and batches==0:
            batches=1

        for i in range(0, batches):
            start = i * 500
            end = i * 500 + 500
            articles_list = contents[start:end]
            a_id_list = a_id[start:end]
            if len(articles_list)==0:
                break
            X = self.vectorizer.transform(articles_list)
            X = self.get_chi_transform(X)
            # print 'Batch:', i, '/', batches

            model=self.models[0]
            y_preds = model.predict_proba(X.todense())
            elections_pred = [(a_id_list[idx],y) for idx, y in
                            enumerate(y_preds[:,1])]
                # news.setdefault(j, [])
                # news[j].extend(election)
            self.logger.info("Updating news batch...")
            update_news_classification(elections_pred)
            self.logger.info("Updated news batch...")







# headlines = cPickle.load(open(OUTPUT + '/news_headlines_latest.pkl', 'r'))
# print headlines
# for idx, new in headlines.iteritems():
#     print idx, len(new)
# for idx, headline, url, art,t,aid in headlines:
# arts = []
# for idx, headline, url, art,t,aid in headlines[0]:
#     # print headline, url,'\n',#art,'\n',(ner_text((idx,art)))
#     # print "---"*50,'\n\n'
#     text=re.sub('ADVERTISEMENTADVERTISEMENT','',headline+". "+art)
#
#     arts.append((idx,text))
# data=ner_docs_list_parallel(arts,{})
# for idx, headline, url, art,t,aid in headlines[1]:
#     print headline,url,data[idx]
# cPickle.dump(data,open(OUTPUT+"/nersss.pkl",'w'))
# #
# ners = cPickle.load(open(OUTPUT + '/nersss.pkl', 'r'))
# # for k,v in ners.iteritems():
# #     print k,v,"  "
# pers_d={}
# rel=RelationFinder()
# j=0
# for id,ners in ners.iteritems():
#     print 'Processing:',j
#     if 'ORG' in ners:
#         orgs=[re.sub('ADVERTISEMENTADVERTISEMENT','',org).strip() for org in expand_duplicates(ners['ORG']) ]
#     if 'PER' in ners:
#         pers=[re.sub('ADVERTISEMENTADVERTISEMENT','',per).strip() for per in expand_duplicates(ners['PER']) ]
#         for per in pers:
#             if per.lower() not in pers_d or len(pers_d[per.lower()])==0:
#                 pers_d[per.lower()]=rel.get_properties(per)#get_wiki_link(per)
#     j+=1
# cPickle.dump(pers_d,open(OUTPUT+'/persons.pkl','w'))
# # pers_d=cPickle.load(open(OUTPUT+'/persons.pkl','r'))
# # print len(ners)
# # for p,v in pers_d.iteritems():
# #     print p,v[0]
# #
# # in_doc_freq={}
# # doc_freq={}
# # j=0
# # for idx, headline, url, art,t,aid in headlines[1]:
# #     print headline,url,ners[j]
# #     j+=1
# #     for p,v in pers_d.iteritems():
# #         doc_freq.setdefault(p,0)
# #         in_doc_freq.setdefault(p,{})
# #         cnt=art.lower().count(p)
# #         if cnt >0:
# #             in_doc_freq[p][idx]=cnt
# #             doc_freq[p]+=1
# # cPickle.dump(pers_d,open(OUTPUT+'/person_counts.pkl','w'))
# # data=[]
# # for p,v in pers_d.iteritems():
# #     data.append((p,len(in_doc_freq[p].keys()),doc_freq[p],sum(in_doc_freq[p].values())))
# #
# #
