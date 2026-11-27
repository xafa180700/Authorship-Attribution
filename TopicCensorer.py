import json
from nltk.tokenize import word_tokenize
import re
import time
import multiprocessing


def text_censorer(text, censor_list):
    for word in censor_list:
        text = re.sub(FR"\b({word})(?=\W)", 'TOPICWORD', text)
    return text


def count():
    from nltk.corpus import stopwords
    stopwords = set(stopwords.words('english'))
    word_count = {}
    for i in range(97, 115):
        print("count: " + str(i))
        if i < 100:
            censored_path = "data/censored/0" + str(i) + "_speeches_party_map.json"
        else:
            censored_path = "data/censored/" + str(i) + "_speeches_party_map.json"

        with open(censored_path, "r") as file:
            data = json.load(file)
            for speech in data:
                text = speech["text"]
                tokens = word_tokenize(text.lower())
                for token in tokens:
                    if token in word_count:
                        word_count[token] += 1
                    else:
                        word_count[token] = 1
    for word in stopwords:
        if word in word_count:
            word_count.pop(word)
    with open("wordCount.txt", "w") as file:
        sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        file.write(json.dumps(sorted_word_count))


def censor_files(start_file_num, end_file_num):
    topic_words = []
    with open("TopicWords.txt", "r") as file:
        for line in file:
            topic_words.append(line.strip())
    len_list = len(topic_words)
    topic_words = set(topic_words)
    len_set = len(topic_words)
    delta_len = len_list - len_set
    print("number of duplicate topic words: " + str(delta_len))
    print("number of unique topic words: " + str(len_set))
    for i in range(start_file_num, end_file_num + 1):
        print("censoring: " + str(i))
        if i < 100:
            cleaned_path = "data/cleaned/0" + str(i) + "_speeches_party_map.json"
            censored_path = "data/censored/0" + str(i) + "_speeches_party_map.json"
        else:
            cleaned_path = "data/cleaned/" + str(i) + "_speeches_party_map.json"
            censored_path = "data/censored/" + str(i) + "_speeches_party_map.json"
        with open(cleaned_path, "r") as file:
            data = json.load(file)
            s = time.time()
            for speech in data:
                text = speech["text"]
                censored_text = text_censorer(text, topic_words)
                speech["text"] = censored_text
            e = time.time()
            print(f"censored file {i} in {(e - s) / 60} minutes")
        with open(censored_path, "w") as file:
            json.dump(data, file, indent=4)


# needs about 3-ish GB of RAM
def multi_process_censorer():
    p1 = multiprocessing.Process(target=censor_files, args=(97, 99))
    p2 = multiprocessing.Process(target=censor_files, args=(100, 102))
    p3 = multiprocessing.Process(target=censor_files, args=(103, 105))
    p4 = multiprocessing.Process(target=censor_files, args=(106, 108))
    p5 = multiprocessing.Process(target=censor_files, args=(109, 111))
    p6 = multiprocessing.Process(target=censor_files, args=(112, 114))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    print("multiprocessing done")


if __name__ == '__main__':
    start_time = time.time()
    multi_process_censorer()
    censored_time = time.time()
    print(f"censored topic words in {(censored_time - start_time) / 60} minutes")
    count()
    end_time = time.time()
    print(f"counted in {(end_time - censored_time) / 60} minutes")
    print(f"total run time: {(end_time - start_time) / 60} minutes")
