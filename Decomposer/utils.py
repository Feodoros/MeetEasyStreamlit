import re
from datetime import timedelta, datetime
import pymorphy2
import random
from keybert import KeyBERT
from collections import defaultdict
from Decomposer.matcher import *
from googletrans import Translator
import json
import openai
import streamlit as st

translator = Translator()

kw_model = KeyBERT()
morph = pymorphy2.MorphAnalyzer()


def process_json(transcript_json):
    
    if 'text' in transcript_json.keys():
        return transcript_json['text']
        
    else:
        text = ''
        for message in transcript_json['message_list']:
            text += message['text'] + '. '
        return text


def split_text_by_speaker(transcript_json):
    
    texts_by_speaker = defaultdict(str)

    for message in transcript_json['message_list']:
        texts_by_speaker[message['speaker']]+=" "+message['text'].lower()
                
    return texts_by_speaker


def get_tasks(transcript_json, doc, nlp, dep_matcher, dep_matches):
    
    text = process_json(transcript_json)

    tasks = []

    for i, match in enumerate(dep_matches):
        pattern_name = match[0]
        matches = match[1]
        
#         if nlp.vocab[pattern_name].text == 'imperative':
#             tasks.append(doc[matches[0]].text.lower()+' '+join_dependant_tokens(1, doc, matches))

        if nlp.vocab[pattern_name].text in ['task', 'need', 'want',"could_you"]:
            tasks.append(join_dependant_tokens(1, doc, matches))
            
        if nlp.vocab[pattern_name].text == 'strong_do':
            
            tasks.append(doc[matches[0]].text+' '+join_dependant_tokens(3, doc, matches))
            
        if nlp.vocab[pattern_name].text in ['weekday', 'time', 'remind']:
            tasks.append(join_dependant_tokens(0, doc, matches).lower().replace('.',''))

    return list(set(tasks))


def get_personal_tasks(transcript_json, doc, nlp, dep_matcher, dep_matches):
    
    tasks_by_speaker = {}
    
    texts_by_speaker = split_text_by_speaker(transcript_json)
    
    for key in texts_by_speaker.keys():
        
        tasks = []
        doc = nlp(texts_by_speaker[key])
        dep_matches = dep_matcher(doc)
        
        for i, match in enumerate(dep_matches):
            pattern_name = match[0]
            matches = match[1]
            
            if nlp.vocab[pattern_name].text == 'imperative':
                tasks.append(doc[matches[0]].text.lower()+' '+join_dependant_tokens(1, doc, matches))
            
            if nlp.vocab[pattern_name].text in ['task','need','want',"could_you"]:
                
                tasks.append(join_dependant_tokens(1, doc, matches))
    
            if nlp.vocab[pattern_name].text == 'strong_do':

                tasks.append(morph.parse(doc[matches[0]].text)[0].normal_form+' '+join_dependant_tokens(3, doc, matches))
                         
            if nlp.vocab[pattern_name].text in ['weekday', 'time', 'remind']:
                tasks.append(join_dependant_tokens(0, doc, matches).lower().replace('.',''))

        tasks_by_speaker[key] = list(set(tasks))
        
    return tasks_by_speaker


def get_en_tasks(transcript_json, nlp, dep_matcher):
    
    tasks_by_speaker = {}
    
    texts_by_speaker = split_text_by_speaker(transcript_json)
    
    for key in texts_by_speaker.keys():
        
        tasks = []
        doc = nlp(texts_by_speaker[key])
        dep_matches = dep_matcher(doc)
        
        for i, match in enumerate(dep_matches):
            pattern_name = match[0]
            matches = match[1]
            
            if nlp.vocab[pattern_name].text in ['task','need', "could_you"]:
                
                output = sorted([matches[0], matches[1]])
                tasks.append(["..." + doc[output[0] - 6: output[0]].text, doc[output[0]].text,
                                 doc[output[0]+1:output[1]].text, doc[output[1]].text, doc[output[1]+1: output[1] + 15].text+"..."])
        tasks_by_speaker[key] = tasks
        
    return tasks_by_speaker


def colour(message, nlp, dep_matcher):
    doc = nlp(message['text'])
    dep_matches = dep_matcher(doc)
    coloured_list = []
    output = []
    for match in dep_matches:
        if nlp.vocab[match[0]].text in ['task','need','want',"could_you", 'imperative', 'weekday', 'time', 'remind', 'strong_do']:
            matches = match[1]
            output+=sorted(matches)

    point = 0

    for match_i in output:
        coloured_list+=[doc[point: match_i].text, doc[match_i].text]
        point = match_i+1
    return coloured_list+[doc[point:].text]


