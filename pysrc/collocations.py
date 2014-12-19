import cPickle
import operator
from nltk.stem.porter import *
from math import log
import cooccurance as oc
import filter_reviews as fr

(cooccurances, probs) = oc.load_cooccurence("data/joint_prob_full.p", "data/probs_full.p")
def main():
	(original_lines, clean_lines) = fr.filter_contents("testIndex/B0006DPVX2.txt")
	print original_lines
	print clean_lines
	gen_summary(clean_lines, original_lines, 2)
	return 0

def find_bigrams(input_list):
	bigram_list = []
	for i in range(len(input_list)-1):
		bigram_list.append((input_list[i].encode('ascii', 'ignore'), input_list[i+1].encode('ascii','ignore')))
	return bigram_list

# returns a dictionary with the key as the tags and the value as a list
# the format of the list is the (review number, sentence content)
# topK here is the number of tags to be generated	
def gen_summary(clean_lines, original_lines, topK):
	ret = []
	sentence_to_bigrams = []
	bigram_list = []
	for line in clean_lines:
		# first find all of the bigrams
		bigram_list = bigram_list + find_bigrams(line.split()[1:])
		sentence_to_bigrams.append(bigram_list)
		# then rank all of the bigrams based on the pmi score
	pmi_bigrams = oc.bigram_pmi(cooccurances, probs, bigram_list)[:topK]
	
	# once we have a ranked list of bigrams these will become our tags.
	print "top bigrams: " , pmi_bigrams
	print "num bigrams: " , len(pmi_bigrams)
	print "clean_lines: ", clean_lines
	# for each tag
	#    we then look at all the sentences which contain this tag	
	#    find the top 3 sentences which are most similar to all other sentences

	#tag to sentence dictionary
	tag_sent = {}
	already_used_sents = []	
	for ( (word1, word2), score ) in pmi_bigrams:
		indecies_of_curr_tag = []
		sents_of_curr_tag = []	
		original_tag = ""
		for i, sent_bigrams in enumerate(sentence_to_bigrams):
			if (word1, word2) in sent_bigrams:
				#print "bigram: ", word1, word2, " is in ", i
				indecies_of_curr_tag.append(i)
				if (original_tag == ""):
					#find the tag
					original_tag = find_tag(word1, word2, original_lines[i])
	
		# quick hack would be to save the sentences that are already seened
		# but this does not solve the problem of choosing good sentences	
		best_sents_indices = top_sentences(indecies_of_curr_tag, clean_lines, already_used_sents)
		already_used_sents = already_used_sents + best_sents_indices
		for index in best_sents_indices:
			revNum = clean_lines[index].split()[0].encode('ascii','ignore')
			print "adding revNum: ", revNum
			print "original line[index]:", original_lines[index]
			sents_of_curr_tag.append( ( revNum, original_lines[index] ) )

		#need to find the phrase which corresponds to the tag
		tag_sent[original_tag] = list(set(sents_of_curr_tag))

	#TODO: here its possible that we return sentences from the same view as the best sentences so we 
	#      need to make sure that we only return the sentences from the differnt reviews.
	print tag_sent
	return tag_sent				
	# if ( len(pmi_bigrams) > 0 ):
	#	ret.append(pmi_bigrams)
	
	# print bigram_list
	# print "ret: ", ret


# for all the sentences find the ones that are the closest to all the other sentences
# assumming indices is non-empty
# returns a list of indices to the topK sentences with the closest to all the other sentences
def top_sentences(indices, sentences, already_used = []):
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
				curr_sim = jaccard_sim(sentences[index1].split()[1:], sentences[index2].split()[1:]) 
				total_similarities[index1] = total_similarities.get(index1,0) + curr_sim
				total_similarities[index2] = total_similarities.get(index2,0) + curr_sim
		
	#from all of the similarities return the best one
	ret_sorted_dic = sorted(total_similarities.iteritems(), key=operator.itemgetter(1), reverse=True)
	ret_sorted = ret_sorted_dic[:topK]

	result = []
	if len(already_used) > 0:
		left_to_return = topK
		for (index,score) in ret_sorted_dic:
			if not index in already_used:
				result.append(i)
				left_to_return = left_to_return - 1
			if left_to_return < 1:
				break
				
	else:
		result = [ index for (index,score) in ret_sorted ]

	return result

#cosine similarity
def cos_sim(v1, v2):

	return 0

# takes in two list of items 
def jaccard_sim(vec1, vec2):
	s1 = set(vec1)
	s2 = set(vec2)
	n = len(s1.intersection(s2))
    	return n / float(len(s1) + len(s2) - n) 	

# finds the original phrase corresponding to the phrase, it finds the first closest phrase corresponding to the 
# stemmed word
def find_tag( word1, word2, sentence):
	tokens = fr.tokenizer2.tokenize(sentence.strip())
	#clean_line = [fr.stemmer.stem(token) for token in tokens if token not in stop_lst and token not in punctuation and token.isalpha()] 
	phrase = []
	for token in tokens:
		if token not in fr.punctuation and token.isalpha():
			curr_token = fr.stemmer.stem(token)
			if curr_token == word2:
				phrase.append(token)
				break
			if len(phrase) > 0:
				phrase.append(token)
			if curr_token == word1:
				phrase = []
				phrase.append(token)
	return " ".join(phrase)




if __name__ == "__main__":
	#print find_tag( "happi", "send", "i was happy after i send it away.")
	#print find_tag( "take", "pictur", "taking still pictures worked, but ...")
	main()
	#print jaccard_sim([1,2,3], [2,3])
