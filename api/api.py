import time
from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify
from evaluator import Evaluator

COLLECTION_SIZE = 18

COLLECTION_LINKS = {'austen-emma.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/austen-emma.txt', 
                  'austen-persuasion.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/austen-persuasion.txt',
                  'austen-sense.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/austen-sense.txt',
                  'bible-kjv.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/bible-kjv.txt',
                  'blake-poems.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/blake-poems.txt',
                  'bryant-stories.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/bryant-stories.txt',
                  'burgess-busterbrown.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/burgess-busterbrown.txt', 
                  'carroll-alice.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/carroll-alice.txt',
                  'chesterton-ball.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/chesterton-ball.txt',
                  'chesterton-brown.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/chesterton-brown.txt',
                  'chesterton-thursday.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/chesterton-thursday.txt',
                  'edgeworth-parents.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/edgeworth-parents.txt',
                  'melville-moby_dick.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/melville-moby_dick.txt', 
                  'milton-paradise.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/milton-paradise.txt', 
                  'shakespeare-caesar.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/shakespeare-caesar.txt', 
                  'shakespeare-hamlet.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/shakespeare-hamlet.txt', 
                  'shakespeare-macbeth.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/shakespeare-macbeth.txt', 
                  'whitman-leaves.txt': 'https://raw.githubusercontent.com/oblasko/information-retrieval-boolean-model/main/corpus/whitman-leaves.txt'}

app = Flask(__name__)
CORS(app)

@app.route('/querry', methods = ['POST'])
def get_query_from_react():
    querry_json = request.get_json()

    if not querry_json:
        return 'Missing JSON', 400

    querry = querry_json["querry"]
    querry = querry["querry"]
    
    if not querry:
        return 'Querry is missing', 400

    e1 = Evaluator(COLLECTION_SIZE)
    
    try:
        res = e1.evaluate(querry)
        ids = []
        raw_links = []

        for i in range(len(res)):
            ids.append(i)
            raw_links.append(COLLECTION_LINKS.get(res[i]))
        
    except TypeError as e:
        return "Not a valid boolean expression", 400

    
    return jsonify({'table': res, 'ids': ids, "links": raw_links}), 200