from flask import Flask, render_template, request
import parser  
from nltk import Tree

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    noun_phrases = ''
    
    if request.method == 'POST':
        text = request.form['text']
        s = parser.preprocess(text)
        
        try:
            trees = list(parser.parser.parse(s))
        except ValueError as e:
            result = f"Error: {e}"
            trees = []

        if trees:
            outputs = []
            np_chunks = []

            for tree in trees:
                outputs.append(tree.pformat())
                
                for subtree in tree.subtrees():
                    if subtree.label() == 'NP':
                        np_chunks.append(subtree)
            
            result = "\n\n".join(outputs)
            noun_phrases = ", ".join(
                " ".join(leaf[0] for leaf in np.leaves()) for np in np_chunks
            )

    return render_template('index.html', result=result, noun_phrases=noun_phrases)


if __name__ == "__main__":
    print("Starting Flask server...") 
    app.run(debug=True, host="0.0.0.0", port=10000)
