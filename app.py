from flask import Flask, render_template, request
import parser as nlp_parser   # rename to avoid conflict with Python's standard library

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        # Preprocess the input
        s = nlp_parser.preprocess(text)
        try:
            trees = list(nlp_parser.parser.parse(s))
        except Exception as e:
            result = f"Error: {e}"
            trees = []

        if trees:
            outputs = []
            for tree in trees:
                # Pretty print as string
                outputs.append(tree.pformat())
                # Get NP chunks
                np_chunks = [" ".join(np.flatten()) for np in nlp_parser.np_chunk(tree)]
                outputs.append("Noun Phrase Chunks: " + ", ".join(np_chunks))
            result = "\n\n".join(outputs)
        else:
            if not result:
                result = "Could not parse sentence."

    # Must return a response for both GET and POST
    return render_template('index.html', result=result)

if __name__ == "__main__":
    print("Starting Flask server...")   # debug line
    app.run(debug=True)
import os
print("Current folder:", os.getcwd())
print("Templates folder exists:", os.path.isdir("templates"))
print("Index exists:", os.path.isfile("templates/index.html"))
