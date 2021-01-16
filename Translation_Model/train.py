import preprocessing
import random
from layers import *
import trainer
import torch
import pickle

# once
input_lang, output_lang, pairs = \
    preprocessing.prepareData('../kor_eng.txt', 'kor', 'eng', 256, True)

with open("input_lang.lq", "rb") as f:
    input_lang = pickle.load(f)

with open("output_lang.lq", "rb") as f:
    output_lang = pickle.load(f)

lines = open("kor_eng_trunc.txt", 'r').read().strip().split('\n')
pairs = [[preprocessing.normalizeString(s) for s in l.split('\t')] for l in lines]

hidden_size = 512
encoder1 = EncoderRNN(input_lang.n_words, hidden_size)
attn_decoder1 = AttnDecoderRNN(hidden_size, output_lang.n_words, dropout_p=0.5)

if torch.cuda.is_available():
    encoder1 = encoder1.cuda()
    attn_decoder1 = attn_decoder1.cuda()

trainer.trainIters(pairs, input_lang, output_lang, encoder1, attn_decoder1, 200000)