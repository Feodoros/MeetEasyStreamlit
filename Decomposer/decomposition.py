from Decomposer.utils import *
from Decomposer.matcher import *
from transformers import MBartTokenizer, MBartForConditionalGeneration
import spacy
from spacy.matcher import Matcher, DependencyMatcher
from langdetect import detect
import pyinflect

# summary_model_name = "IlyaGusev/mbart_ru_sum_gazeta"
# tokenizer = MBartTokenizer.from_pretrained(summary_model_name)
# summary_model = MBartForConditionalGeneration.from_pretrained(summary_model_name)


functions_matcher = {'ru': {'topic': get_keywords,
                            'summary': get_mbart_ru_summary,
                            'task': get_personal_tasks,
                            },
                     'en': {'topic': get_en_keywords,
                            'summary': get_en_summary,
                            'task': get_tasks,
                            }}


def decompose(transcript_json):

    text = process_json(transcript_json)
    lang = detect(text)

    nlp = spacy.load(model_matcher[lang])
    doc = nlp(text)
    dep_matcher = DependencyMatcher(vocab=nlp.vocab)

    for pattern_name in patterns.keys():
        if type(patterns[pattern_name][lang][0]) == list:
            dep_matcher.add(
                pattern_name, patterns=patterns[pattern_name][lang])
        else:
            dep_matcher.add(pattern_name, patterns=[
                            patterns[pattern_name][lang]])

    dep_matches = dep_matcher(doc)

    transcript_json['topic'] = functions_matcher[lang]['topic'](text)
    transcript_json['summary'] = functions_matcher[lang]['summary'](
        text, doc, nlp, dep_matches, lang)
    transcript_json['task'] = functions_matcher[lang]['task'](transcript_json, doc, nlp, dep_matcher, dep_matches)
    transcript_json['colored'] = {"BEEN DONE": get_BEEN_DONE(text, doc, nlp, dep_matches),
                                  "TODO": get_TODO(text, doc, nlp, dep_matches)}
    
    transcript_json = get_assembly_summary(transcript_json, nlp, dep_matcher, lang)

    return transcript_json
