import math
import nltk.data
from nltk.collocations import *
from nltk.stem.porter import *
from nltk.tokenize import *
import cooccurance
import collections
import cPickle
import random

Datafile="data/Electronics.txt"
PathToContents="data/contents/contents.dat"
punctuation = set(['.',',','?','!','\'','\"','`','``','*','-','/','+'])
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
tokenizer2 = RegexpTokenizer(r'(\w|\')+')
stemmer = PorterStemmer()
SampleSize = 100

def filter_reviews():
	open("Filtered_Electronics2.txt","w").close()
	f = open('Filtered_Electronics2.txt', 'a')
	clean_lines = []
	i = 0
	#stop_lst = get_stop_lst()
	punctuation = ['.',',','?','!','\'','\"','`','``','*','-','/','+']
	with open(Datafile, 'r') as fileobj:
		for line in fileobj:
			if i % 10000 == 0:
				print i
			if len(line)> 0 and line[:12]== 'review/text:':
				review = line[12:].strip()
				
				for punc in punctuation:
					review = review.replace(punc, ' ')

				words = review.split()
				s = ""
				for word in words:
					if word.lower() not in stop_lst:
						s += word.lower() + " "	
				clean_lines.append(s.strip()+'\n')
				i = i + 1
	f.writelines(clean_lines)

def filter_contents():
	#open("data/contents/contents.dat","r")
	f = open('pmi_input_sentences_full.txt', 'w')
	clean_lines = []
	i = 0
	#stop_lst = set(get_stop_lst())
	punctuation = set(['.',',','?','!','\'','\"','`','``','*','-','/','+'])
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')			
	tokenizer2 = RegexpTokenizer(r'(\w|\')+')
	with open("data/contents/contents.dat", 'r') as fileobj:
		for review in fileobj:
			if i % 10000 == 0:
				print i
			lines = tokenizer.tokenize(review.lower())
			#print len(lines)
			for line in lines:
				#tokens = nltk.wordpunct_tokenize(line)
				tokens = tokenizer2.tokenize(line.strip())
				stemmer = PorterStemmer()
				clean_line = [stemmer.stem(token) for token in tokens if token not in stop_lst and token not in punctuation and token.isalpha()]
				if len(clean_line) > 2 :
					clean_lines.append(" ".join(clean_line) + '\n')	
			i = i + 1

	f.writelines(clean_lines)

def inverted_index():
	iindex = collections.defaultdict(set)
	i = 0
	stop_lst = set(get_stop_lst())
	punctuation = set(['.',',','?','!','\'','\"','`','``','*','-','/','+'])
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')	
	tokenizer2 = RegexpTokenizer(r'(\w|\')+')
	with open("contents.dat","r") as fileobj:
		for review in fileobj:
			if i% 10000 == 0:
				print i
			lines = tokenizer.tokenize(review.lower())
                        #print len(lines)
                        for line in lines:
                                #tokens = nltk.wordpunct_tokenize(line)
                                tokens = tokenizer2.tokenize(line.strip())
                                stemmer = PorterStemmer()
                                clean_line = [stemmer.stem(token) for token in tokens if token not in stop_lst and token not in punctuation and token.isalpha()]
				for token in set(clean_line):
					iindex[token].add(i)
					
                                #if len(clean_line) > 2 :
                                #        clean_lines.append(" ".join(clean_line) + '\n')
                        i = i + 1

	cPickle.dump(iindex, open( "iindex.p", "wb" ) )


def find_sentences_from_reviews(tag_review_dict):
	d = {}
	print "looking for sentences"
	stop_lst = set(get_stop_lst())
	tokenize=tokenizer2.tokenize
	stem = stemmer.stem
	for tag, reviews in tag_review_dict.iteritems():
		print "current tag: ", tag
		sentences = []
		for (idx, review) in reviews:
			lines = tokenizer.tokenize(review)
			for line in lines:
		                #tokens = nltk.wordpunct_tokenize(line)
		                tokens = tokenize(line)
		                clean_line = [stem(token) for token in tokens if token not in stop_lst and token not in punctuation and token.isalpha()]
				if tag in clean_line:
					sentences.append((idx,line))
		d[tag] = sentences
	return d

				
		
