#Alana Anderson and Julia McCarthy

from porter import create_stem
import math
class TextModel:

    def __init__(self, name):
        """ the constructor for the TextModel class
            all dictionaries are started at empty
            the name is just for our own purposes, to keep things 
            organized
        """
        self.name = name
        self.words = {}   # starts empty
        self.wordlengths = {}
        self.stems = {}
        self.sentencelengths = {}
        self.contractions = {}


    def __repr__(self):
        """ this method creates the string version of TextModel objects
        """
        s  = "\nModel name: " + str(self.name) + "\n"
        s += "    n. of words: " + str(len(self.words))  + "\n"
        s += "    n. of word lengths: " + str(len(self.wordlengths))  + "\n"
        s += "    n. of sentence lengths: " + str(len(self.sentencelengths))  + "\n"
        s += "    n. of stems: " + str(len(self.stems))  + "\n"
        # you will likely want another line for your custom text-feature!
        return s

    def readTextFromFile(self, filename): 
        """ should take in a filename (a string) and should return all of the text in that file as a single, very large string """
        f = open(filename)
        text = f.read()
        f.close()
        return text



    def makeSentenceLengths(self,s):
        """ should use the text in the input string s to create the self.sentencelengths dictionary """
        LoW = s.split()
        self.sentencelengths = {}
        sentencecount = 0
        for w in LoW:
            sentencecount+=1
            if w[-1] in '.?!':
                if sentencecount not in self.sentencelengths:
                    self.sentencelengths[sentencecount] = 1
                else:
                    self.sentencelengths[sentencecount] += 1
                sentencecount = 0
        return self.sentencelengths

 

    def cleanString(self,s):
        """ should take in a string s and return a string with no punctuation and no upper-case letters """
        newstring = ''
        for i in range(len(s)):
            if s[i] not in "?!,'.":
                newstring+=s[i].lower()
        return newstring

        

    def makeWordLengths(self,s):
        """  should use the text in the input string cleanstring to create the self.wordlengths dictionary """
        self.wordlengths = {}
        charcount = 0
        cleanstring = self.cleanString(s)
        for i in range(len(cleanstring)):
            charcount+=1
            if cleanstring[i] == ' ':
                charcount-=1
                if charcount not in self.wordlengths:
                    self.wordlengths[charcount] = 1
                else:
                    self.wordlengths[charcount] += 1
                charcount = 0
            if i == len(cleanstring)-1:
                if charcount not in self.wordlengths:
                    self.wordlengths[charcount] = 1
                else:
                    self.wordlengths[charcount] += 1
        return self.wordlengths



    def makeWords(self,s):
        """should use the text in the input string cleanstring to create a dictionary of the words and the number of times the word appears"""
        self.words = {}
        cleanstring = self.cleanString(s)
        LoW = cleanstring.split()
        wordcount = 0
        
        for word in LoW:
            if word in self.words:
                self.words[word]+=1
            else:
                self.words[word]=1
        return self.words

    def makeStems(self,s):
        """should use the text in the input string cleanstring to create a dictionary of the word stems and the number of times the stem appears"""
        self.stems = {}
        cleanstring = self.cleanString(s)
        LoW = cleanstring.split()
        

        for word in LoW:
            stem=create_stem(word)
            if stem in self.stems:
                self.stems[stem]+=1
            else:
                self.stems[stem]=1
        return self.stems

    def numcontractions(self,s):
        """uses the text in the input string cleanstring and creates a dictionary of two types of contractions used ('t and 've) and the number of times these contractions appear"""
        self.contractions = {}
        
        LoW = s.split()

        for word in LoW:
            if "'" in word:
                cont = word.split("'")
                if cont[1]=='t':
                    if cont[1] in self.contractions:
                        self.contractions[cont[1]]+=1
                    else:
                        self.contractions[cont[1]]=1
                elif cont[1]=='ve':
                    if cont[1] in self.contractions:
                        self.contractions[cont[1]]+=1
                    else:
                        self.contractions[cont[1]]=1
               
        return self.contractions

    def createAllDictionaries(self,s):
        """ creates all dictionaries """
        self.makeWords(s)
        self.makeWordLengths(s)
        self.makeSentenceLengths(s)
        self.makeStems(s)
        self.numcontractions(s)
 
    def printAllDictionaries(self):
        """ prints out all five of self's dictionaries """
        print 'self.name:', self.name 
        print 'self.words:', self.words  
        print 'self.wordlengths:', self.wordlengths 
        print 'self.stems:', self.stems
        print 'self.sentencelengths:', self.sentencelengths
        print 'self.contractions:', self.contractions

    def normalizeDictionary(self,d):
        """ normalizes dictionary """
        nd = {}
        V = d.values()
        sumd = float(sum(V))
        for k in d:
            nd[k] = d[k]/sumd
        return nd

    def smallestValue(self,nd1,nd2):
        """ takes in two model dictionaries nd1 and nd2 and returns the smallest positive value across both """
        smallestvalue = 1
        smallestvalue2 = 1
        for k in nd1:
            if nd1[k] < smallestvalue:
                smallestvalue = nd1[k]
        for k in nd2:
            if nd2[k] < smallestvalue2:
                smallestvalue2 = nd2[k]
        if smallestvalue < smallestvalue2:
            return smallestvalue
        else: return smallestvalue2

    def compareDictionaries(self,d,nd1,nd2):
        """ computes the log-probability that the dictionary d arose from the distribution of data in nd1 and nd2 """
        lp = 0
        e = self.smallestValue(nd1,nd2)/2
        for k in d:
            if k in nd1:
                lp+=d[k]*math.log(nd1[k])
            else: 
                lp+=d[k]*math.log(e)
        lp2 = 0
        for k in d:
            if k in nd2:
                lp2+=d[k]*math.log(nd2[k])
            else:
                e = e + 0.000000001
                lp2+=d[k]*math.log(e)
        list_of_probs = [lp,lp2]
        return list_of_probs

    def compareTextWithTwoModels(self,model1,model2):
        print 'The text model named [model1] has dictionaries:', model1.printAllDictionaries()
        print 'The text model named [model2] has dictionaries:', model2.printAllDictionaries()
        print 'The text model named [unknown(trial)] has dictionaries:', self.printAllDictionaries()
        words = self.compareDictionaries(self.words,model1.normalizeDictionary(model1.words),model2.normalizeDictionary(model2.words))
        wordlengths = self.compareDictionaries(self.wordlengths,model1.normalizeDictionary(model1.wordlengths),model2.normalizeDictionary(model2.wordlengths))
        sentencelengths = self.compareDictionaries(self.sentencelengths,model1.normalizeDictionary(model1.sentencelengths),model2.normalizeDictionary(model2.sentencelengths))
        stems = self.compareDictionaries(self.stems,model1.normalizeDictionary(model1.stems),model2.normalizeDictionary(model2.stems))
        contractions = self.compareDictionaries(self.contractions,model1.normalizeDictionary(model1.contractions),model2.normalizeDictionary(model2.contractions))

        print "           name          model 1             model 2"
        print "           ----          -------             -------"
        print "          words", ("%16i" % words[0]) + ("%20.2f" % words[1])
        print "    wordlengths", ("%16i" % wordlengths[0]) + ("%20.2f" % wordlengths[1])
        print "sentencelengths", ("%16i" % sentencelengths[0]) + ("%20.2f" % sentencelengths[1])
        print "          stems", ("%16i" % stems[0]) + ("%20.2f" % stems[1])
        print "   contractions", ("%16i" % contractions[0]) + ("%20.2f" % contractions[1])

        if words[0] > words[1]:
            print 'Model 1 wins the words feature.'
        else: print 'Model 2 wins the words feature.'

        if wordlengths[0] > wordlengths[1]:
            print 'Model 1 wins the wordlengths feature.'
        else: print 'Model 2 wins the wordlengths feature.'

        if sentencelengths[0] > sentencelengths[1]:
            print 'Model 1 wins the sentencelengths feature.'
        else: print 'Model 2 wins the sentencelengths feature.'

        if stems[0] > stems[1]:
            print 'Model 1 wins the stems feature.'
        else: print 'Model 2 wins the stems feature.'

        if contractions[0] > contractions[1]:
            print 'Model 1 wins the contractions feature.'
        else: print 'Model 2 wins the contractions feature.'

        totalmodel1 = [words[0],wordlengths[0],sentencelengths[0],stems[0],contractions[0]]
        totalmodel2 = [words[1],wordlengths[1],sentencelengths[1],stems[1],contractions[1]]
        if sum(totalmodel1) > sum(totalmodel2):
            print 'Therefore, model 1 wins!'
        elif sum(totalmodel2) > sum(totalmodel1): 
            print 'Therefore, model 2 wins!'
        else:
            print 'Therefore, the models are tied!'

