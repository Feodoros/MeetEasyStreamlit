import json
from decomposition import decompose


input_path = '13_.json'
output_path = "13_.json"

if __name__ == '__main__':
    
    for i in range(8):
        input_path='../Transcriber/English_'+str(i)+'.json'
        output_path=input_path
    
        with open(input_path) as json_file:
            transcript_json = json.load(json_file)

        decomposed_json = decompose(transcript_json)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(decomposed_json, f, ensure_ascii=False)