def get_assembly_summary(transcript_json, nlp, dep_matcher, lang):
    
    print(transcript_json)
    chapters = []
    for i, chapter in enumerate(transcript_json['chapters']):
        if i < 3: 
            chapter['headline'] = chapter['gist']
        if chapter['start']:
            start_id = message_list_range(transcript_json['message_list'], timedelta(milliseconds=chapter['start']), 'start_time')
            end_id = message_list_range(transcript_json['message_list'], timedelta(milliseconds=chapter['end']), 'end_time')
            chapter['message_list'] = transcript_json['message_list'][start_id:end_id+1]
        else:
            chapter['message_list'] = transcript_json['message_list']
        for message in chapter['message_list']:
            message['coloured'] = colour(message, nlp, dep_matcher)

    return transcript_json


def request_gpt3_summary(text, prompt, lang):
    openai_api_key = random.choice(st.secrets['my_cool_secrets']['openai_api_keys'])
    try:
        response = openai.Completion.create(
          engine="davinci-instruct-beta",
          prompt=text+prompt,
          temperature=0,
          max_tokens=100,
          top_p=1,
          frequency_penalty=1
        )

        print(response['choices'][0]['text'], translator.translate(response['choices'][0]['text'],src='en', dest=lang).text if translator.detect(response['choices'][0]['text']).lang=='en' else "")

        summary = translator.translate(response['choices'][0]['text'],src='en', dest=lang).text if translator.detect(response['choices'][0]['text']).lang=='en' else ""

    except:
        response = openai.Completion.create(
          engine="davinci-instruct-beta",
          prompt=text[:int(len(text)/2)]+prompt,
          temperature=0,
          max_tokens=100,
          top_p=1,
          frequency_penalty=1
        )
        summary = translator.translate(response['choices'][0]['text'],src='en', dest=lang).text if translator.detect(response['choices'][0]['text']).lang=='en' else ""

    return summary

def request_summary(transcript_json, nlp, dep_matcher, lang):
    n=20
    chunks = [("\n".join([jsn['start_time']+" "+jsn['text'] for jsn in transcript_json['message_list'][i:i+n]]), transcript_json['message_list'][i:i+n]) for i in range(0, len(transcript_json['message_list']), n)]
    chapters = [{'summary': '', 'headline': '','gist': '<gist>', 'text':'','message_list': []} for e in range(len(chunks))]
    i=0
    for text, message_list in chunks:
            summary = request_gpt3_summary(text, prompt='\n\nSummarise in 5 lines or less', lang=lang)
            headline = request_gpt3_summary(text, prompt='\n\nSummarise in 1 line', lang=lang)
            if summary:
                chapters[i]['summary']+=summary
                chapters[i]['text']+=text
                chapters[i]['message_list']+=message_list
                chapters[i]['headline']=headline
                i+=1

            else:
                chapters[i]['text']+=text
                chapters[i]['message_list']+=message_list

    transcript_json['chapters'] = chapters[:i] 
    for chapter in transcript_json['chapters']:
        for message in chapter['message_list']:
            message['coloured'] = colour(message, nlp, dep_matcher)

    return transcript_json


def get_en_summary(text, doc, nlp, dep_matches, lang):

    been_done = defaultdict(list)
    strong_been_done = []
    discussed = []
    plans = []
    summary_done = ''
    summary_plan = ''

    for i, match in enumerate(dep_matches):
        pattern_name = match[0]
        matches = match[1]
        if nlp.vocab[pattern_name].text == 'strong_been_done' and len(matches) > 2:

            if doc[matches[0]]._.inflect("VBN"):

                been_done[doc[matches[0]]._.inflect("VBN")].append(doc[matches[2]])

        elif nlp.vocab[pattern_name].text == 'need' and len(matches) > 3:
            
            plans.append(join_dependant_tokens(1, doc, matches))

        elif nlp.vocab[pattern_name].text == 'discuss':

            discussed.append(join_dependant_tokens(1, doc, matches))
    
    for key in been_done.keys():
        subjects = list(set([noun.text for noun in been_done[key]]))
        strong_been_done.append("the "+ join_phrases(subjects, lang, upper=False)[:-1] +' '+['were' if len(subjects)>1 else num_map[lang][been_done[key][0].morph.get("Number")[0]]][0]+" "+key)
        
    if plans:
        summary_plan += '\n'+random.choice(plan_phrases[lang])+' '+join_phrases(plans, lang, upper=False)

    if discussed:
        return random.choice(discussed_phrases[lang])+' ' + join_phrases(discussed, lang, upper=False)+'\n' +join_phrases(strong_been_done, lang)+' '+summary_plan
    else:
        return join_phrases(strong_been_done, lang)+' '+summary_plan


