import json


for i in range(97, 115):

    if i < 100:
        speaker_path = "data/raw/hein-daily/0" + str(i) + "_SpeakerMap.txt"
        speech_path = "data/raw/hein-daily/speeches_0" + str(i) + ".txt"
        cleaned_path = "data/cleaned/0" + str(i) + "_speeches_party_map.json"
    else:
        speaker_path = "data/raw/hein-daily/" + str(i) + "_SpeakerMap.txt"
        speech_path = "data/raw/hein-daily/speeches_" + str(i) + ".txt"
        cleaned_path = "data/cleaned/" + str(i) + "_speeches_party_map.json"

    speech_party_map = {}

    with open(speaker_path, "r") as speaker_file:
        next(speaker_file)
        for line in speaker_file:
            line_content = line.split("|")
            speech_party_map[line_content[1]] = line_content[7]

    with open(cleaned_path, "w") as cleaned_file:
        cleaned_file.write("[") #to make sure file is empty before apending below. and to make sure its properly formatted

    skipped_speeches = 0

    with open(speech_path, "r") as speech_file, open(cleaned_path, "a") as cleaned_file:
        next(speech_file)
        counter = 0
        try:
            for speech in speech_file:
                speech_content = speech.split("|")
                if speech_content[0] in speech_party_map:
                    d = {"speech_ID" : speech_content[0], "text" : speech_content[1], "speaker_party" : speech_party_map[speech_content[0]]}
                    if counter > 0:
                        cleaned_file.write(",")
                    json.dump(d, cleaned_file, indent=4)
                    counter+=1
        except UnicodeDecodeError:
            skipped_speeches += 1 #5 of the raw speech files contain 1 speech that throws an error, so i just skip those, since its not too much of a loss in data.
        cleaned_file.write("]")
    print(str(skipped_speeches) + " skipped in file: " + str(i))