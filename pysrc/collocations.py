import cPickle
from nltk.stem.porter import *
from math import log
import cooccurance as oc
import filter_reviews as fr

(cooccurances, probs) = oc.load_cooccurence("data/joint_prob_full.p", "data/probs_full.p")
def main():
	#f = open(fr.PathToContents)
	#lines = f.readlines()
	#index_file = cPickle.load(open("iindex.p","rb"))
	(original_lines, clean_lines) = fr.filter_contents("testIndex/B0006DPVX2.txt")
	print original_lines
	print clean_lines
	gen_summary(clean_lines, original_lines, 10)
	return 0

def find_bigrams(input_list):
	bigram_list = []
	for i in range(len(input_list)-1):
		bigram_list.append((input_list[i].encode('ascii', 'ignore'), input_list[i+1].encode('ascii','ignore')))
	return bigram_list

# returns a dictionary with the key as the tags and the value as a list
# the format of the list is the (review number, sentence content)
def gen_summary(clean_lines, original_lines, topK):
	ret = []
	sentence_to_bigrams = []
	bigram_list = []
	for line in clean_lines:
		# first find all of the bigrams
		bigram_list = bigram_list + find_bigrams(line.split()[1:])
		sentence_to_bigrams.append(bigram_list)
		# then rank all of the bigrams based on the pmi score
	
	pmi_bigrams = oc.bigram_pmi(cooccurances, probs, bigram_list, topK)[:topK]
	
	# once we have a ranked list of bigrams these will become our tags.
	print "top bigrams: " , pmi_bigrams
	print "num bigrams: " , len(pmi_bigrams)
	# for each tag
	#    we then look at all the sentences which contain this tag	
	#    find the top 3 sentences which are most similar to all other sentences

	#tag to sentence dictionary
	tag_sent = {}
	
	for ( (word1, word2), score ) in pmi_bigrams:
		sents_of_curr_tag = []
		for i, sent_bigrams in enumerate(sentence_to_bigrams):
			if (word1, word2) in sent_bigrams:
				#print "bigram: ", word1, word2, " is in ", i
				sents_of_curr_tag.append(i)
		
		best_sents_indices = top_sentences(sents_of_curr_tag, clean_lines)
		
		for index in best_sents_indices:
			revNum = clean_lines[index].split()[0]
			sents_of_curr_tag.append( ( revNum, original_lines[index] ) )
		
	# if ( len(pmi_bigrams) > 0 ):
	#	ret.append(pmi_bigrams)
	
	# print bigram_list
	# print "ret: ", ret


# for all the sentences find the ones that are the closest to all the other sentences
# assumming indices is non-empty
# returns a list of indices to the topK sentences with the closest to all the other sentences
def top_sentences(indices, sentences):
	topK = 3
	if indices < 2:#require atlest 2 sentences
		return [indeces[0]]
	top_sents = []
	n = len(indices)
	total_similarities = {}
	for i, index1 in enumerate(indices):
		curr_sim = 0
		for j, index2 in enumerate(indices):
			if i < j:
				curr_sim = jaccard_sim(sentences[index1].split()[1:], sentence[index2].split()[1:]) 
				total_similarities[index1] = total_similarities.get(index1,0) + curr_sim
				total_similarities[index2] = total_similarities.get(index2,0) + curr_sim
		
	#from all of the similarities return the best one
	ret_sorted = sorted(total_similarities.iteritems(), key=operator.itemgetter(1), reverse=True)[:topK]
	#for index in ret_sorted:
	#	top_sents.append(sentences[index])
	return ret_sorted

# takes in two list of items 
def jaccard_sim(vec1, vec2):
	s1 = set(vec1)
	s2 = set(vec2)
	n = len(s1.intersection(s2))
    	return n / float(len(s1) + len(s2) - n) 	

if __name__ == "__main__":
	#main()
	#print jaccard_sim([1,2,3], [2,3])
