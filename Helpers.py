from nltk.tokenize import word_tokenize
import json


def n_gram_maker(text, n):
    words = word_tokenize(text)
    n_gram_list = []
    for i in range(len(words)):
        n_gram = []
        for j in range(i, i + n):
            if j < len(words):
                n_gram.append(words[j])
        n_gram_list.append(n_gram)
    return n_gram_list


def word_count_party(start_file_num, end_file_num):
    word_count_demo = {}
    word_count_rep = {}
    for i in range(start_file_num, end_file_num + 1):
        if i < 100:
            cleaned_path = "data/cleaned/0" + str(i) + "_speeches_party_map.json"
        else:
            cleaned_path = "data/cleaned/" + str(i) + "_speeches_party_map.json"
        with open(cleaned_path, "r") as file:
            data = json.load(file)
            for speech in data:
                if speech["speaker_party"] == "R":
                    tokens = word_tokenize(speech["text"].lower())
                    for token in tokens:
                        if token in word_count_rep:
                            word_count_rep[token] += 1
                        else:
                            word_count_rep[token] = 1
                elif speech["speaker_party"] == "D":
                    tokens = word_tokenize(speech["text"].lower())
                    for token in tokens:
                        if token in word_count_demo:
                            word_count_demo[token] += 1
                        else:
                            word_count_demo[token] = 1
    with open("wordCountDemo.txt", "w") as file:
        sorted_word_count = sorted(word_count_demo.items(), key=lambda x: x[1], reverse=True)
        file.write(json.dumps(sorted_word_count))
        with open("wordCountRep.txt", "w") as file:
            sorted_word_count = sorted(word_count_rep.items(), key=lambda x: x[1], reverse=True)
            file.write(json.dumps(sorted_word_count))


if __name__ == '__main__':
    word_count_party(97, 114)
