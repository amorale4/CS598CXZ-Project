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
# this controlls the a lower bound to the number of reviews saved
# all the reviews must contain MIN_REVS < number of reviews
MIN_REVS=1
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
	pr_len = len(productRef)
	product_list = []
	with open(args[0], 'r') as f:
		current_product = ""      #current product name
		product_meta = []         #current review for the product
		current_product_list = [] #list of reviews for this product
		i = 0
		for line in f:
			#if i > 1000: break
			i = i+1
			if len(line) > 0 and line[:pr_len]== productRef:
				product = line[pr_len:].strip()
				if product == current_product:
					#add the current product
					if( len(product_meta) > 0):
						current_product_list.append(",".join(product_meta) + "\n")
						product_meta = []
					
				else:
					if( len(product_meta) > 0):
						current_product_list.append(",".join(product_meta) + "\n")
						product_meta = []
					
					if len(current_product_list) > 1:	
						with open(args[1] + current_product + ".txt", 'w') as output:
							output.writelines(current_product_list)

					if len(product_meta) > 0:
						print "i: ", i
						print "current_product: ", current_product
						print "product: ", product
						break

					current_product = product
					if not current_product in product_list:
						#print current_product
						product_list.append(current_product)

					else:
						print "have already seen: "+ current_product	
					current_product_list = []
					#write the lines to file
					#print "add to file"
					
			elif len(line) > 0:
				if line[:len(productNam)] == productNam:
					product_meta.append( line[len(productNam):].strip().replace(",","") )				
				elif line[:len(productHlp)] == productHlp:		
					product_meta.append( line[len(productHlp):].strip().replace(",","") )
				elif line[:len(productScr)] == productScr:		
					product_meta.append( line[len(productScr):].strip().replace(",","") )
				elif line[:len(productTim)] == productTim:	
					product_meta.append( line[len(productTim):].strip().replace(",","") )	
				elif line[:len(productSum)] == productSum:	
					product_meta.append( line[len(productSum):].strip().replace(",", "" ) )
				elif line[:len(productRev)] == productRev:		
					product_meta.append( "\"" +  line[len(productRev):].strip() + "\"" )

	if len(current_product_list) > 0:
		with open(args[1] + current_product + ".txt", 'w') as output:
			output.writelines(current_product_list)
		
if __name__ == "__main__":
	main(sys.argv[1:])