# #test_tm = TextModel( "Milestone test" )  # create a TextModel object
# #text = test_tm.readTextFromFile( "test.txt" )
# #print text

# #test_tm.makeSentenceLengths(text)
# #print test_tm.sentencelengths
# clean_s = test_tm.cleanString(text)
# print clean_s

# test_tm.makeWordLengths(text)
# print test_tm.wordlengths

# test_tm.makeWords(text)
# print test_tm.words

# test_tm.makeStems(text)
# print test_tm.stems

 test_tm.numcontractions(text)
 print test_tm.contractions

# test_tm.printAllDictionaries()

# test_tm = TextModel( "Final test" )
# d = {'a': 5, 'b':1, 'c':2}
# nd = test_tm.normalizeDictionary( d )
# print "The original dictionary is"
# print d
# print "The normalized dictionary is"
# print nd

# test_tm = TextModel( "Final test" )
# d1 = {'a': 5, 'b':1, 'c':2}
# nd1 = test_tm.normalizeDictionary( d1 )
# d2 = {'a': 15, 'd':1}
# nd2 = test_tm.normalizeDictionary( d2 )
# print "The normalized dictionaries are"
# print nd1
# print nd2
# sm_va = test_tm.smallestValue( nd1, nd2 )
# print "and the smallest value between them is", 
# print sm_va 