def find_reviews_from_index(query, tags, index_file, lines):
	#index_file = cPickle.load(open("iindex.p", "rb"))
	print "looking for reviews"
	d = {}
	query_doc = set(index_file[query])
	#lines = f.readlines()
	for tag in tags:
		reviews = []
		query_docs = query_doc.intersection(index_file[tag])
		for location in query_docs:
			reviews.append((location, lines[location]))
		
		sample_reviews = random.sample(reviews, 100)
		d[tag] = sample_reviews
		print "number of reviews for tag: ", tag, " = ", len(reviews)
	return find_sentences_from_reviews(d)

def find_reviews_from_index2(queries, tags, index_file, lines):
	print "looking for reviews"
	d = {}
	query_doc = set(index_file[queries[0]])
	for i, query in enumerate(queries):
		if i != 0:
			query_doc = query_doc.intersection( set(index_file[query]) )
		
	#lines = f.readlines()
	for tag in tags:
		reviews = []
		query_docs = query_doc.intersection(index_file[tag])
		for location in query_docs:
			reviews.append((location, lines[location]))
		
		print "number of reviews for tag: ", tag, " = ", len(reviews)
		sample_reviews = random.sample(reviews, min(SampleSize, len(reviews)))
		d[tag] = sample_reviews
	return find_sentences_from_reviews(d)


def convert_to_contents():
	open("contents.txt","w").close()
	i = 0
	f = open('contents.txt', 'a')
	lines = []
	with open(Datafile, 'r') as fileobj:
		for line in fileobj:
			if len(line)> 0 and line[:12]== 'review/text:':
				lines.append(line[12:].strip().lower()+'\n')
				i = i + 1
				if i % 100000 == 0:
					print i
	f.writelines(lines)
	f.close()

def get_stop_lst():
	stop_lst = []
	with open("stop_words.txt", 'r') as fileobj:
		for line in fileobj:
			if len(line) > 0:
				stop_lst.append(line[:len(line) - 1])
	return stop_lst

def convert_to_title():
	open("titles.txt","w").close()
	f = open('titles.txt', 'a')
	lines = []
	i = 0
	with open(Datafile, 'r') as fileobj:
		for line in fileobj:
			if i % 100000 == 0:
				print i 
			if len(line)> 0 and line[:15]== 'review/summary:':
				lines.append(line[15:].strip()+'/'+str(i)+'\n')
				i = i + 1
	f.writelines(lines)
	
def get_mutual_info(query):
	#pair_d records the coocurrance of A and B = Nab
	#Na - Nb 
	pair_d = {}
	single_d = {}
	file_size = 0.0
	with open('Filtered_Electronics.txt') as fileobj:
		for line in fileobj:
			if (len(line) > 0):
				words = list(set(line[:len(line) - 1].split()))
				for word in words:	
					if word in single_d:
						single_d[word] += 1
					else:
						single_d[word] = 1

	with open('Filtered_Electronics.txt') as fileobj:
		for line in fileobj:
			if (len(line) > 0):
				file_size += 1.0
				words = list(set(line[:len(line) - 1].split()))
				for q in query:	
					if q in words:
						for word in words:
							if not word == q:
								key = q + "," + word
								if key not in pair_d:
									pair_d[key] = 1
								else:
									pair_d[key] += 1


	for key, value in pair_d.iteritems():
		words = key.split(',')
		if words[0] in single_d.keys() and words[1] in single_d.keys():
			p11 = (value+0.25)/(file_size+1)
			pa = (single_d[words[0]]+0.5)/(file_size+1)
			pb = (single_d[words[1]]+0.5)/(file_size+1)
			p10 = (single_d[words[0]]-value + 0.25)/(file_size + 1)
			p01 = (single_d[words[1]]-value + 0.25)/(file_size + 1)
			p00 = (file_size - single_d[words[0]] -single_d[words[1]]+value + 0.25)/(file_size+1)
			
			MI11 = 0
			MI10 = 0
			MI01 = 0
			MI00 = 0
			if p11 > 0 and pa >0 and pb > 0:
				MI11 = p11*(math.log(p11,2)-math.log(pa,2) - math.log(pb,2))
			if p10 > 0 and pa > 0 and 1-pb > 0:
				MI10 = p10*(math.log(p10,2)-math.log(pa,2) - math.log(1-pb,2))
			if p01 > 0 and 1-pa > 0 and pb > 0:
				MI01 = p01*(math.log(p01,2)-math.log(1-pa,2) - math.log(pb,2))
			if p00 > 0 and 1-pa > 0 and 1-pb > 0:
				MI00 = p00*(math.log(p00,2)-math.log(1-pa,2) - math.log(1-pb,2))
			'''if key == 'phone,call':
				print pa, pb, p11, p10, p01, p00
			if key == 'call,phone':
				print pa, pb, p11, p10, p01, p00'''
			MI = MI11 + MI01 + MI10 + MI00
			pair_d[key] = MI
		else:
			pair_d[key] = 0.0


	final_lst = sorted(pair_d.items(), key=lambda x:x[1])
	retval = []
	#f = open('Tags.txt', 'w')
	cnt = 0
	for a in final_lst[::-1]:
		if cnt >= 20:
			break;
		w = str(a[0]).split(',')
		#f.write(str(a[1]) + ' ' + str(w[1])+'\n')
		retval.append(str(a[1]) + ' ' + str(w[1]))
		cnt += 1
	#f.close()
	return retval
	'''cnt_lst = sorted(single_d.items(), key=lambda x:x[1])
	f = open('tags_with_cnt.txt', 'w')
	cnt = 0
	for a in cnt_lst[::-1]:
		if cnt >= 60:
			break;
		f.write(str(a[1]) + ' ' + str(a[0])+'\n')
		cnt += 1
	f.close()'''

