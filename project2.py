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
        # you will want another dictionary for your text feature


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
        test_text = """This is a small sentence. This isn't a small sentence, because
        this sentence contains more than 10 words and a number! This isn't
        a question, is it?"""
        test_tm = TextModel( "Milestone test" )  # create a TextModel object
        text = test_tm.readTextFromFile( "test.txt" )
        print "Is text == test_text? ", text == test_text


    def makeSentenceLengths(self,s):
        """ should use the text in the input string s to create the self.sentencelengths dictionary """
        LoW = text.split()
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

        test_tm = TextModel( "Milestone test" )
        s = test_tm.readTextFromFile( "test.txt" )
        test_tm.makeSentenceLengths(text)
        print test_tm.sentencelengths

    def cleanString(self,s):
        """ should take in a string s and return a string with no punctuation and no upper-case letters """
        newstring = ''
        for i in range(len(s)):
            if s[i] not in '.,?!':
                newstring+=s[i].lower()
        return newstring

        test_tm = TextModel( "Milestone test" )
        s = test_tm.readTextFromFile( "test.txt" )
        clean_s = test_tm.cleanString(s)
        print clean_s

    def makeWordLengths(self,s):
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

    test_tm = TextModel( "Milestone test" )
    s = test_tm.readTextFromFile( "test.txt" )
    test_tm.makeWordLengths(s)
    print test_tm.wordlengths


