import sys,os,csv,random,math

class Node(object):
	def __init__(self, parent, attr, entropy, lchild=None, rchild=None, classification=False):
		self.parent = parent;
		self.attr = attr;
		self.entropy = entropy;
		self.lchild = lchild;
		self.rchild = rchild;
		self.classification = classification;

def getDataSet(inputFileName):
	dataSet=list();
	attribute=list();
	with open(inputFileName) as csvfile:
		reader = csv.reader(csvfile,delimiter='\t',quoting=csv.QUOTE_NONE);
		i=0;
		for row in reader:
			if(i==0):
				attribute=row;
				i=i+1;
				continue;
			i=i+1;
			j=0;
			eachData=dict();
			for attr in attribute:
				if row[j]=='true':
					eachData[attr]=True;
				else:
					eachData[attr]=False;
				j=j+1;
			dataSet.append(eachData);
		return dataSet,attribute;

def getTrainingDataSet(dataSet,trainingSetSize):
	trainingSet=list();
	testingSet=list();
	randomList = random.sample(range(len(dataSet)),trainingSetSize);
	#randomList = range(trainingSetSize);
	for i in range(len(dataSet)):
		if randomList.count(i)==0:
			testingSet.append(dataSet[i]);
		else:
			trainingSet.append(dataSet[i]);
	return testingSet,trainingSet

def getPriorProb(trainingSet):
	i=0;
	j=0;
	for row in trainingSet:
		if row["CLASS"]==True:
			i=i+1;
		else:
			j=j+1;
	#print(str(i)+" "+str(j));
	if(i>j):
		return True;
	else:
		return False;

def getEntropy(listing,attr):
	t,f = 0,0;
	for row in listing:
		if row[attr]==True:
			t=t+1;
		else:
			f=f+1;
	if t==0 or f==0:
		return 0;
	t=float(t);
	f=float(f);
	return -t/(t+f)*math.log(t/(t+f),2)-f/(t+f)*math.log(f/(t+f),2);

def constuctDecisionTree(parent,trainingSet,attribute):
	entropy=getEntropy(trainingSet,'CLASS');
	if len(trainingSet) == 0:
		return True;
	elif entropy==0:
		return trainingSet[0]['CLASS'];
	elif len(attribute) == 0:
		t,f=0,0;
		for row in trainingSet:
			if row['CLASS']==True:
				t=t+1;
			else:
				f=f+1;
		return t>f;
	else:
		lset=list();
		rset=list();
		minEntropy=1;
		classification=True;
		minAttr=attribute[0];
		size=len(trainingSet);
		for attr in attribute:
			l1=list();
			l2=list();
			for row in trainingSet:
				if row[attr]==True:
					l1.append(row);
				else:
					l2.append(row);
			tempEntropy = getEntropy(l1,'CLASS')*len(l1)/size+getEntropy(l2,'CLASS')*len(l2)/size;
			if minEntropy > tempEntropy:
				minEntropy = tempEntropy;
				minAttr = attr;
				if len(l1)>len(l2):
					classification=True;
				else:
					classification=False;
				lset = l1;
				rset = l2;
		T=Node(parent,minAttr,entropy,classification=classification);
		attribute.remove(minAttr);
		T.lchild=constuctDecisionTree(T.attr,lset,attribute);
		T.rchild=constuctDecisionTree(T.attr,rset,attribute);
		attribute.append(minAttr);
		return T;

def displayDecisionTree(T):
	if type(T)==Node:
		print "parent: "+T.parent+" attribute: "+T.attr+" trueChild: ",;
		if(type(T.lchild)==Node):
			print T.lchild.attr,;
		else:
			print "leaf",;
		print " falseChild: ",;
		if(type(T.rchild)==Node):
			print T.rchild.attr,;
		else:
			print "leaf",;
		print ;
		displayDecisionTree(T.lchild);
		displayDecisionTree(T.rchild);

def getProbOfPrior(prob,testingSet):
	size=len(testingSet);
	numOfTrue=0;
	for row in testingSet:
		if row['CLASS']==prob:
			numOfTrue=numOfTrue+1;
	return float(numOfTrue)/size;

def getProbOfDT(T,testingSet):
	numOfTrue=0;
	listOfTree=list();
	for row in testingSet:
		Tree=T;
		while type(Tree)==Node:
			if row[Tree.attr]==True:
				#print 1,
				Tree=Tree.lchild
			else:
				#print 2,
				Tree=Tree.rchild
		listOfTree.append(Tree)
		if Tree==row['CLASS'] :
			numOfTrue=numOfTrue+1;
	return (float(numOfTrue)/len(testingSet),listOfTree);


if __name__=="__main__":
	if len(sys.argv)!=5:
		print ("There must be five parameters.");
		exit();
	else:
		inputFileName = sys.argv[1];
		trainingSetSize = int(sys.argv[2]);
		numberOfTrials = int(sys.argv[3]);
		verbose = sys.argv[4];
	if(int(verbose)!=0 and int(verbose)!=1):
		print("The verbose must be choose from 0 or 1.")
		exit();
	(dataSet,attribute)=getDataSet(inputFileName);
	attribute.remove('CLASS');
	#print(attribute)
	if trainingSetSize >= len(dataSet):
		print ("The training set size is bigger than size of data set.");
		exit();
	sumOfDT=0
	sumOfP=0;
	for i in range(numberOfTrials):
		(testingSet,trainingSet)=getTrainingDataSet(dataSet,trainingSetSize);
		#print(len(testingSet))
		priorProb = getPriorProb(trainingSet);
		T=constuctDecisionTree('root',trainingSet,attribute);
		print("TRIAL NUMBER: "+str(i))
		print("=================================")
		print '\n',
		print("DECISION TREE STRUCTURE:")
		displayDecisionTree(T);
		print '\n',
		probOfPrior=getProbOfPrior(priorProb,testingSet);
		probOfPrior=int(probOfPrior*100)
		sumOfP=sumOfP+probOfPrior;
		probOfDT,listOfTree=getProbOfDT(T,testingSet);
		probOfDT=int(probOfDT*100)
		sumOfDT=sumOfDT+probOfDT;
		print "Percent of test cases correctly classified by using prior probabilities from the training set = " + str(probOfPrior) +"%"
		print "Percent of test cases correctly classified by a decision tree built with ID3 = " + str(probOfDT) +"%"
		print '\n',
		if int(verbose)==1:
			print "The training set is:"
			for row in trainingSet:
				print row;
			print '\n',
			print "The testing set is:"
			i=0;
			for row in testingSet:
				print row
				print "The result of decision tree is "+str(listOfTree[i])
				print "The result of prior probability is "+str(priorProb)
				i=i+1;
	print '\n',
	print("example file used = "+inputFileName);
	print("number of trials = "+str(numberOfTrials));
	print("training set size for each trial = "+str(trainingSetSize));
	print("testing set size for each trial = "+str(len(dataSet)-trainingSetSize));
	print("mean performance of using prior probability derived from the training set = "+ str(sumOfP/numberOfTrials)+"% correct classification");
	print("mean performance of decision tree over all trials = "+str(sumOfDT/numberOfTrials)+"% correct classification");
