import os
from flask import Flask, render_template, request
import parser  # your parser.py

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        s = parser.preprocess(text)
        try:
            trees = list(parser.parser.parse(s))
        except ValueError as e:
            result = str(e)
            trees = []

        outputs = []
        for tree in trees:
            outputs.append(tree.pformat())
        return render_template('index.html', result="\n\n".join(outputs))
    return render_template('index.html', result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
