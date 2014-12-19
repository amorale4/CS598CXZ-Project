'''take in sentences, output vector representation of reviews'''
import random, math
import numpy as np
import filter_reviews as fr

location_to_word = {}
def generate_dict(fileobj):
	
	d = {}
	word_cnt = {}
	location = 0;
	sentence_lst = []
	sentence_id = 0
	for line in fileobj:
		if len(line[:len(line)-1]) > 0:
			
			lst = []
			words = line[:len(line)-1].split()
			review_id = words[0]
			for word in words[1:]:
				try:
					word_cnt[word] += 1
	
				except KeyError:
					word_cnt[word] = 1
		
				if word not in d:
					d[word] = location
					location_to_word[location] = word
					location += 1

			for word in list(set(words[1:])):
				lst.append((d[word], word_cnt[word]))	
			lst.sort(key=lambda tup: tup[0])
			lst.insert(0, str(words[0])+"&"+str(sentence_id))
			sentence_lst.append(lst)
			sentence_id += 1				
	return sentence_lst

def cluster_points(X, mu):
	clusters  = {}
	'''for i in range(0,2):
		clusters[i] = [mu[i]]'''
	for x in X:
		min_d = 0
		min_idx = 0
		cnt = 0
		for m in mu:
			d = getDistanceL1(x,m)
			if cnt == 0:
				min_d = d
			elif d < min_d:
				min_idx = cnt
				min_d = d
			cnt += 1
		try:
			clusters[min_idx].append(x)
		
		except KeyError:
			clusters[min_idx] = [x]
	#print len(clusters)
	return clusters


def getDistance(l1, l2):
	(x1, w1) = l1[1]
	(x2, w2) = l2[1]
	cur1 = 1
	cur2 = 1
	s = 0
	while cur1 < len(l1) and cur2 < len(l2):
		x1 = l1[cur1][0]
		x2 = l2[cur2][0]
		if x1 < x2:
			s += l1[cur1][1]*l1[cur1][1]
			cur1 += 1
					
		elif x1 == x2:
			s += (l1[cur1][1]-l2[cur2][1])*(l1[cur1][1]-l2[cur2][1])
			cur1 += 1
			cur2 += 1
		else:
			s += l2[cur2][1]*l2[cur2][1]
			cur2 += 1
			
	while cur1 < len(l1):
		s += l1[cur1][1]*l1[cur1][1]
		cur1 += 1
	while cur2 < len(l2):
		s += l2[cur2][1]*l2[cur2][1]
		cur2 += 1
	return s

def getDistanceL1(l1, l2):
	(x1, w1) = l1[1]
	(x2, w2) = l2[1]
	cur1 = 1
	cur2 = 1
	s = 0
	while cur1 < len(l1) and cur2 < len(l2):
		x1 = l1[cur1][0]
		x2 = l2[cur2][0]
		if x1 < x2:
			s += l1[cur1][1]
			cur1 += 1
					
		elif x1 == x2:
			s += math.fabs(l1[cur1][1]-l2[cur2][1])
			cur1 += 1
			cur2 += 1
		else:
			s += l2[cur2][1]
			cur2 += 1
			
	while cur1 < len(l1):
		s += l1[cur1][1]
		cur1 += 1
	while cur2 < len(l2):
		s += l2[cur2][1]
		cur2 += 1
	return int(s)

def reevaluate_centers(mu, clusters):
    newmu = []
    for val in clusters.values():
	newmu.append(getMean(val))
    #print "newmu" + str(len(newmu))
    return newmu

def getMean(lst):
	retval = []
	d = {}
	for l in lst:
		for (x, w) in l[1:]:
			try:
				d[x].append(w)
			except KeyError:
				d[x] = [w]
	for key, val in d.iteritems():
		m = np.mean(val)
		retval.append((key, m))
	retval.sort(key=lambda tup: tup[0])	
	retval.insert(0, -1)
	min_p = getNearestPoint(retval, lst)
	#print retval
	return min_p

