import pandas as pd
import re
from itertools import combinations


def get_data_from_xlsx():
    excel_data = pd.read_excel("file.xlsx", header=None)
    return pd.DataFrame(excel_data)


def delete_header_row(df):
    df_without_header_row = df.drop(df.index[0])
    return df_without_header_row


def get_grouped_sentences(df, index):
    original_dialogs = df[index].tolist()
    original_dialogs = list(map(lambda d: str(d), original_dialogs))

    grouped_sentences = []

    for dialog in original_dialogs:
        grouped_sentences.append(get_dialog_sentences(dialog))

    return grouped_sentences


def get_dialog_sentences(dialog):
    sentences = []

    client_dialogs = re.findall(r'CLIENT:(.+?)BOT:', dialog + "BOT:", re.DOTALL)

    if len(client_dialogs) == 0:
        sentences.append(dialog)
    else:
        client_dialogs = get_client_dialogs(client_dialogs)

        for client_dialog in client_dialogs:
            client_sentences = client_dialog.split(".")
            sentences = sentences + client_sentences

    sentences = list(map(lambda d: d.strip(), sentences))
    sentences = list(filter(lambda d: d != '', sentences))

    return sentences


def get_client_dialogs(dialogs):
    delimiter_chars = ['?', '!', '.', '\n', 'CLIENT:']

    client_dialogs = []

    for dialog in dialogs:
        filtered_dialog = dialog

        for char in delimiter_chars:
            filtered_dialog = filtered_dialog.replace(char, ".")

        filtered_dialog = filtered_dialog.strip()
        filtered_dialog = re.sub(r"[:,'\";<>\\/`~#%^&*()+]", "", filtered_dialog)
        client_dialogs.append(filtered_dialog.lower())

    return client_dialogs


def get_words_from_sentence(sentence):
    words = list(map(lambda word: word.strip('‌ '), sentence.split(' ')))
    return list(filter(lambda word: word != '', words))


def remove_short_words(words, max_short_word_len=4):
    return list(filter(lambda w: len(w) > max_short_word_len, words))


def get_outlying_phrases(grouped_sentences, phrase_word_count):
    phrases = []
    grouped_joined_sentences = []

    for group_sentences in grouped_sentences:
        grouped_joined_sentences.append(" ".join(group_sentences))

    for sentence in grouped_joined_sentences:
        words = remove_short_words(get_words_from_sentence(sentence))

        group_phrases = []

        for i in range(len(words)):
            tuple_phrases = set(combinations(words[i + 1:15], phrase_word_count - 1))

            for phrase in tuple_phrases:
                str_phrase = " ".join(phrase)
                group_phrases.append(words[i] + " " + str_phrase)

        phrases += set(group_phrases)

    return phrases


def get_nearby_phrases(grouped_sentences, phrase_word_count):
    phrases = []

    for group_sentences in grouped_sentences:
        group_phrases = set()

        for sentence in group_sentences:
            words = get_words_from_sentence(sentence)

            for i in range(len(words)):
                if i + phrase_word_count > len(words):
                    break

                phrase = " ".join(words[i:i + phrase_word_count])

                group_phrases.add(phrase)

        phrases = phrases + list(group_phrases)

    return phrases


def get_phrase_count_dict(phrases):
    phrase_count = {}

    for phrase in phrases:
        if phrase in phrase_count.keys():
            phrase_count[phrase] = phrase_count[phrase] + 1
        else:
            phrase_count[phrase] = 1

    return phrase_count


def sort_phrases(phrase_counts, sort_type="max"):
    reverse = True

    if sort_type == "min":
        reverse = False

    return sorted(phrase_counts.items(), key=lambda p: p[1], reverse=reverse)


