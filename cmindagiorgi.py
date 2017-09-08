from flask import Flask, render_template, request
from giorgisshubi import analyze, compare, lgconvert, finalize
import json

app = Flask(__name__)

with app.open_resource('static/roots.json', 'r') as f:
    morphology = f.read()
    roots = json.loads(morphology)

with app.open_resource('static/definitions.json', 'r') as g:
    defs = g.read()
    definitions = json.loads(defs)

@app.route('/dictionary', methods=['GET', 'POST'])
def dictionary():

    if request.method == 'POST':
        result = request.form
        verb = result['verb']
        gverb = lgconvert(verb)
        word = finalize(verb, roots)
        gword = {}

        for k in word:
            try:
                gword[k] = lgconvert(word[k])
            except:
                gword[k] = word[k]

        root = word['root']

        if root in roots:
            pass
     
        elif word['agrpref'] + word['root'] in roots:
            if word['version'] == '':
                root = word['agrpref'] + word['root']
                word['root'] = root
                word['agrpref'] = ''
            else:
                pass

        elif word['root'] + word['doniani'] in roots:
            root = word['root'] + word['doniani']
            word['root'] = root
            word['doniani'] = ''

        elif word['agrpref'] + word['root'] + word['doniani'] in roots:
            root = word['agrpref'] + word['root'] + word['doniani']
            word['root'] = root
            word['agrpref'] = ''
            word['doniani'] = ''

        else:
            error = "Can't find in dictionary"
            return render_template('index.html', error=error)

        possible_matches = roots[root]
        matches = compare(word, possible_matches)
        top_matches = []

        for entry in matches:
            match = definitions[str(entry['definition'])]
            match['aorist'] = lgconvert(match['aorist'])
            match['future'] = lgconvert(match['future'])
            match['perfect'] = lgconvert(match['perfect'])
            if match not in top_matches:
                if word['preverb'] in match['tag']['preverbs'] or word['preverb'] == '':
                    top_matches.append(match)


        return render_template('index.html', word=gword, matches=top_matches,
                gverb=gverb)


    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

