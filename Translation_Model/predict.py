import torch
import pickle
import sentence_predictor
import preprocessing

with open("input_lang.lq", "rb") as f:
    input_lang = pickle.load(f)

with open("output_lang.lq", "rb") as f:
    output_lang = pickle.load(f)

lines = open("kor_eng_trunc.txt", 'r').read().strip().split('\n')
pairs = [[preprocessing.normalizeString(s) for s in l.split('\t')] for l in lines]

device = torch.device('cuda')
encoder = torch.load("encoder.pt")
encoder.load_state_dict(torch.load("encoder_state_dict.pt"))
encoder.to(device)
decoder = torch.load("decoder.pt")
decoder.load_state_dict(torch.load("decoder_state_dict.pt"))
decoder.to(device)

def evaluate_sentences(input_lang, output_lang, pairs, encoder, decoder, sentences):
    n = len(sentences)
    for i in range(n):
        print('>', sentences[i])
        output_words, attentions = sentence_predictor.evaluate(input_lang, output_lang, encoder, decoder, sentences[i])
        output_sentence = ' '.join(output_words)
        print('<', output_sentence)
        print('')

sentence = "대한민국 서울특별시 용산구 용산동 2가 남산 공원 정상 부근에 위치한 전파 송출 및 관광용 타워" 
output_words, attentions = sentence_predictor.evaluate(input_lang, output_lang, encoder, decoder, sentence)
output_sentence = ' '.join(output_words)
print(output_sentence)



