import sys

# given a file containing a set or product reviews it will create a forward index of all the products and 
# their corresponding reviews. Current supported structure is as follows
#product/productId: B0000630MQ
#product/title: Kodak Max K2000 Battery Charger with 4 NiMH AA Batteries
#product/price: unknown
#review/userId: A2F6FARSB1VL6Q
#review/profileName: "frumpy16"
#review/helpfulness: 2/2
#review/score: 5.0
#review/time: 1072915200
#review/summary: Great charger
#review/text:
def main(args):
	print args

	if ( len(args) < 2 ):
		print "ussage: file_corpus.py <corpus> <outputDir>"
		return -1

	productRef = "product/productId:"
	productNam = "product/title:"
	productHlp = "review/helpfulness:"
	productScr = "review/score:"
	productTim = "review/time:"
	productSum = "review/summary:" 
	productRev = "review/text:"
	pr_len = len(prodRef)
	with open(args[0], 'r') as f:
		current_product = ""
		product_meta = []
		current_product_list = []
		for line in f:
			if len(line) > 0 and line[:pr_len]== productRef:	
			
				

if __name__ == "__main__":
	main(sys.argv[1:])
