from __future__ import division
########################################################################################################################
# Author: Aravindh Varadharaju
#
# For Task II
#
# Code is used to generate Sentiment rating using TextBlob Sentiment Analyzer which internally used NaiveBayesAnalyzer
# to calculate the sentiment score.
#
# Moreover, it takes a second for the analyzer to come up with a sentiment score. So need to generate the score by
# running the code in parallel. To support this, a field called counter has been added to the collection. The number
# of records in the collection is ~86579. The MacBookPro that the code is being run has 8 cores. So we split the records
# into 8 parts and each core will generate the score for a section of a collection. For example, Core 1 will generate
# the score for Section 1, Core 2 will generate the score for Section 2 etc.
#
# Input: Records from review collection
# Output: JSON files with records in the format: {"rating": 5, "business_id": "KPoTixdjoJxSqRSEApSAGg", "stars": 5}
#         where, "stars" is from the Yelp Dataset and "rating" is generated by TextBlob Sentiment Score
########################################################################################################################
from pymongo import MongoClient
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import time
from joblib import Parallel, delayed
import multiprocessing
import json

inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class Business:
    def __init__(self, business_id, stars, score):
        self.business_id = business_id
        self.stars = stars
        self.rating = score


def process_input(i):
    """
    Function is used to select a subset of data from mongodb. For example, if i = 1, the records with counter
    between 1 and 10000 are selected. This subset is then passed on to get a sentiment score from Naive Bayes. Naive
    Bayes returns a two scores for the text passed: positivity and negativity. Since we are not interested in negativity,
    we substract the negativity score from the positive score. Depending on the positive score, the review will be
    categorized into one of the review categories. For example, if the calculated positivity is 0.25, the review will
    be rated as 2 since 0.25 lies between 0.2 and 0.4
    #
    :param i: prefix for the record eg., when 1 records from 1 to 10000 will be fetched
    :return: None
    """
    global ratings, start, end
    if i == 1:
        start = 1
        end = 10000
    elif i == 2:
        start = 10001
        end = 20000
    elif i == 3:
        start = 20001
        end = 30000
    elif i == 4:
        start = 30001
        end = 40000
    elif i == 5:
        start = 40001
        end = 50000
    elif i == 6:
        start = 50001
        end = 60000
    elif i == 7:
        start = 60001
        end = 70000
    elif i == 8:
        start = 70001
        end = 80000
    elif i == 9:
        start = 80001
        end = 86579

    print "In :"+str(i)+" - "+str(start)+" - "+str(end)
    review_collection = MongoClient('localhost', 29017).yelp.review_counter
    review_cursor = review_collection.find({'counter': {'$gte': start, '$lte': end}})\
        .add_option(16)
    file_name = "CalculatedRatings_"+str(i)+".json"
    ratings_file = open(file_name, 'w')
    if review_cursor and review_cursor.alive:
        print "Cursor Count: "+str(review_cursor.count())
        line = 0
        for entry in review_cursor:
            business_id = entry["business_id"]
            text = entry["text"]
            stars = entry["stars"]
            if text:
                line += 1
                blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
                pos = blob.sentiment.p_pos
                neg = blob.sentiment.p_neg
                avg = pos - neg
                if avg < 0.2:
                    ratings = 1
                elif 0.2 < avg < 0.4:
                    ratings = 2
                elif 0.4 < avg < 0.6:
                    ratings = 3
                elif 0.6 < avg < 0.8:
                    ratings = 4
                elif avg > 0.8:
                    ratings = 5

            # record_dict = {'business_id': business_id, 'stars': stars, 'rating': rating}
            obj = Business(business_id, stars, ratings)
            ratings_file.write(json.dumps(vars(obj)))
            ratings_file.write("\n")
    print "Finished with the files starting with: ", str(i) + "\n"


def main():
    """
    The function is used to create the number of threads based on the CPU cores and then spawn equivalent number of
    jobs using threads
    :return:
    """

    num_cores = multiprocessing.cpu_count()
    print("numCores = " + str(num_cores))

    startTime = time.time()
    print "Start Time: "+str(startTime)
    results = Parallel(n_jobs=num_cores, verbose=5)(delayed(process_input)(i) for i in inputs)
    print 'Bulk Insert took ', (time.time() - startTime)

main()