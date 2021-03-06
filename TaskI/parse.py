from __future__ import print_function
import json
import string
import nltk
import csv
#import enchant
from featureSpace import featureSpace, topFeatures
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
#from autocorrect import spell

myStopWords = ['haahaa','tough','thoughts','disappointed','guys','amazing','\'s','yay','nicely','inside','together','tell','love','\'m','n\'t','lol','good','a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can', 'cannot', "can't", 'cause', 'causes', 'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'd', 'date', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', "i'll", 'im', 'immediate', 'immediately', 'importance', 'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', 'itd', "it'll", 'its', 'itself', "i've", 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure', 'adorable', 'beautiful', 'clean', 'drab', 'elegant', 'fancy', 'glamorous', 'handsome', 'long', 'magnificent', 'old-fashioned', 'plain', 'quaint', 'sparkling', 'ugliest', 'unsightly', 'wide-eyed', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'gray', 'black', 'white', 'alive', 'better', 'careful', 'clever', 'dead', 'easy', 'famous', 'gifted', 'helpful', 'important', 'inexpensive', 'mushy', 'odd', 'powerful', 'rich', 'shy', 'tender', 'uninterested', 'vast', 'wrong', 'angry', 'bewildered', 'clumsy', 'defeated', 'embarrassed', 'fierce', 'grumpy', 'helpless', 'itchy', 'jealous', 'lazy', 'mysterious', 'nervous', 'obnoxious', 'panicky', 'repulsive', 'scary', 'thoughtless', 'uptight', 'worried', 'agreeable', 'brave', 'calm', 'delightful', 'eager', 'faithful', 'gentle', 'happy', 'jolly', 'kind', 'lively', 'nice', 'obedient', 'proud', 'relieved', 'silly', 'thankful', 'victorious', 'witty', 'zealous', 'broad', 'chubby', 'crooked', 'curved', 'deep', 'flat', 'high', 'hollow', 'low', 'narrow', 'round', 'shallow', 'skinny', 'square', 'steep', 'straight', 'wide', 'big', 'colossal', 'fat', 'gigantic', 'great', 'huge', 'immense', 'large', 'little', 'mammoth', 'massive', 'miniature', 'petite', 'puny', 'scrawny', 'short', 'small', 'tall', 'teeny', 'teeny-tiny', 'tiny', 'cooing', 'deafening', 'faint', 'hissing', 'loud', 'melodic', 'noisy', 'purring', 'quiet', 'raspy', 'screeching', 'thundering', 'voiceless', 'whispering', 'discovering', 'ancient', 'brief', 'early', 'fast', 'late', 'long', 'modern', 'old', 'old-fashioned', 'quick', 'rapid', 'short', 'slow', 'swift', 'young', 'bitter', 'delicious', 'fresh', 'greasy', 'juicy', 'hot', 'icy', 'loose', 'melted', 'nutritious', 'prickly', 'rainy', 'rotten', 'salty', 'sticky', 'strong', 'sweet', 'tart', 'tasteless', 'uneven', 'weak', 'wet', 'wooden', 'yummy', 'awesome', 'boiling', 'breeze', 'broken', 'bumpy', 'chilly', 'cold', 'cool', 'creepy', 'crooked', 'cuddly', 'curly', 'damaged', 'damp', 'dirty', 'dry', 'dusty', 'filthy', 'flaky', 'fluffy', 'freezing', 'hot', 'warm', 'wet', 'abundant', 'empty', 'few', 'full', 'heavy', 'light', 'many', 'numerous', 'sparse', 'substantial']

def preprocessing(reviewList):
    stopWords = set(stopwords.words('english'))
    stemming = SnowballStemmer("english", ignore_stopwords=False)
    punctuation = ['=','~','!','@','#','%','$','_','+','*','-',' '' ','(', ')', '?', ':', ';', ',', '.', '!', '', '\\', '...', '..', '/']
    digits = ['0','1','2','3','4','5','6','7','8','9']
    tokens0 = nltk.word_tokenize(reviewList)
    
    #Only consider nouns
    tokens1 = []
    pos_tag_results = nltk.pos_tag(tokens0)
    for i in range(0,len(pos_tag_results)):
        if pos_tag_results[i][1]=='NN':
            tokens1.append(pos_tag_results[i][0])

    #Remove punctuation
    tokens2 = []
    for everyToken in tokens1:
        everyToken = everyToken.lower()
        if everyToken not in string.punctuation and everyToken not in punctuation and everyToken not in digits:
            tokens2.append(everyToken)

    #Remove stopWords
    tokens3 = []
    for everyToken in tokens2:
       if everyToken not in stopWords and everyToken not in myStopWords:
           tokens3.append(everyToken)
   
    #Stemming
    tokens4 = []
    #d = enchant.dict_exists("en_US")
    for everyToken in tokens3:
        stemmedWord = stemming.stem(everyToken)
        #if not(d.check(stemmedWord)):
            #correctlySpelledWords = d.suggest(stemmedWord)
            #stemmedWord = correctlySpelledWords[0]
        tokens4.append(stemmedWord)
    
    return tokens4

#create bid categories dict
categories = []
idsCategories = {}
with open('RestaurantReviews.json') as f:
    for line in f:
        data = json.loads(line)
        value = data['category']
        idsCategories[data['business_id']] = value
        categories.append(value)      

#distinct categories
distinctCategories = []
'''
for category in categories:
    for subCategory in category:
        if(subCategory not in distinctCategories):
            print(subCategory)
            distinctCategories.append(subCategory)
distinctCategories.remove("Restaurants")
distinctCategories.remove("Food")
'''
#distinctCategories.append("Bars")
distinctCategories.append("Italian")
distinctCategories.append("Burgers")
distinctCategories.append("Mediterranean")
distinctCategories.append("Chinese")
distinctCategories.append("Steakhouses")
#distinctCategories.append("Indian")
distinctCategories.append("Mongolian")
distinctCategories.append("Barbeque")
distinctCategories.append("Japanese")
distinctCategories.append("Pakistani")
distinctCategories.append("Afghan")
distinctCategories.append("Mexican")
distinctCategories.append("Nightlife")
distinctCategories.append("American (New)")
distinctCategories.append("Bakeries")
distinctCategories.append("Breakfast & Brunch")
distinctCategories.append("Thai")
distinctCategories.append("Middle Eastern")
distinctCategories.append("Sushi Bars")

#create bid reviews dict
idsReviews = {}
with open('BusinessReviewsSample1.json') as f:
    i = 0
    for line in f:
        #print(i)
        data = json.loads(line)
        key = data['business_id']
        value = preprocessing(data['text'])
        if key in idsReviews:
            idsReviews[key].append(value)
        else:
            idsReviews[key] = [value]
        i += 1

#create dict of category and corresponding reviews
categoryReviews = {}
for category in distinctCategories:
    print(category)
    i = 0
    for key, value in idsCategories.items():
        if category in value:
            #remove later
            if idsReviews.get(key):
                categoryReviews[category] = idsReviews[key]
        i += 1

featureSpace(categoryReviews, idsCategories, distinctCategories)


   



