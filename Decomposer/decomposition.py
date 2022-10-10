from Decomposer.utils import *
from Decomposer.matcher import *
import spacy
from spacy.matcher import Matcher, DependencyMatcher
from langdetect import detect
import pyinflect

functions_matcher = {'ru': {'topic': get_keywords,
                            'summary': request_summary,
                            'task': get_personal_tasks,
                            },
                     'en': {'topic': get_en_keywords,
                            'summary': get_en_summary,
                            'task': get_personal_tasks,
                            },
                     'de': {'topic': get_en_keywords,
                            'summary': get_en_summary,
                            'task': lambda *args: None,
                           },
                     'es': {'topic': get_en_keywords,
                            'summary': get_en_summary,
                            'task': lambda *args: None,
                           }
                    }


def decompose(transcript_json, lang):

    text = process_json(transcript_json)

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
    transcript_json['task'] = functions_matcher[lang]['task'](transcript_json, doc, nlp, dep_matcher, dep_matches)
    transcript_json = functions_matcher[lang]['summary'](transcript_json, nlp, dep_matcher, lang)
    

    return transcript_json
