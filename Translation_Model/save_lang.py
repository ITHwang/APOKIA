import preprocessing
import pickle

input_lang, output_lang, pairs = \
    preprocessing.prepareData('../kor_eng.txt', 'kor', 'eng', 32, False)

with open("input_lang.lq", "wb") as f:
    pickle.dump(input_lang, f)

with open("output_lang.lq", "wb") as f:
    pickle.dump(output_lang, f)

