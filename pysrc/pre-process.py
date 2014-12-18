'''take in sentences, output vector representation of reviews'''
import random
import numpy as np
def generate_dict(filename):
	d = {}
	location = 0;
	sentence_lst = []
	with open(filename) as fileobj:
		for line in fileobj:
			if len(line[:len(line)-1]) > 0:
				lst = []
				words = line[:len(line)-1].split()
				review_id = words[0]
				for word in words[1:]:
					if word not in d:
						d[word] = location
						lst.append((location, 1))
						location += 1
					else:
						lst.append((d[word], 1))
				lst.sort(key=lambda tup: tup[0])
				lst.insert(0, words[0])
				sentence_lst.append(lst)		
	#print sentence_lst			
	return sentence_lst

def cluster_points(X, mu):
	clusters  = {}
	for x in X:
		min_d = 0
		min_idx = 0
		cnt = 0
		for m in mu:
			d = getDistance(x,m)
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

def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        
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
	print retval
	return retval
				
def k_means(X, K):
	#randomly generate k centers
	#calculate 
	oldmu = random.sample(X, K)
	mu = random.sample(X, K)
	while not has_converged(mu, oldmu):
		oldmu = mu
		# Assign all points in X to clusters
		clusters = cluster_points(X, mu)
		# Reevaluate centers
		mu = reevaluate_centers(oldmu, clusters)
	return(mu, clusters)
def main_func():
	#lst = generate_dict('pmi_input_sentences_full.txt')
	#k_means(lst, 5)
	#d = getDistance([0, (0,1),(2, 2), (3, 5)], [1, (1, 1), (2, 4), (4,1), (5, 1)])
	#cluster_points([[0, (0,1), (2,2)]], [[0, (1,1), (2, 2)], [0, (0,1), (3,3)]])
	
	#1 + 1 + 4 + 25 + 1
	#print d
	getMean([[0, (0,1),(2, 2), (5, 5)], [1, (1, 1), (2, 4), (4,1), (5, 1)], [2,(2,6), (4,2)]])
if __name__ == "__main__":
	main_func()
