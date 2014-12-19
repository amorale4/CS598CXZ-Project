import sys
import operator
import cPickle
import filter_reviews
from math import log
import nltk.data
from nltk.stem.porter import *
from nltk.collocations import *
from nltk.tokenize import *

#data size 
N=600000

def get_list_of_words(string):
	return string.strip().replace('\n', '').split()

#returns a set of unique pairs.
def get_word_pairs(string):
	words = list(set(get_list_of_words(string) ) ) 
	pairs = []
	for i, word1 in enumerate(words):
		for j, word2 in enumerate(words):
			if i < j:
				pairs.append(( word1, word2))
	return pairs

def main(argv):
	if len(argv) < 1:
		print("Ussage: this_program inputfile")
		exit(-1)

	print argv
	
	#inputlines = []
	#with open( argv[0], 'r'  ) as input:
	#	inputlines = input.readlines()

	#get_cooccurence(argv[0], save=True)
		
	#(cooccurances, probs) = load_cooccurence("data/joint_prob_full.p", "data/probs_full.p")
	iindex = load_index("iindex.p")
	stemmer = PorterStemmer()
	while True:
		query = str( input("query:") )
		clean_query = stemmer.stem(query)
		#topK_pmi = query_pmi(cooccurances, probs, clean_query, 10)
		#print topK_pmi'''
		print iindex[query]
	#print cooccurances.keys()

	#(cooccurances, probs)  = get_cooccurence(inputlines)
	#N = len(inputlines)	

def rank_sentences( tagdict, tags, topK, cooccurances, probs):
	stop_lst = set(filter_reviews.get_stop_lst())
	punctuation = set(['.',',','?','!','\'','\"','`','``','*','-','/','+'])
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	tokenizer2 = RegexpTokenizer(r'(\w|\')+')
	tag_sentence_rank = {}
	stemmer = PorterStemmer()
	tokenize = tokenizer2.tokenize
	stem = stemmer.stem
	for tag in tags:
		candidates = tagdict[tag]
		if len(candidates) <= topK:
			tag_sentence_rank[tag] = candidates
			continue

		scores = []
		for (reviewIdx, sentence) in candidates:
			score = 0
			tokens = tokenize(sentence)
			clean_line = [stem(token) for token in tokens if token not in stop_lst and token not in punctuation and token.isalpha()]
			score = ( score + score_sentence_tag(clean_line, tag, cooccurances, probs) + 1) / (1.0*len(clean_line) + 1.0)
			scores.append((score, (reviewIdx, sentence) ))
		#max(scores)
		ret = sorted(scores, key=lambda score_sent: score_sent[0], reverse=True)[:topK]
		tag_sentence_rank[tag] = ret
		#for i,pair in enumerate(candidates):
		#	if scores[i] >= lowest_score
	return tag_sentence_rank
			
def score_sentence_tag(sentence, tag, cooccurances, probs):
	score = 0
	for word in sentence:
		N_AB = max(cooccurances.get((word,tag), 0 ), cooccurances.get((tag,word),0))
		if N_AB < 1:
			continue
		N_A =  probs.get(word, 0)
		N_B = probs.get(tag, 0)
		#p(x=1, y=1)
		p_11 =  (N_AB + 0.25) / (1.0*(1+N))
		#p(x=1,y=0)
		p_10 = (N_A - N_AB + 0.25) / (1.0*(1+N))
		#p(x=0,y=1)
		p_01 = (N_B - N_AB + 0.25) / (1.0*(1+N))
		#p(x=0,y=0)
		p_00 = (N - N_A - N_B + N_AB + 0.25) / (1.0*(1+N))
		#p(x=1)
		p_x = (N_A + 0.5) / (1.0*(1+N))
		#p(y=1)
		p_y = (N_B + 0.5) / (1.0*(1+N))
		m_xy = p_11*log( p_11/(p_x*p_y) , 2) + p_10 * log( p_10/(p_x*(1-p_y)),2) + p_01*log(p_01/((1-p_x)*p_y),2) + p_00*log(p_00/((1-p_x)*(1-p_y)),2)
		score = score + m_xy
	return score		

