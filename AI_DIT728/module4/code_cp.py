from collections import Counter
import numpy as np


# A function to collect the english and swedish translations
def get_data():
    #with open('dat410_europarl/en.txt', 'r') as f:  #
    with open('dat410_europarl/europarl-v7.sv-en.lc.en', 'r') as f:  #
        lines_en = f.readlines()
    #with open('dat410_europarl/sv.txt', 'r') as f:  #
    with open('dat410_europarl/europarl-v7.sv-en.lc.sv', 'r') as f:  #
        lines_sv = f.readlines()
    return lines_en, lines_sv


# Processing the data like removing special characters and tokanizing the
# sentances
def process_data(lang1, lang2):
    lang1_mat = []
    lang2_mat = []
    characters = [',', '.', '-', '(', ')', '!', '?']
    for line1, line2 in zip(lang1, lang2):
        tmp1 = [word for word in line1.split() if word not in characters]
        tmp2 = [word for word in line2.split() if word not in characters]
        lang1_mat.append(tmp1)
        lang2_mat.append(tmp2)
    return lang1_mat, lang2_mat


# function to compute the lengt of a matix, used to compute total number of
# words
def mat_len(mat):
    lenght = 0
    for row in mat:
        lenght += len(row)
    return lenght


# fits a counter to a language corpus
def get_counts(lan_mat):
    # warmup
    c = Counter()
    for line in lan_mat:
        c.update(line)
    return c


# Aswers the a) questions
def warmup():
    en, sv = get_data()
    en_mat, sv_mat = process_data(en, sv)
    c_en = get_counts(en_mat)
    c_sv = get_counts(sv_mat)
    print('Most common swedish words:')
    for word, count in c_sv.most_common(10):
        print(f'{word}: {count}')
    print('Most common english words:')
    for word, count in c_en.most_common(10):
        print(f'{word}: {count}')
    en_words = mat_len(en_mat)
    speaker = c_en['speaker']
    zebra = c_en['zebra']
    print(f'P(speaker) = {speaker}/{en_words} = {speaker/en_words}')
    print(f'P(zebra) = {zebra}/{en_words} = {zebra / en_words}')


# collects the distribution of following words
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


# computes the bigram
def bigram_prob(word1, word2, mat):
    if word1 == '^':  # ^ specifies that it is the first word
        words = []  # store all the starting words here
        for ind in range(len(mat)):  # for each sentence
            if mat[ind] != []:  # problems occured when sentences where empty
                words.append(mat[ind][0])
    else:
        words = get_following_word(word1, mat)
    hits = len([x for x in words if x == word2])
    prob = hits / len(words)
    return prob


# computes the bigram probabilty for a sentence
def prob_sentence(sentence, mat):
    prob = 1
    copy = sentence.copy(
    )  # have to copy so that we do not manipulate sentence
    copy.insert(0, '^')  # defining start of sentence
    for ind in range(len(copy) - 1):
        # next line computes the bigram probabilty, if it is lower then 1e-6
        # then we return 1e-6, this is an assumption so that the probabilty wont
        # be equal to 0
        curr_prob = max(bigram_prob(copy[ind], copy[ind + 1], mat), 1e-6)
        prob *= curr_prob
    return prob


# collects all the words in a corpus
def get_words(mat):
    word_list = []
    for sent in mat:  # for each sentence
        for word in sent:  # for each word
            if (word not in word_list):  # if it is a new word
                word_list.append(word)  # save new words
    word_list.insert(0, 'NULL')  # need the NULL token aswell
    return word_list


# a function that performes the em algorithm
def em(tx, t, c_sv_en, c_en, en_mat, sv_mat, en_dic, sv_dic):
    #mat1 = en, mat2 = sv
    for it, (en_sent, sv_sent) in enumerate(zip(en_mat, sv_mat)):
        print(f'iteration {it}, {tx}')
        en_sent.insert(0, 'NULL')
        for sv_word in sv_sent:  # for each sve word
            ix = sv_dic.index(sv_word)
            for en_word in en_sent:  # for each eng word
                jx = en_dic.index(en_word)
                en_ind = [en_dic.index(wx) for wx in en_sent]
                en_ind = np.array(en_ind)  # add null word
                denominator = np.sum(t[ix][en_ind])
                nominator = t[ix][jx]
                delta = nominator / denominator
                c_sv_en[ix][jx] += delta
                c_en[0][jx] += delta
    return c_sv_en, c_en


