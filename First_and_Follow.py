input = {
	"S":["AeB","bA","e"],
	"A":["aAb","e"],
	"B":["bB","e"]
}
def rDirectLR(inputA, A):
	temp = inputA[A]
	tempCr = []
	tempInCr = []
	for i in temp:
		if i[0] == A:
			tempInCr.append(i[1:]+[A+"'"])
		else:
			tempCr.append(i+[A+"'"])
	tempInCr.append(["e"])
	inputA[A] = tempCr
	inputA[A+"'"] = tempInCr
	return inputA
def checkForIndirect(inputA, a, ai):
	if ai not in inputA:
		return False 
	if a == ai:
		return True
	for i in inputA[ai]:
		if i[0] == ai:
			return False
		if i[0] in inputA:
			return checkForIndirect(inputA, a, i[0])
	return False
def rep(inputA, A):
	temp = inputA[A]
	newTemp = []
	for i in temp:
		if checkForIndirect(inputA, A, i[0]):
			t = []
			for k in inputA[i[0]]:
				t=[]
				t+=k
				t+=i[1:]
				newTemp.append(t)
		else:
			newTemp.append(i)
	inputA[A] = newTemp
	return inputA
def rem(input):
	c = 1
	conv = {}
	inputA = {}
	revconv = {}
	for j in input:
		conv[j] = "A"+str(c)
		inputA["A"+str(c)] = []
		c+=1
	for i in input:
		for j in input[i]:
			temp = []	
			for k in j:
				if k in conv:
					temp.append(conv[k])
				else:
					temp.append(k)
			inputA[conv[i]].append(temp)
	for i in range(c-1,0,-1):
		ai = "A"+str(i)
		for j in range(0,i):
			aj = inputA[ai][0][0]
			if ai!=aj :
				if aj in inputA and checkForIndirect(inputA,ai,aj):
					inputA = rep(inputA, ai)
	for i in range(1,c):
		ai = "A"+str(i)
		for j in inputA[ai]:
			if ai==j[0]:
				inputA = rDirectLR(inputA, ai)
				break
	op = {}
	for i in inputA:
		a = str(i)
		for j in conv:
			a = a.replace(conv[j],j)
		revconv[i] = a
	for i in inputA:
		l = []
		for j in inputA[i]:
			k = []
			for m in j:
				if m in revconv:
					k.append(m.replace(m,revconv[m]))
				else:
					k.append(m)
			l.append(k)
		op[revconv[i]] = l
	return op
result = rem(input)
def first(input, term):
	a = []
	if term not in input:
		return [term]
	for i in input[term]:
		if i[0] not in input:
			a.append(i[0])
		elif i[0] in input:
			a += first(input, i[0])
	return a
firsts = {}
for i in result:
	firsts[i] = first(result,i)
	print(f'First({i}):',firsts[i])
def follow(input, term):
	a = []
	for rule in input:
		for i in input[rule]:
			if term in i:
				temp = i
				indx = i.index(term)
				if indx+1!=len(i):
					if i[-1] in firsts:
						a+=firsts[i[-1]]
					else:
						a+=[i[-1]]
				else:
					a+=["e"]
				if rule != term and "e" in a:
					a+= follow(input,rule)
	return a
follows = {}
for i in result:
	follows[i] = list(set(follow(result,i)))
	if "e" in follows[i]:
		follows[i].pop(follows[i].index("e"))
	follows[i]+=["$"]
	print(f'Follow({i}):',follows[i])
