from flask import Flask, render_template, request
import cPickle
from nltk.stem.porter import *
from math import log
import cooccurance as oc
import filter_reviews as fr
import SearchFiles
app = Flask(__name__)

stemmer = PorterStemmer()
#home page
@app.route('/')
def homepage(name = None):
	return render_template('index.html', name = name)

@app.route('/search', methods=['POST'])
def search():
	query = request.form['keywords']
	topK = 10
	reviews = SearchFiles.queryIndex(query, topK)
	results = {}
	result_list = []
	basePath = "data/products/"
	for review in reviews:
		with open(basePath + review, "r") as f:
			result_list.append(f.readline().split(",")[0])

	print "result list: ", result_list
	results[query] = result_list	
	'''keywords = query.split()
	clean_keywords = []
	all_tags = []
	for keyword in keywords:
		clean_query = stemmer.stem(keyword)
		tags = oc.query_pmi(cooccurances, probs, clean_query, 5)
		all_tags = all_tags + tags
		clean_keywords.append(clean_query)
	
	print clean_keywords
	print all_tags	
	results = {}
	d = fr.find_reviews_from_index2(clean_keywords, all_tags, index_file, lines)
	print "found reviews"
	results = oc.rank_sentences(d, all_tags, 3, cooccurances, probs)
	'''
	
	'''for keyword in keywords:
		clean_query = stemmer.stem(keyword)
		tags = oc.query_pmi(cooccurances, probs, clean_query, 10)
		d = fr.find_reviews_from_index(clean_query, tags, index_file, lines)
		print "found reviews"
		results = oc.rank_sentences(d, tags, 3, cooccurances, probs)
		print "ranked reviews"
		print results[tags[0]]
	'''
	return render_template('index.html', results = results)

@app.route('/sentence/<path:file_path>')
def sentence(file_path = None):
	temp = int(file_path)
	reviews = [lines[temp]]	
	return render_template('keywords.html', reviews = reviews)

if __name__ == '__main__':
	#app.debug = True
	#f = open(fr.PathToContents)
	#lines = f.readlines()
	#index_file = cPickle.load(open("iindex.p","rb"))
	#(cooccurances, probs) = oc.load_cooccurence("data/joint_prob_full.p", "data/probs_full.p")
	app.run(debug = True, use_reloader=False)


