import re
import json

male_words = ['شىء', 'مكعب']
female_words = ['كرة', 'اسطوانة', 'كرات', 'مكعبات', 'اسطوانات', 'أشياء']

female_male_dict = {'توجد': 'يوجد',
                    'هى': 'هو',
                    'لها': 'له',
                    'التى': 'الذى',
                    'مصنوعة': 'مصنوع',
                    'صنعت': 'صنع',
                    'ضخمة': 'ضخم',
                    'كبيرة': 'كبير',
                    'صغيرة': 'صغير',
                    'ضئيلة': 'ضئيل',
                    'لامعة': 'لامع',
                    'معدنية': 'معدنى',
                    'مطاطية': 'مطاطى',
                    'رمادية': 'رمادى',
                    'حمراء': 'أحمر',
                    'زرقاء': 'أزرق',
                    'خضراء': 'أخضر',
                    'بنية': 'بنى',
                    'بنفسجية': 'بنفسجى',
                    'لبنية': 'لبنى',
                    'صفراء': 'أصفر'}


def split_by_list(txt, seps):
    """
    :param txt: text to be split
    :param seps: list of separators
    :return: List including the separators
    """
    seps_str = '(' + '|'.join(seps) + ')'
    return re.split(seps_str, txt)


def change_text_gender_to_male(txt):
    """
    :param txt: input string
    :return: the same text with genders changed from female to male
    """

    # Some strings are left with gender unchanged and it is included in the below list
    # like:  'ما هى المادة التى', 'ما هى المادة'
    words = split_by_list(txt, ['ما هى المادة التى',
                                'ما هى المادة',
                                'ما هى مادة',
                                ' ',
                                '\؟',
                                'التى',
                                'ال'])
    for idx, word in enumerate(words):
        if word in female_male_dict.keys():
            words[idx] = female_male_dict[word]
        elif word.endswith('ها'):
            words[idx] = word[:-1]
    return ''.join(words)


def correct_single_word_errors(txt):
    # Replace any ال with a white space char after it with a white space only
    # Replace any ال with a ? char after it with a ? only
    # Replace any شىءات with أشياء
    # Replace any شىءة with شىء
    # Replace any مكعبة with مكعب
    txt = txt.replace('ال ', ' '). \
        replace('ال;', ';'). \
        replace('ال؟', '؟'). \
        replace('شىءات', 'أشياء'). \
        replace('شىءة', 'شىء'). \
        replace('مكعبة', 'مكعب')
    # Remove duplicated white spaces
    txt = re.sub(' +', ' ', txt)
    return txt


def correct_grammar_errors(q_str):
    all_words_to_split_on = female_words + male_words

    # list after splitting
    lst = split_by_list(q_str, all_words_to_split_on + [';'])

    """
    Correct the first item in the list if the one following it is male
    for example:  توجد مكعب  -> يوجد مكعب
    """
    the_first_part_after_semicolon_is_male = False
    if len(lst) > 1 and lst[1] in male_words:
        lst[0] = change_text_gender_to_male(lst[0])
        the_first_part_after_semicolon_is_male = True

    """
    Iterate on the list of split question string. If a male word is found, mark a boolean (change_to_male) as true
    so the next item will be changed to male
    """
    change_to_male = False
    for idx, item in enumerate(lst):
        if change_to_male:
            lst[idx] = change_text_gender_to_male(item)
            change_to_male = False
        if item in male_words or (item == ';' and the_first_part_after_semicolon_is_male):
            change_to_male = True
        if item == ';' and the_first_part_after_semicolon_is_male == False:
            change_to_male = False

    return ''.join(lst)


def correct_errors(q_str):
    single_word_corrected_question = correct_single_word_errors(q_str)
    grammar_corrected_question = correct_grammar_errors(single_word_corrected_question)
    return grammar_corrected_question


with open(r'J:\vqa\AR-CLEVR\question_generation\ar_qs.json', encoding='utf-8') as f:
    dic = json.load(f)
    questions = dic['questions']
    for idx, q in enumerate(questions):
        q['question'] = correct_errors(q['question'])
        # For debugging purposes, print the corrected question and its index in the json, you can pass this
        # index to the test_idx method defined below to retrieve the original (non corrected question) and debug
        print(idx, q['question'])
        questions[idx] = q
    dic['questions'] = questions

with open(r'J:\vqa\AR-CLEVR\question_generation\qr_qs_cor.json', 'w', encoding='utf-8') as f:
    json.dump(dic, f, ensure_ascii=False)


def test_idx(idx):
    with open(r'J:\vqa\ARCLEVR\question_generation\ar_qs.json', encoding='utf-8') as f:
        dic = json.load(f)
        questions = dic['questions']
        return questions[idx]['question']