def query_pmi(cooccurances, probs, query, K):
	mutual_info = {} #results
	query_pairs = filter(lambda (x,y): x == query or y == query , cooccurances.keys())
	#temp = cooccurances.keys()[0]
	for temp in query_pairs:
		N_AB = max(cooccurances.get(temp, 0 ), cooccurances.get((temp[1],temp[0],0)))
		if N_AB < 1:
			continue
		N_A =  probs.get(temp[0], 0)
		N_B = probs.get(temp[1], 0)
		#p(x=1, y=1)
		p_11 =  (N_AB + 0.25) / (1.0*(1+N))
		#p(x=1,y=0)
		p_10 = (N_A - N_AB + 0.25) / (1.0*(1+N))
		#p(x=0,y=1)
		p_01 = (N_B - N_AB + 0.25) / (1.0*(1+N))
		#p(x=0,y=0)
		p_00 = (N - N_A - N_B + N_AB + 0.25) / (1.0*(1+N))
		#p(x=1)
		p_x = (N_A + 0.5) / (1.0*(1+N))
		#p(y=1)
		p_y = (N_B + 0.5) / (1.0*(1+N))
		m_xy = p_11*log( p_11/(p_x*p_y) , 2) + p_10 * log( p_10/(p_x*(1-p_y)),2) + p_01*log(p_01/((1-p_x)*p_y),2) + p_00*log(p_00/((1-p_x)*(1-p_y)),2)
		mutual_info[temp] = m_xy

	sorted_MI = sorted(mutual_info.iteritems(), key=operator.itemgetter(1), reverse=True)
	#print sorted_MI[0:10]
	tags = []
	for item in sorted_MI[0:K]:
		#print item
		temp1 =  item[0]
		if  temp1[0] == query:
			tags.append(temp1[1])
		else:
			tags.append(temp1[0])

	#return sorted_MI[0:K]
	return tags

def bigram_pmi(cooccurances, probs, query_pairs):
	mutual_info = {} #results
	for temp in query_pairs:
		#print "temp, " , temp
		N_AB = max(cooccurances.get(temp, 0 ), cooccurances.get((temp[1],temp[0],0)))
		#print "N_AB: ",  N_AB
		N_A =  probs.get(temp[0], 0)
		N_B = probs.get(temp[1], 0)
		#print "N_A: ", temp[0], " ", N_A
		#print "N_B: ", temp[1], " ", N_B
		if N_AB < 1:
			continue
		#p(x=1, y=1)
		p_11 =  (N_AB + 0.25) / (1.0*(1+N))
		#p(x=1,y=0)
		p_10 = (N_A - N_AB + 0.25) / (1.0*(1+N))
		#p(x=0,y=1)
		p_01 = (N_B - N_AB + 0.25) / (1.0*(1+N))
		#p(x=0,y=0)
		p_00 = (N - N_A - N_B + N_AB + 0.25) / (1.0*(1+N))
		#p(x=1)
		p_x = (N_A + 0.5) / (1.0*(1+N))
		#p(y=1)
		p_y = (N_B + 0.5) / (1.0*(1+N))
		m_xy = p_11*log( p_11/(p_x*p_y) , 2) + p_10 * log( p_10/(p_x*(1-p_y)),2) + p_01*log(p_01/((1-p_x)*p_y),2) + p_00*log(p_00/((1-p_x)*(1-p_y)),2)
		mutual_info[temp] = m_xy

	sorted_x = sorted(mutual_info.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_x
	'''
	sorted_MI = sorted(mutual_info.iteritems(), key=operator.itemgetter(1), reverse=True)
	#print sorted_MI[0:10]
	tags = []
	for item in sorted_MI[0:K]:
		#print item
		temp1 =  item[0]
		if  temp1[0] == query:
			tags.append(temp1[1])
		else:
			tags.append(temp1[0])

	#return sorted_MI[0:K]
	return tags
	'''

def load_cooccurence(cooccurenceFile, probFile):
	print "loading co-occurence table"
	cooccurence = cPickle.load( open( cooccurenceFile, "rb" ) )
	print "loading probabilities table"
	probs = cPickle.load( open( probFile, "rb" ) )
	return (cooccurence, probs)

def load_index(indexFile):
        iindex = cPickle.load( open( indexFile, "rb" ) )
        return iindex

def get_cooccurence(inputfile, save=False):
	inputlines = []
	with open( inputfile, 'r'  ) as input:
		inputlines = input.readlines()
	
	table = {}
	probabilities = {}
	counter = 0
	for line in inputlines:
		#words = list(set(get_list_of_words(line)))
		counter = counter + 1
		if counter % 10000 == 0:
			print counter
			if counter == N:
				break
		words = get_list_of_words(line)
		for word in words:
			probabilities[word] = probabilities.get(word,0)+1
		
		pairs = get_word_pairs(line)
		for (a,b) in pairs:
			if (a != b): 
				if table.get((a,b),0)  > table.get((b,a),0):
					table[(a,b)] = table.get((a,b),0) + 1
				else:
					table[(b,a)] = table.get((b,a),0) + 1
	#print table
	#sorted_table = sorted(table.iteritems(), key=operator.itemgetter(1), reverse=True)
	#sorted_prob = sorted(probabilities.iteritems(), key=operator.itemgetter(1), reverse=True)
	#print sorted_table[0:10]
	#for item in sorted_table[0:10]:
	#	 print item
	if (save):
		print "saving probability table"
		cPickle.dump(probabilities, open("probs_full.p", "wb"))
		print "saving co-occurance table"
		cPickle.dump(table, open("joint_prob_full.p", "wb"))

	return (table,probabilities)

if __name__ == "__main__":
	main(sys.argv[1:])
