import time
from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify
from evaluator import Evaluator

COLLECTION_SIZE = 18

COLLECTION_LINKS = {'austen-emma.txt': 'austen-emma.txt', 
                  'austen-persuasion.txt': 'austen-persuasion.txt',
                  'austen-sense.txt': 'austen-sense.txt',
                  'bible-kjv.txt': 'bible-kjv.txt',
                  'blake-poems.txt': 'blake-poems.txt',
                  'bryant-stories.txt': 'bryant-stories.txt',
                  'burgess-busterbrown.txt': 'burgess-busterbrown.txt', 
                  'carroll-alice.txt': 'carroll-alice.txt',
                  'chesterton-ball.txt': 'chesterton-ball.txt',
                  'chesterton-brown.txt': 'chesterton-brown.txt',
                  'chesterton-thursday.txt': 'chesterton-thursday.txt',
                  'edgeworth-parents.txt': 'edgeworth-parents.txt',
                  'melville-moby_dick.txt': 'melville-moby_dick.txt', 
                  'milton-paradise.txt': 'milton-paradise.txt', 
                  'shakespeare-caesar.txt': 'shakespeare-caesar.txt', 
                  'shakespeare-hamlet.txt': 'shakespeare-hamlet.txt', 
                  'shakespeare-macbeth.txt': 'shakespeare-macbeth.txt', 
                  'whitman-leaves.txt': 'whitman-leaves.txt'}

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