def getNearestPoint(center, lst):
	cnt = 0
	min_p = center
	min_d = 0
	for p in lst:
		d = getDistanceL1(center, p)
		if cnt == 0 or d < min_d:
			min_d = d
			min_p = p
		cnt += 1
	return min_p
		
def kNN(center, lst, k):
	retval = []
	review_ids = []
	while k > 0 and len(lst)>0:
		p = getNearestPoint(center, lst)
		rid = p[0].split("&")[0]
		if rid not in review_ids:
			review_ids.append(rid)
			retval.append(p[0])
			k = k-1
		lst.remove(p)
	return retval
	
def has_converged(mu, oldmu):
	return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))
				
def k_means(X, K):
	#randomly generate k centers
	#calculate 
	clusters = {}
	oldmu = random.sample(X, K)
	mu = random.sample(X, K)
	i = 0
	while True:
		i += 1
		oldmu = mu
		# Assign all points in X to clusters
		clusters = cluster_points(X, mu)
		# Reevaluate centers
		mu = reevaluate_centers(oldmu, clusters)
		if has_converged(mu, oldmu) or i >= 100:
			break
	#print mu
	#print clusters
	return (mu, clusters)

def simple_tag_generation(lst):
	word_cnt = {}
	for sentence in lst:
		words = sentence.split()
		for word in words:
			try:
				word_cnt[word] += 1
			except KeyError:
				word_cnt[word] = 1
	max_cnt = -1
	max_w = ""
	for word, cnt in word_cnt.iteritems():
		if cnt > max_cnt:
			max_w = word
			max_cnt = cnt
	#print max_w, max_cnt
	return max_w
		
def main_func(filename, sentence_lst):
	'''lst = [
	[1, (1, 1), (2, 1)],
	[1, (1, 2), (2, 2)],
	[1, (1, 2), (2, 1)],
	[2, (1, 4), (2, 5)],
	[2, (1, 5), (2, 4)],
	[2, (1, 6), (2, 7)],
	]'''
	#getNearestPoint([-1, (4,3)], [[0, (4,3)], [0, (4,2)]])
	lst = generate_dict(filename)
	#print location_to_word
	(mu, clusters) = k_means(lst, 5)
	#print clusters
	#results = []
	#print len(mu)
	tag_to_sentence = {}
	for key, val in clusters.iteritems():
		results = []
		for p in val:
			temp = ""
			for (x, w) in p[1:]:
				temp = temp + location_to_word[x] + " "
			#temp += str(p[0])
			results.append(temp[:-1])
		tag = simple_tag_generation(results)
		#print "CENTER " + str(key)
		best_ids = kNN(mu[key], val, 3)
		for bid in best_ids:
			ids = bid.split("&")
			
			s = sentence_lst[int(ids[1])]	
			try:
				tag_to_sentence[tag].append((ids[0], s))
			except KeyError:
				tag_to_sentence[tag] = [(ids[0], s)]
			#find_original_sentence()
	for tag, sentences in tag_to_sentence.iteritems():
		print "TAG="+tag
		for s in sentences:
			print s
	return tag_to_sentence

def get_review(rid, filename):
	f = open(filename)
	lines = f.readlines()
	review = ",".join(lines[rid].split(",")[5:])
	return review
		

	#d = getDistance([0, (0,1),(2, 2), (3, 5)], [1, (1, 1), (2, 4), (4,1), (5, 1)])
	#cluster_points([[0, (0,1), (2,2)]], [[0, (1,1), (2, 2)], [0, (0,1), (3,3)]])
	
	#1 + 1 + 4 + 25 + 1
	#print d
	#getMean([[0, (0,1),(2, 2), (5, 5)], [1, (1, 1), (2, 4), (4,1), (5, 1)], [2,(2,6), (4,2)]])
if __name__ == "__main__":
	retval = fr.filter_contents("data/products/B000SNC70U.txt")
	main_func(retval[1], retval[0])