# this function computes t, it took about 12 hours to compute ten iterations
def compute_t():
    print('loading data')
    en_raw, sv_raw = get_data()
    print('process_data')
    en_mat, sv_mat = process_data(en_raw, sv_raw)
    print('counting words')
    en = get_words(en_mat)
    sv = get_words(sv_mat)
    # inializing t as random values
    len_sv = len(sv)
    len_en = len(en)
    t = np.random.rand(len_sv, len_en)
    # perforing the EM-algorithm with k iterations
    k = 10
    for tx in range(k):
        # takes so long, nice to see the counts
        print(f'em iteration {tx}')
        # inializing conditional probabilities
        c_sv_en = np.zeros([len_sv, len_en])  # conditional prob c(en|sv)
        c_en = np.zeros([1, len(en)])  # conditional prob c(en)
        # sending the data to the EM-algorithm
        c_sv_en, c_en = em(tx, t, c_sv_en, c_en, en_mat, sv_mat, en, sv)
        t = c_sv_en / c_en  # updates t
        # save t after update to local memory
        f_name = f't_{tx}'
        np.save(f_name, t)


# a function that returns the top contendors for a word
def get_top(x, t, en_dic, sv_dic, sv_word):
    ix = sv_dic.index(sv_word)  # swedish word index
    t = t[ix, :]
    # here we sort the indecies in increasing order, then we pick the last x of
    # then, lastly we invert the matrix so that we get the highest probible one
    # first
    top = np.argsort(t)[len(t) - x:][::-1]
    # extact thoose words
    words = [en_dic[ind] for ind in top]
    # extract the probabilities we will will use for the conditional one
    probs = t[top]
    tot_prob = np.sum(probs)
    return words, probs  #/ tot_prob  # return the conditional probabilty


# this funtion is similar to the one above, but it instead works on english and
# only prints out the top 10 words, this is to asnwer the question in c)
def top_10(t, en_dic, sv_dic, en_word):
    jx = en_dic.index(en_word)
    t = t[:, jx]
    top = np.argsort(t)[len(t) - 10:][::-1]
    # extact thoose words
    words = [sv_dic[ind] for ind in top]
    for word, it in zip(words, top):
        print(word, t[it])
    return None


# given the top n word candidates and their probabilities this function returns
# the most probable sentence
def best_translation(word_mat, prob_mat, en_mat):
    m = len(word_mat)  # number of words
    n = len(
        word_mat[0])  # how many translation conteders does one sentence have
    sent = []
    best_sent = []
    best_score = 0
    for it in range(m**n):  # for all positive conteders
        prob = 1
        ind = n_base(m, n, it)  # gets the index for each word
        for mt, nt in enumerate(ind):  # compute the probability of the word
            prob *= prob_mat[mt][nt]
        prob *= prob_sentence(sent, en_mat)
        if prob > best_score:
            for mt, nt in enumerate(ind):  # constuct the sentence
                sent.append(word_mat[mt][nt])
            best_score = prob  # update best_score
            best_sent = sent  # update best_sent
            sent = []  # reset sent
    return best_sent  # return the best translation


# this function writes an integer on base n and with lenght m, I did this to
# make it easier to loop through all possible sentences
def n_base(m, n, num):
    base_n = []
    for it in range(m):
        value = n**(m - 1 - it)
        base_n.append(int(num / value))
        num = num % value
    return base_n


# decodes an swedish sentence into an english one
def decoder(x, t, en_dic, sv_dic, en_mat, sv_sent):
    word_mat = []
    prob_mat = []
    for sv_word in sv_sent:
        # first we find all the candidates and their conditional probabilities
        words, probs = get_top(x, t, en_dic, sv_dic, sv_word)
        word_mat.append(words)
        prob_mat.append(probs)
    # then we return the best translation
    return best_translation(word_mat, prob_mat, en_mat)


# a function that lets the user input a swedish text from their terminal after
# running the program
def get_input(sv_dic):
    while (True):
        txt = input('Write an swedish sentance: ')
        txt = txt.split()
        sentance_supported = True
        for word in txt:
            sentance_supported *= word in sv_dic
            if (word not in sv_dic):
                print(
                    f'The word you used {word} is not supported, please try an alternative'
                )
        if sentance_supported:
            return txt


def main():
    warmup()  #remove comment to also run the warmup function to answer a)
    #compute_t() #takes a really long time

    # instead we load an already computed t-matrix
    t_9 = np.load('t/t_9.npy')

    # inializing
    en, sv = get_data()
    en_mat, sv_mat = process_data(en, sv)
    en_dic = get_words(en_mat)
    sv_dic = get_words(sv_mat)

    # now translations can be done in the terminal, ctrl-c to abort
    while (True):
        # gets user input, a swedish sentence that we will translate
        sv_sent = get_input(sv_dic)

        # decode the swedish into english
        translation = decoder(3, t_9, en_dic, sv_dic, en_mat, sv_sent)

        # prints the decoded sentence out
        print('In english that becomes:')
        print(translation)


if __name__ == "__main__":
    main()