def generate_key(word1, word2):
	if word1 < word2:
		key = word1+ ',' + word2
	else:
		key = word2 + ',' + word1
	return key

def get_tag_lst():
	tag_lst = []
	with open('Tags.txt') as fileobj:
		for line in fileobj:
			word = line.split()[1]
			tag_lst.append(word)
	return tag_lst

def get_sentences_based_on_tag(tag):
	sentence_lst = []
	with open('contents.txt') as fileobj:
		for line in fileobj:
			if len(line)> 0:
				sentences = line[:len(line) - 1].split('.')
				for sentence in sentences:
					if tag in sentence:
						sentence_lst.append(sentence)
	#print len(sentence_lst)
	return sentence_lst

def rank_sentences(tag):
	sentence_lst = get_sentences_based_on_tag(tag)
	tag_dist = get_mutual_info(tag)
	rank_d = {}

	for sentence in sentence_lst:
		score = get_similarity(tag_dist, sentence)
		rank_d[sentence] = score

	final_lst = sorted(rank_d.items(), key=lambda x:x[1])
	retval = []
	cnt = 0
	for a in final_lst[::-1]:
		if cnt >= 10:
			break;
		retval.append(str(a[1]) + ' ' + str(a[0]))
		cnt += 1

	print retval
	return retval

def get_similarity(tag_dist, sentence):
	score = 0.0
	for string in tag_dist:
		pair = string.split()
		if pair[1] in sentence:
			print pair[0]
			score += float(str(pair[0]))
			break
	return score
	
def main_func():
	f = open(PathToContents)
	lines = f.readlines()
	print "opening index"
	index_file = cPickle.load(open("iindex.p", "rb")) 
	(cooccurances, probs) = cooccurance.load_cooccurence("data/joint_prob_full.p", "data/probs_full.p")
	print "querying"


	query = "phone"
	tags = ["cell", "call"]

	d = find_reviews_from_index(query, tags, index_file, lines)
	print "loading cooccurance"
	print cooccurance.rank_sentences(d, tags, 3, cooccurances, probs)
	#get_stop_lst()
	#convert_to_title()
	#filter_reviews()
	#filter_contents()
	#convert_to_contents()
	#inverted_index()
	#query = ['phone']
	#tag_lst = get_mutual_info(query)
	
	#print lst
	'''query = ['call']
	lst = get_mutual_info(query)
	
	print lst'''
	
	#get_sentences_based_on_tag('tivo')
	#rank_sentences('wireless')
	'''tag_lst = get_tag_lst()
	
	for tag in tag_lst:
		print tag
		lst = get_mutual_info([tag])
		print lst'''	

if __name__ == "__main__":
	main_func()	
