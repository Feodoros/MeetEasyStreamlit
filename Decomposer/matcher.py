model_matcher = {'ru': 'ru_core_news_lg',
                 'en': 'en_core_web_sm'}

num_map = {'ru': {'Plur': 'были', 'Sing': 'был'},
           'en': {'Plur': 'were', 'Sing': 'was'}}

and_map = {'ru':'и ', "en":"and "}

gen_map = {'Fem': 'femn', 'Masc': 'masc', 'Neut': 'neut'}

plan_phrases = {'ru': ['Теперь нужно', "Дальше нужно", "Следующий этап:", "Далее:"],
                'en': ['We now need', "Now we need", "It's time", "Now it's time", "Next is", "Then is"]}

rus_stopwords = ['аа', 'слушай', "говоришь", 'клево', 'ща', 'привет', 'приветик', "допустим", "смотри",
                 'приду', 'секунду', 'разрешаю', 'нет', "типа", "угу", "ну", "чето", "да", "ааа", 'обсудить']
pron_stopwords = ["нибудь", "который", "я",
                  "ты", "он", "она", "они", "кое", "что", "это"]
verb_stopwords = ['told', 'said', 'had', 'loved', 'see', 'have', 'need','want', 'use','imagine', 'miss','tell','say','expect', 'consider', 'end']
noun_stopwords = ['kind', 'microphone', 'screen', 'moment', 'thing', 'one','ones','what', 'that', 'it','kinds','sorts','which','mic','microphones', 'minute', 'minutes', 'whatever']
discussed_phrases = {"en":["We have discussed"], "ru":["Обсуждали", "Обсудили"]}
summary_junk = ['Начну с того', 'В сегодняшнем обзоре я расскажу о том', 'В сегодняшнем обзоре мы поговорим о том', 'В преддверии новогодних праздников я решил поделиться своим мнением о том','В последнее время я очень много пишу о том','В очередной раз напишу про то', 'В очередной раз я хочу рассказать тебе о том','Представляешь']