def get_BEEN_DONE(text, doc, nlp, dep_matches):

    extracts_list = []

    for i, match in enumerate(dep_matches):
        pattern_name = match[0]
        matches = match[1]
        if nlp.vocab[pattern_name].text in ['been_done'] and len(matches) > 2:

            output = sorted([matches[0], matches[1], matches[2]])

            extracts_list.append(["..." + doc[output[0] - 6: output[0]].text, doc[output[0]].text, doc[output[0]+1:output[1]].text,
                                 doc[output[1]].text, doc[output[1]+1:output[2]].text, doc[output[2]].text, doc[output[2]+1:output[2]+10].text+"..."])

    return extracts_list


def get_TODO(text, doc, nlp, dep_matches):

    extracts_list = []

    for i, match in enumerate(dep_matches):
        pattern_name = match[0]
        matches = match[1]

        if nlp.vocab[pattern_name].text in ['nsubj_verb_dobj', 'strong_do'] and len(matches) > 3:

            output = sorted([matches[0], matches[1], matches[2], matches[3]])
            extracts_list.append(["..." + doc[output[0] - 6: output[0]].text, doc[output[0]].text, doc[output[0]+1:output[1]].text, doc[output[1]].text,
                                 doc[output[1]+1:output[2]].text, doc[output[2]].text, doc[output[2]+1:output[3]].text, doc[output[3]].text, doc[output[3]+1: output[3] + 15].text+"..."])

        elif nlp.vocab[pattern_name].text in ["can", "today",'want'] and len(matches) > 1:

            output = sorted([matches[0], matches[1]])
            extracts_list.append(["..." + doc[output[0] - 6: output[0]].text, doc[output[0]].text,
                                 doc[output[0]+1:output[1]].text, doc[output[1]].text, doc[output[1]+1: output[1] + 15].text+"..."])

    return extracts_list


def get_keywords(text):

    return []


def get_en_keywords(text):

    keywords = kw_model.extract_keywords(text)[:3]

    return [keyword[0] for i, keyword in enumerate(keywords)]


def extract_dependant_tokens(tokens, dependant_tokens):

    new_dependant_tokens = {}
    for key, value in dependant_tokens.items():
        head_id = key

        for token in tokens:
            if token.head.i == head_id and token.text:
                new_dependant_tokens[token.i] = token.text
    return new_dependant_tokens


def join_dependant_tokens(root_idx, doc, matches):

    tasks = {}
    dependant_tokens = {matches[root_idx]: doc[matches[root_idx]].text}
    tasks[doc[matches[root_idx]].text] = dependant_tokens
    while dependant_tokens:
        dependant_tokens = extract_dependant_tokens(doc, dependant_tokens)
        if dependant_tokens.items() <= tasks[doc[matches[root_idx]].text].items():
            break
        tasks[doc[matches[root_idx]].text].update(dependant_tokens)

    sentence = ' '.join([tasks[doc[matches[root_idx]].text][i]
                        for i in sorted(tasks[doc[matches[root_idx]].text])])

    return sentence


def join_phrases(phrases_list, lang, upper=True):

    sentence = ''
    if len(phrases_list) == 1:
        if upper:
            return phrases_list[0][0].upper() + phrases_list[0][1:]+'.'
        else:
            return phrases_list[0]+"."
    else:
        for i, phrase in enumerate(phrases_list):
            if upper and i == 0:
                sentence += phrase[0].upper() + phrase[1:]+', '

            elif i == len(phrases_list)-1:
                sentence += and_map[lang] +phrase+'.'

            elif i == len(phrases_list)-2:
                sentence += phrase+' '

            else:
                sentence += phrase+', '

        return sentence


def message_list_range(message_list, time_point, key):
    for i, message_json in enumerate(message_list):
        delta = timedelta(hours=datetime.strptime(message_json[key],'%H:%M:%S').hour, minutes=datetime.strptime(message_json[key],'%H:%M:%S').minute, seconds=datetime.strptime(message_json[key],'%H:%M:%S').second)
        if message_json[key]==str(time_point).split(".")[0] or delta>time_point:
            return i
