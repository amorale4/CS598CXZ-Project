from flask import Flask, render_template, request
import cPickle
from nltk.stem.porter import *
from math import log
import cooccurance as oc
import filter_reviews as fr
import SearchFiles
import k_means as km
import collocations as col

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
	#results = {}
	product = {}
	basePath = "data/products/"
	for review in reviews:
		with open(basePath + review, "r") as f:
			product[review] = f.readline().split(",")[0]

	#tagInput = fr.filter_corpus(basePath + review)
	#tags = pp.main_func(tagInput)
	#print "result list: ", result_list
	return render_template('index.html', product = product)
	#results[query] = result_list	
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

@app.route('/product/<path:file_path>/<path:name>')
def product(file_path = None, name = None):
	basePath = "data/products/"
	filename = basePath + file_path
	(original_lines, clean_lines) = fr.filter_contents(filename)
	results = col.gen_summary(clean_lines, original_lines, 5)
	#results = km.main_func(tagInput[1], tagInput[0])
	#print results
	return render_template('index.html', name = name, file_path = file_path, results = results)
	#return "OK"
	'''query = request.form['keywords']
	topK = 10
	reviews = SearchFiles.queryIndex(query, topK)
	product = {}
	#results = {}
	basePath = "data/products/"
	for review in reviews:
		with open(basePath + review, "r") as f:
			product[review] = f.readline().split(",")[0]
	tagInput = fr.filter_corpus(basePath + file_path)
	results = km.main_func(tagInput)
	print results
	return render_template('index.html', product = product)'''

@app.route('/sentence/<path:file_name>/<path:rid>')
def sentence(file_name = None, rid = None):
	file_path = "data/products/" + file_name
	reviews = [km.get_review(int(rid), file_path)]
	return render_template('keywords.html', reviews = reviews)
	'''temp = int(file_path)
	reviews = [lines[temp]]	
	return render_template('keywords.html', reviews = reviews)'''

if __name__ == '__main__':
	#app.debug = True
	#f = open(fr.PathToContents)
	#lines = f.readlines()
	#index_file = cPickle.load(open("iindex.p","rb"))
	#(cooccurances, probs) = oc.load_cooccurence("data/joint_prob_full.p", "data/probs_full.p")
	app.run(debug = True, use_reloader=False)


