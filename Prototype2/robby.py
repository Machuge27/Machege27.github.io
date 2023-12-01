from flask import Flask, render_template, request, jsonify
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

app = Flask(__name__)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# Load documents
loader = CSVLoader(file_path="dataset.csv")
index_creator = VectorstoreIndexCreator()
docsearch = index_creator.from_loaders([loader])

# Create question-answering chain
chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=docsearch.vectorstore.as_retriever(),
    input_key="question",
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    # Pass query to the chain
    response = chain({"question": question})
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
