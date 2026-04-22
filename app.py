from flask import Flask, render_template, request
import os
import parser as nlp_parser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    parse_trees = []
    noun_phrases = []
    error = None
    
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if not text:
            error = "Please enter a sentence."
        else:
            trees = nlp_parser.parse_sentence(text)
            if not trees:
                error = "Could not parse sentence with current grammar."
            else:
                parse_trees = [tree.pformat() for tree in trees]
                chunk_values = []
                seen_chunks = set()
                for tree in trees:
                    for np_subtree in nlp_parser.np_chunk(tree):
                        leaf_words = [
                            leaf[0] if isinstance(leaf, tuple) else leaf
                            for leaf in np_subtree.leaves()
                        ]
                        chunk_text = " ".join(leaf_words)
                        if chunk_text not in seen_chunks:
                            seen_chunks.add(chunk_text)
                            chunk_values.append(chunk_text)
                noun_phrases = chunk_values

    return render_template(
        'index.html',
        parse_trees=parse_trees,
        noun_phrases=noun_phrases,
        error=error
    )


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(
        debug=os.getenv("FLASK_DEBUG", "").lower() in {"1", "true", "yes"},
        host="0.0.0.0",
        port=10000
    )
