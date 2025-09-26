from flask import Flask, render_template, request
import parser  # your parser.py

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    noun_phrases = ''
    if request.method == 'POST':
        text = request.form['text']
        print("Received text:", text)  # debug line
        s = parser.preprocess(text)
        try:
            trees = list(parser.parser.parse(s))
        except ValueError as e:
            result = str(e)
            trees = []

        if trees:
            outputs = []
            np_chunks = []
            for tree in trees:
                outputs.append(tree.pformat())
                np_chunks.extend(parser.np_chunk(tree))
            result = "<br>".join(outputs)
            noun_phrases = ", ".join(np_chunks)

    return render_template('index.html', result=result, noun_phrases=noun_phrases)

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, host="0.0.0.0", port=10000)
