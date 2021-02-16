from collections import Counter
<<<<<<< HEAD
import numba
=======
from sklearn.feature_extraction import DictVectorizer
>>>>>>> 5f6e015667966fee372b17c4b0d8a9e1147e4927
import numpy as np


def get_data():
    with open('dat410_europarl/europarl-v7.sv-en.lc.en', 'r') as f:
        lines_en = f.readlines()
    with open('dat410_europarl/europarl-v7.sv-en.lc.sv', 'r') as f:
        lines_sv = f.readlines()
    return lines_en, lines_sv


def process_data(lang1, lang2):
    lang1_mat = []
    lang2_mat = []
<<<<<<< HEAD
    characters = [',', '.', '-', '(', ')', '!', '?']
    for line1, line2 in zip(lang1, lang2):
        tmp1 = [word for word in line1.split() if word not in characters]
        tmp2 = [word for word in line2.split() if word not in characters]
=======
    for line1, line2 in zip(lang1, lang2):
        tmp1 = [
            word for word in line1.split()
            if word != ',' and word != '.' and word != '-' and word != '('
            and word != ')' and word != '!' and word != '?'
        ]
        tmp2 = [
            word for word in line2.split()
            if word != ',' and word != '.' and word != '-' and word != '('
            and word != ')' and word != '!' and word != '?'
        ]
>>>>>>> 5f6e015667966fee372b17c4b0d8a9e1147e4927
        lang1_mat.append(tmp1)
        lang2_mat.append(tmp2)
    return lang1_mat, lang2_mat


def mat_len(mat):
    lenght = 0
    for row in mat:
        lenght += len(row)
    return lenght


def get_counts(lan_mat):
    # warmup
    c = Counter()
    for line in lan_mat:
        c.update(line)
    return c


def warmup():
    en, sv = get_data()
    en_mat, sv_mat = process_data(en, sv)
    c_en = get_counts(en_mat)
    c_sv = get_counts(sv_mat)
<<<<<<< HEAD
    print('Most common swedish words:')
    for word, count in c_sv.most_common(10):
        print(f'{word}: {count}')
    print('Most common english words:')
    for word, count in c_en.most_common(10):
        print(f'{word}: {count}')
=======

    print('Most common swedish words:')
    for word, count in c_sv.most_common(10):
        print(f'{word}: {count}')

    print('Most common english words:')
    for word, count in c_en.most_common(10):
        print(f'{word}: {count}')

>>>>>>> 5f6e015667966fee372b17c4b0d8a9e1147e4927
    en_words = mat_len(en_mat)
    speaker = c_en['speaker']
    zebra = c_en['zebra']
    print(f'P(speaker) = {speaker}/{en_words} = {speaker/en_words}')
    print(f'P(zebra) = {zebra}/{en_words} = {zebra / en_words}')


def get_following_word(looking_for, mat):
    followed_by = []
    for line in mat:
        for ind, word in enumerate(line):
            if (looking_for == word):
                if ind < len(line) - 1:
                    followed_by.append(line[ind + 1])
                else:
                    followed_by.append('$')
    return followed_by


def bigram_prob(word1, word2, mat):
    if word1 == '^':
        #c = get_counts(mat)
        #return c[word2]/mat_len(mat)
        words = []
        for ind in range(len(mat)):
            if mat[ind] != []:
                words.append(mat[ind][0])
    else:
        words = get_following_word(word1, mat)
    hits = len([x for x in words if x == word2])
    prob = hits / len(words)
    return prob


def prob_sentence(sentence, mat):
    prob = 1
    copy = sentence.copy()
    copy.insert(0, '^')
    for ind in range(len(copy) - 1):
        curr_prob = max(bigram_prob(copy[ind], copy[ind + 1], mat), 1e-6)
        prob *= curr_prob
    return prob


def get_words(mat):
    word_list = []
    for sent in mat:
        for word in sent:
            if (word not in word_list):
                word_list.append(word)
<<<<<<< HEAD
    word_list.insert(0, 'NULL')
    return word_list


def em(tx, t, c_sv_en, c_en, en_mat, sv_mat, en_dic, sv_dic):
    #mat1 = en, mat2 = sv
    for it, (en_sent, sv_sent) in enumerate(zip(en_mat, sv_mat)):
        print(f'iteration {it}, {tx}')
        for sv_word in sv_sent:  # for each sve word
            ix = sv_dic.index(sv_word)
            for en_word in en_sent:  # for each eng word
                jx = en_dic.index(en_word)
                en_ind = [en_dic.index(wx) for wx in en_sent]
                en_ind.insert(0, 0)
                en_ind = np.array(en_ind)  # add null word
                denominator = np.sum(t[ix][en_ind])
                nominator = t[ix][jx]
                delta = nominator / denominator
                c_sv_en[ix][jx] += delta
                c_en[0][jx] += delta
    return c_sv_en, c_en


@numba.njit(fastmath=True, parallel=True)
def calc(ix, en_sent, en_dic, sv_dic, t, c_sv_en, c_en):
    for en_word in en_sent:  # for each eng word
        jx = en_dic.index(en_word)
        en_ind = [en_dic.index(wx) for wx in en_sent]
        en_ind.insert(0, 0)
        en_ind = np.array(en_ind)  # add null word
        denominator = np.sum(t[ix][en_ind])
        nominator = t[ix][jx]
        delta = nominator / denominator
        c_sv_en[ix][jx] += delta
        c_en[0][jx] += delta
    return None
=======
    return word_list


def EM(t, mat1, mat2, words1, words2):
    #mat1 = en, mat2 = sv
    for sent1, sent2 in zip(mat1, mat2):
        lk = len(sent1)  # lenght of eng sentence
        mk = len(sent2)  # lenght of sve sentence
        for ix, word2 in enumerate(sent2):  # for each sve word
            for jx, word1 in enumerate(sent1):  # for each eng word
                ind2 = [sv.index(wx) for wx in word2]
                denominator = np.sum([t[ix][en.index(word1)] for ix in ind2])
                delta = t[sv.index(word2)][en.index(word1)] / denominator

    return t
>>>>>>> 5f6e015667966fee372b17c4b0d8a9e1147e4927


def main():
    #warmup()
    print('loading data')
    en_raw, sv_raw = get_data()
<<<<<<< HEAD
    print('process_data')
    en_mat, sv_mat = process_data(en_raw, sv_raw)
    print('counting words')
    en = get_words(en_mat)
    sv = get_words(sv_mat)
    t = np.random.rand(len(sv), len(en))
    k = 10
    for tx in range(k):
        print(f'em iteration {tx}')
        c_sv_en = np.zeros([len(sv), len(en)])
        c_en = np.zeros([1, len(en)])
        c_sv_en, c_en = em(tx, t, c_sv_en, c_en, en_mat, sv_mat, en, sv)
        t = c_sv_en / c_en
        f_name = f't_{tx}'
        np.save(f_name, t)
    np.save('t', t)
=======

    print('process_data')
    en_mat, sv_mat = process_data(en_raw, sv_raw)

    print('counting words')
    en = get_words(en_mat)
    sv = get_words(sv_mat)

    t = np.random.rand(len(sv), len(en))

    K = 10
    for tx in range(K):
        t = EM(t, en_mat, sv_mat, en, sv)
>>>>>>> 5f6e015667966fee372b17c4b0d8a9e1147e4927


if __name__ == "__main__":
    main()
