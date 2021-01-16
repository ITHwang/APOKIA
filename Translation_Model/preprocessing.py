# https://9bow.github.io/PyTorch-tutorials-kr-0.3.1/intermediate/seq2seq_translation_tutorial.html
import unicodedata
import re

class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2
    
    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)
        
    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

def normalizeString(s):
    s = re.sub('[-=+,#/\?:^$.@*\"\'※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', s)
    return s

def readLangs(file_path, lang1, lang2, reverse=False):
    print("Reading lines...")

    lines = open(file_path, 'r').read().strip().split('\n')

    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]

    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)

    return input_lang, output_lang, pairs

def filterPair(p, maxlength):
    return len(p[0].split(' ')) < maxlength and \
        len(p[1].split(' ')) < maxlength

def filterPairs(pairs, maxlength):
    return [pair for pair in pairs if filterPair(pair, maxlength)]

def prepareData(file_path, lang1, lang2, maxlength, reverse=False):
    input_lang, output_lang, pairs = readLangs(file_path, lang1, lang2, reverse)
    print("Read %s sentence pairs" % len(pairs))
    pairs = filterPairs(pairs, maxlength)
    print("Trimmed to %s sentence pairs" % len(pairs))

    f = open("kor_eng_trunc.txt", 'w')
    for kor_sent, eng_sent in pairs:
        line = kor_sent + "\t" + eng_sent + "\n"
        f.write(line)
    f.close
    print("kor_eng_trunc.txt was saved")

    print("Counting words...")
    
    for i, pair in enumerate(pairs):
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
        if i % 100000 == 0:
            print("%d번째 완료" % i)

    print("counted words: ")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    
    return input_lang, output_lang, pairs







            