# test_tm = TextModel( "Final test" )
# d = {'a':2, 'b':1, 'c':1, 'd':1, 'e':1}
# print "The unnormalized dictionary is"
# print d
# print "\n"
# d1 = {'a': 5, 'b':1, 'c':2}
# nd1 = test_tm.normalizeDictionary( d1 )
# d2 = {'a': 15, 'd':1}
# nd2 = test_tm.normalizeDictionary( d2 )
# print "The normalized comparison dictionaries are"
# print nd1
# print nd2

# List_of_log_probs = test_tm.compareDictionaries(d, nd1, nd2)
# print "The list of log probs is"
# print List_of_log_probs

# trained_tm1 = TextModel( "Model1" )
# text1 = trained_tm1.readTextFromFile( "train1.txt" )
# trained_tm1.createAllDictionaries(text1)
# trained_tm1.printAllDictionaries()

# trained_tm2 = TextModel( "Model2" )
# text2 = trained_tm1.readTextFromFile( "train2.txt" )
# trained_tm2.createAllDictionaries(text2)
# trained_tm2.printAllDictionaries()

# unknown_tm = TextModel( "Unknown (trial)" )
# text_unk = unknown_tm.readTextFromFile( "unknown.txt" )
# unknown_tm.createAllDictionaries(text_unk)
# unknown_tm.printAllDictionaries()

# unknown_tm.compareTextWithTwoModels(trained_tm1,trained_tm2)

