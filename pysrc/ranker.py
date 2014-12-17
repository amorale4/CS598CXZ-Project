def main():
	f = open("data/Electronics.txt", "r")
	lines = f.readlines()
	products=[]
	for i, line in enumerate(lines):
		if i % 10000 == 0:
			print i 
		i = i+1
		if line[:14] == "product/title:":
			product = line[14:]
			#if product not in products:
			products.append(product.split())
	f.close()
	with open("products.dat", "w") as b:
		b.writelines(products)

if __name__ == "__main__":
	main()