patterns = {'imperative' : {
    'ru' : [{'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {"LOWER":{"NOT_IN": verb_stopwords},'POS': 'VERB',"IS_SENT_START":True, 'MORPH': {'IS_SUBSET': ['VerbForm=Inf','Tense=Pres']}}},
         {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'd_object', 'RIGHT_ATTRS': {'DEP': 'dobj','POS': 'NOUN'}}],
    'en' : [
        [{'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB',"IS_SENT_START":True, "LOWER":{"NOT_IN": verb_stopwords},'MORPH': {'IS_SUBSET': ['VerbForm=Inf','Tense=Pres']}}},
         {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'd_object', 'RIGHT_ATTRS': {'DEP': 'dobj','POS': 'NOUN',"LOWER":{"NOT_IN":noun_stopwords}}}
#                 ],
#         [
#     {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB', "ORTH":{"NOT_IN": verb_stopwords},'MORPH': {'IS_SUBSET':['VerbForm=Inf','Tense=Pres','VerbForm=Fin']}}},
#     {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'd_object', 'RIGHT_ATTRS': {'DEP': 'dobj','POS': 'NOUN',"LOWER":{"NOT_IN":noun_stopwords}}},
#     {'LEFT_ID': 'verb', 'REL_OP': ';', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','LOWER':{"IN" : ['you']}}},
#             {'LEFT_ID': 'subject', 'REL_OP': ';', 'RIGHT_ID': 'any', 'RIGHT_ATTRS': {'LOWER':{"NOT_IN" : ['if', 'when','once','would']}}}
        ]
    ]},
            'need' : {
        
        'ru' : [
            
    {'RIGHT_ID': 'advmod', 'RIGHT_ATTRS': {"LOWER": {"IN": ["нужно","надо","необходимо", "план", "планы", "планах","планирую","планируем", "собираюсь"]}}},
    {'LEFT_ID': 'advmod', 'REL_OP': '>', 'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'DEP': {"IN":['csubj', "nmod"]},'POS': 'VERB',"LOWER": {"NOT_IN":rus_stopwords}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': {"IN":['obj', "conj"]}, 'POS': {"IN":["NOUN", "PRON", "VERB"]}, "LOWER": {"NOT_IN":pron_stopwords}}}
                ],
        
        'en' : [
            
    {'RIGHT_ID': 'mod', 'RIGHT_ATTRS': {'POS': 'VERB',"LOWER": {"IN": ["need","have"]}}},
    {'LEFT_ID': 'mod', 'REL_OP': '>', 'RIGHT_ID': 'x_comp', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB', "LOWER":{"NOT_IN": verb_stopwords}}},
    {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {'DEP': 'aux','POS': 'PART'}},
    {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'c_comp', 'RIGHT_ATTRS': {'DEP': 'ccomp', 'POS': {"IN":["PRON", "NOUN", "VERB"]}, "LOWER": {"NOT_IN":pron_stopwords}}}
                ]
                     },
    'could_you' : {
        
        'ru' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {"LOWER": {"IN": ["можешь","могла","мог","могли", "можете"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'part', 'RIGHT_ATTRS': {'DEP': 'advmod',"LOWER": {"IN": ["ли", "бы"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'x_comp', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB'}}
                ],
        
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {"LOWER": {"IN": ["could"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj', 'POS': {"IN":["PRON"]},"LOWER": {"NOT_IN": ["it"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'x_comp', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB',"LOWER":{"NOT_IN": verb_stopwords}}}
                ]
                     },
    'appeared' : {
        
        'ru' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {"LOWER": {"IN": ["появился", "появились", "появилась"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj', 'POS': {"IN":["NOUN"], "NOT_IN":["PROPN"]}, "LOWER": {"NOT_IN":rus_stopwords}}}
                ],
        
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {"LOWER": {"IN": ["appeared"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj', 'POS': {"IN":["NOUN"]}}}
                ]
                     },
    'added' : {
        
        'ru' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {"LOWER": {"IN": ["добавил", "добавила", "добавили"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': {"IN":['obj','pobj', 'dobj']}, 'POS': {"IN":["NOUN"], "NOT_IN":["PROPN"]}, "LOWER": {"NOT_IN":rus_stopwords}}}
                ],
        
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {"LOWER": {"IN": ["added"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': {"IN":['obj','pobj', 'dobj']}, 'POS': {"IN":["NOUN"], "NOT_IN":["PROPN"]}}}
                ]
                     },
            'can' : {
        
        'ru' : [
            
    {'RIGHT_ID': 'can', 'RIGHT_ATTRS': {"LOWER": {"IN": ["можешь", "можете", "сможешь", "сможете"]}}},
    {'LEFT_ID': 'can', 'REL_OP': '>', 'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB'}}
                ],
        'en': [
            
    {'RIGHT_ID': 'mod', 'RIGHT_ATTRS': {"LOWER": {"IN": ["can"]}}},
    {'LEFT_ID': 'mod', 'REL_OP': '>', 'RIGHT_ID': 'x_comp', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB',"LOWER":{"NOT_IN": verb_stopwords}}},
    {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'c_comp', 'RIGHT_ATTRS': {'DEP': 'ccomp', 'POS': {"IN":["PRON", "NOUN", "VERB"]}}}
                ]
                     },
    
            'want' : {
        
        'ru' : [
            
    {'RIGHT_ID': 'want', 'RIGHT_ATTRS': {"LOWER": {"IN": ["хотим", "хочу","думаю","могу"]}}},
    {'LEFT_ID': 'want', 'REL_OP': '>', 'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': 'obj', 'POS': {"IN":["NOUN", "VERB"]},"LOWER": {"NOT_IN":rus_stopwords}}}
                ],
        'en': [
            [{'RIGHT_ID': 'mod', 'RIGHT_ATTRS': {"LOWER": {"IN": ["want", "plan"]}}},
                {'LEFT_ID': 'mod', 'REL_OP': '>', 'RIGHT_ID': 'x_comp', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB',"LOWER":{"NOT_IN": verb_stopwords}}},
                {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'part', 'RIGHT_ATTRS': {'DEP': 'aux','POS': 'PART'}},
                {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'c_comp', 'RIGHT_ATTRS': {'DEP': {'IN' : ['ccomp','dobj']}, 'POS': {"IN":["NOUN", "VERB"]},"LOWER": {"NOT_IN":noun_stopwords}}},
                {'LEFT_ID': 'mod', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','LOWER': {"NOT_IN":["you","it","they","who"]}, 'POS': {"IN":["PRON", "PROPN"]}}},
#                 {'LEFT_ID': 'mod', 'REL_OP': ';', 'RIGHT_ID': 'any', 'RIGHT_ATTRS': {'LOWER':{"NOT_IN" : ["n't", "not"]}}}],
            
#                 [{'RIGHT_ID': 'mod', 'RIGHT_ATTRS': {"LOWER": {"IN": ["thinking","planning","going"]}}},
#                 {'LEFT_ID': 'mod', 'REL_OP': '>', 'RIGHT_ID': 'x_comp', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB',"LOWER":{"NOT_IN": verb_stopwords}}},
#                 {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'part', 'RIGHT_ATTRS': {'DEP': 'aux','POS': 'PART'}},
#                 {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'c_comp', 'RIGHT_ATTRS': {'DEP': {'IN' : ['ccomp','dobj']}, 'POS': {"IN":["PRON", "NOUN", "VERB"]},"LOWER": {"NOT_IN":noun_stopwords}}},
#                 {'LEFT_ID': 'mod', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','LOWER': {"NOT_IN":["you","it","they","who"]}, 'POS': {"IN":["PRON"]}}},
#                 {'LEFT_ID': 'mod', 'REL_OP': ';', 'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {'DEP': 'aux','POS': 'AUX'}},
                {'LEFT_ID': 'mod', 'REL_OP': ';', 'RIGHT_ID': 'any', 'RIGHT_ATTRS': {'LOWER':{"NOT_IN" : ["n't", "not"]}}}]
               ]
                     },
    
            'task' : {
        
        'ru' : [
            
    {'RIGHT_ID': 'noun', 'RIGHT_ATTRS': {'POS': 'NOUN',"LOWER": {"IN": ["задача", "задачу"]}}},
    {'LEFT_ID': 'noun', 'REL_OP': '>', 'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'DEP': 'csubj','POS': 'VERB'}}
                ],
        'en' : [[
            
    {'RIGHT_ID': 'mod', 'RIGHT_ATTRS': {'POS': 'VERB',"LOWER": {"IN": ["task"]}}},
    {'LEFT_ID': 'mod', 'REL_OP': '>', 'RIGHT_ID': 'x_comp', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB'}},
    {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {'DEP': 'aux','POS': 'PART'}},
    {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'c_comp', 'RIGHT_ATTRS': {'DEP': 'ccomp', 'POS': {"IN":["PRON", "NOUN", "VERB"]}, "LOWER": {"NOT_IN":pron_stopwords}}}
                ],
            
    [{'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {"LOWER": {"IN": ["is"]}}},
    {'LEFT_ID': 'aux', 'REL_OP': '>', 'RIGHT_ID': 'x_comp', 'RIGHT_ATTRS': {'DEP': 'xcomp','POS': 'VERB'}},
     {'LEFT_ID': 'aux', 'REL_OP': '>', 'RIGHT_ID': 'task', 'RIGHT_ATTRS': {'DEP': 'nsubj',"LOWER": {"IN": ["task","plan"]}}},
    {'LEFT_ID': 'x_comp', 'REL_OP': '>', 'RIGHT_ID': 'part', 'RIGHT_ATTRS': {'DEP': 'aux','POS': 'PART'}}
                ]]
                    },
                
            'discuss' : {
        
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB',"LOWER": {"IN": ["discuss","discussing"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'obj', 'RIGHT_ATTRS': {'DEP': {"IN" : ['xcomp','dobj']},'POS': {"IN":['VERB',"NOUN"]},"LOWER":{"NOT_IN":noun_stopwords+verb_stopwords}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {'DEP': 'aux','POS': {"IN": ['PART', "AUX"]}}},
                  ],
        
        'ru' : [
            
    {'RIGHT_ID': 'discuss', 'RIGHT_ATTRS': {"LOWER": {"IN": ["обсудим", "обсуждаем"]}}},
    {'LEFT_ID': 'discuss', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': 'obj', 'POS': {"IN":["NOUN", "VERB"]}}}
                ]
                    },
    
            'remind' : {
        
        'ru' : [
            
    {'RIGHT_ID': 'noun', 'RIGHT_ATTRS': {'POS': 'NOUN',"LOWER": {"IN": ["напоминаю","напоминание"]}}},
    {'LEFT_ID': 'noun', 'REL_OP': '>', 'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'DEP': 'csubj','POS': 'VERB'}}
                ],
        
        'en' : [
            
    {'RIGHT_ID': 'remind', 'RIGHT_ATTRS': {'POS': 'VERB',"LOWER": {"IN": ["remind", "forget","reminder", "reminding"]}}},
    {'LEFT_ID': 'remind', 'REL_OP': '>', 'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'DEP': {"IN" : ['ccomp','dobj']},'POS': {"IN":['VERB',"NOUN"]},"LOWER":{"NOT_IN":verb_stopwords+noun_stopwords}}}
                  ]
                },
    
#             'date' : ,
    
            'weekday' : {
        
        'ru' : [
            
            [
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB','MORPH': {'INTERSECTS': ['Tense=Fut','Number=Plur','Tense=Pres',"VerbForm=Inf"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'weekday', 'RIGHT_ATTRS': {'DEP': {"IN": ["nsubj",'obl',"advmod"]},"LOWER": {"IN": ["завтра", "послезавтра", "понедельник","вторник","среду","четверг","пятницу","субботу","воскресенье"]}}}
            ],
            
            [
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'LOWER': {'IN': ['созвонимся','созвониться']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'weekday', 'RIGHT_ATTRS': {'DEP': 'obl',"LOWER": {"IN": ["сегодня","завтра", "послезавтра", "понедельник","вторник","среду","четверг","пятницу","субботу","воскресенье"]}}}
            ]
                ],
        'en' : 
            [
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB','MORPH': {'IS_SUBSET': ['VerbForm=Inf','Tense=Pres']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'prep', 'RIGHT_ATTRS': {'POS': 'ADP'}},
    {'LEFT_ID': 'prep', 'REL_OP': '>', 'RIGHT_ID': 'weekday', 'RIGHT_ATTRS': {'DEP': 'pobj',"LOWER": {"IN": ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]}}}
            ]},
            
            'time' : {
        
        'ru' : [
            
            [
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>>', 'RIGHT_ID': 'hours', 'RIGHT_ATTRS': {"LOWER" : {"IN" : ['час', "2", "3", "4", "5","6","7","8","9","10","11", "12", "30", "40","15","10","20","50"]}}},
    {'LEFT_ID': 'hours', 'REL_OP': '>', 'RIGHT_ID': 'minutes', 'RIGHT_ATTRS': {'DEP': 'nummod', "LOWER" : {"IN" : ['час', "2", "3", "4", "5","6","7","8","9","10","11", "12", "30", "40","15","10","20","50"]}}}
            ],
            
            [
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'LOWER': {'IN': ['созвонимся']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>>', 'RIGHT_ID': 'hours', 'RIGHT_ATTRS': {'POS': 'NUM'}},
    {'LEFT_ID': 'hours', 'REL_OP': '>', 'RIGHT_ID': 'minutes', 'RIGHT_ATTRS': {'DEP': 'nummod', 'POS': 'NUM'}}
            ]
                ],
        
        'en' : [
                [
    {'RIGHT_ID': 'root', 'RIGHT_ATTRS': {'POS': {"IN":['VERB','AUX']}}},
    {'LEFT_ID': 'root', 'REL_OP': '>', 'RIGHT_ID': 'adp', 'RIGHT_ATTRS': {'POS': 'ADP'}},
    {'LEFT_ID': 'adp', 'REL_OP': '>', 'RIGHT_ID': 'noun', 'RIGHT_ATTRS': {"LOWER": {"IN": ["pm","am"]}}},
    {'LEFT_ID': 'noun', 'REL_OP': '>', 'RIGHT_ID': 'hours', 'RIGHT_ATTRS': {'POS': 'NUM'}}
            ]]},
    
            'nsubj_verb_dobj' : { 
        
        'ru' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB',"LOWER":{"NOT_IN":rus_stopwords}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {'DEP': 'aux'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': {"IN":['PRON',"PROPN"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': 'obj', 'POS': {"NOT_IN":['NOUN',"PROPN"]}}}
                ],
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB',"LOWER":{"NOT_IN":verb_stopwords}}},
    {'LEFT_ID': 'verb', 'REL_OP': ';', 'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {'DEP': 'aux','MORPH': 'VerbForm=Fin'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': {"IN":['PRON',"PROPN"]},"LOWER": {"NOT_IN": noun_stopwords}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'd_object', 'RIGHT_ATTRS': {'DEP': 'dobj','POS': {"NOT_IN":['NOUN',"PROPN"]},"LOWER":{"NOT_IN":noun_stopwords}}}
                ]},
    
            'strong_do' : {
        'ru' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB',"LOWER":{"NOT_IN":rus_stopwords}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {'DEP': 'aux'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': {"IN":['PRON',"PROPN"]},'LOWER':{"NOT_IN" : ["что"]}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': 'obj', 'POS': {"IN":['NOUN',"PROPN"]},"LOWER":{"NOT_IN":rus_stopwords}}}
                ],
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB',"LOWER":{"NOT_IN":verb_stopwords}}},
    {'LEFT_ID': 'verb', 'REL_OP': ';', 'RIGHT_ID': 'aux', 'RIGHT_ATTRS': {'DEP': 'aux','MORPH': 'VerbForm=Fin'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': {"IN":['PRON',"PROPN"]},"LOWER": {"NOT_IN": noun_stopwords}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'd_object', 'RIGHT_ATTRS': {'DEP': 'dobj','POS': {"IN":['NOUN',"PROPN"]},"LOWER":{"NOT_IN":noun_stopwords}}}
                ]},
    
            'been_done': {
        
        'ru' : [
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB','MORPH': {'IS_SUPERSET': ['Tense=Past']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': 'PRON'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': 'obj','POS': {"IN":["NOUN"]}, "LOWER": {"NOT_IN":pron_stopwords}}}
                ],
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB','MORPH': {'IS_SUPERSET': ['Tense=Past']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': 'PRON'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'd_object', 'RIGHT_ATTRS': {'DEP': 'dobj',"LOWER":{"NOT_IN":noun_stopwords}}}
                ]},
        'strong_been_done': {
        
        'ru' : [
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB','MORPH': {'IS_SUPERSET': ['Tense=Past']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': 'PRON'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'object', 'RIGHT_ATTRS': {'DEP': 'obj','POS': {"IN":["NOUN"]}, "LOWER": {"NOT_IN":pron_stopwords}}}
                ],
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB', "ORTH":{"NOT_IN": verb_stopwords},'MORPH': {'IS_SUPERSET': ['Tense=Past']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS':{"IN" : ['PRON', 'PROPN']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'd_object', 'RIGHT_ATTRS': {'DEP': 'dobj','POS': 'NOUN',"LOWER":{"NOT_IN":noun_stopwords}}}
                ]},
    'today': {
        
        'ru' : [
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB','MORPH': {'IS_SUPERSET': ['Tense=Pres']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': 'PRON'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'today', 'RIGHT_ATTRS': {'DEP': 'advmod','LOWER': {"IN":["сегодня"]}}}
                ],
        'en' : [
            
    {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'POS': 'VERB','MORPH': {'IS_SUBSET': ['Tense=Pres', 'Tense=Fut']}}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS': {'DEP': 'nsubj','POS': 'PRON'}},
    {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'today', 'RIGHT_ATTRS': {'DEP': 'advmod',"LOWER":{"IN":['today']}}}
                ]}
    
}