from Decomposer.utils import *
from Decomposer.matcher import *
import spacy
from spacy.matcher import Matcher, DependencyMatcher
from langdetect import detect
import pyinflect

# functions_matcher = {'ru': {'topic': lambda *args: [],
#                             'summary': request_summary,
#                             'task': get_gpt3_tasks,
#                             },
#                      'en': {'topic': get_en_keywords,
#                             'summary': get_assembly_summary,
#                             'task': get_personal_tasks,
#                             },
#                      'de': {'topic': lambda *args: [],
#                             'summary': request_summary,
#                             'task': get_gpt3_tasks,
#                            },
#                      'es': {'topic': lambda *args: [],
#                             'summary': request_summary,
#                             'task': get_gpt3_tasks,
#                            },
#                      'fr': {'topic': lambda *args: [],
#                             'summary': request_summary,
#                             'task': get_gpt3_tasks,
#                            }, 
#                      'it': {'topic': lambda *args: [],
#                             'summary': request_summary,
#                             'task': get_gpt3_tasks,
#                            }, 
#                      'pt': {'topic': lambda *args: [],
#                             'summary': request_summary,
#                             'task': get_gpt3_tasks,
#                            }, 
#                      'nl': {'topic': lambda *args: [],
#                             'summary': request_summary,
#                             'task': get_gpt3_tasks,
#                            }
#                     }


def decompose(transcript_json, lang):
    
    transcript_json = request_all(transcript_json, lang)

#     text = process_json(transcript_json)
#     try:
#         nlp = spacy.load(model_matcher[lang])
#         doc = nlp(text)
#         dep_matcher = DependencyMatcher(vocab=nlp.vocab)
        
#         for pattern_name in patterns.keys():
#             if type(patterns[pattern_name][lang][0]) == list:
#                 dep_matcher.add(
#                     pattern_name, patterns=patterns[pattern_name][lang])
#             else:
#                 dep_matcher.add(pattern_name, patterns=[
#                                 patterns[pattern_name][lang]])
#     except:
#         nlp = spacy.load(model_matcher['en'])
#         doc = nlp(text)
#         dep_matcher = DependencyMatcher(vocab=nlp.vocab)

    

#     dep_matches = dep_matcher(doc)

#     transcript_json['topic'] = functions_matcher[lang]['topic'](text)
#     transcript_json = functions_matcher[lang]['summary'](transcript_json, nlp, dep_matcher, lang)
#     transcript_json['task'] = functions_matcher[lang]['task'](transcript_json, doc, nlp, dep_matcher, dep_matches)
    

    return transcript_json
