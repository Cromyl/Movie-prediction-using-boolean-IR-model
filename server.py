from transformers import pipeline
import pandas as pd
from collections import defaultdict
import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
import json
from flask import Flask, jsonify, request
from pyngrok import ngrok
import threading
from flask_cors import CORS


def answer_question(paragraph, question):
    # Initialize the question-answering pipeline
    qa_pipeline = pipeline("question-answering")

    # Use the pipeline to answer the question
    result = qa_pipeline(question=question, context=paragraph)

    return result['answer']



def answers_to_common_question(paragraph):
    # paragraph = """
    # A thriller story written by jk rowling which has a character named voldemord.
    # """
    question1 = "Genre of the movie?"
    question2 = "Keywords of the movie?"
    question3 = "Tagline of the movie?"
    question4 = "Overview of the movie?"
    question5 = "Director of the movie?"
    question6 = "Cast of the movie?"

    answer1 = answer_question(paragraph, question1)
    answer2 = answer_question(paragraph, question2)
    answer3 = answer_question(paragraph, question3)
    answer4 = answer_question(paragraph, question4)
    answer5 = answer_question(paragraph, question5)
    answer6 = answer_question(paragraph, question6)
    return [answer1,answer2,answer3,answer4,answer5,answer6]



class BooleanModel:
    def __init__(self):
        self.inverted_index = defaultdict(set)

    def tokenize(self, text):
        # Tokenize by splitting genres by spaces

        return text.lower().split()

    def add_document(self, doc_id, text):
        # Tokenize the genres and add to inverted index
        tokens = self.tokenize(text)
        for token in tokens:
            self.inverted_index[token].add(doc_id)

    def and_query(self, terms):
        # Find common movies containing all genres (AND operation)
        results = None
        for term in terms:
            if results is None:
                results = self.inverted_index.get(term, set())
            else:
                results = results.intersection(self.inverted_index.get(term, set()))
        return results if results else set()

    def or_query(self, terms):
      results = {}
      for term in terms:
          matching_movies = self.inverted_index.get(term, set())
          for movie in matching_movies:
              if movie in results:
                  results[movie] += 1
              else:
                  results[movie] = 1

      return results

    def not_query(self, term, all_docs):
        # Find movies that do not contain the genre (NOT operation)
        return all_docs.difference(self.inverted_index.get(term, set()))

# Function to load movie data and build the boolean model
def create_boolean_model_from_csv(file_path,requirement):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Initialize the BooleanModel
    model = BooleanModel()

    # Loop through each row and add to the BooleanModel
    for index, row in df.iterrows():
        title = row['title']
        requirements = row[requirement]
        model.add_document(str(title), str(requirements))

    return model, set(df['title'])

# Example usage
def boolean_model_creator():
    # Path to the CSV file
    file_path = "movie_dataset.csv"

    # Create the Boolean model from the CSV
    model1, all_titles = create_boolean_model_from_csv(file_path,'genres')
    model2, all_titles = create_boolean_model_from_csv(file_path,'keywords')
    model3, all_titles = create_boolean_model_from_csv(file_path,'tagline')
    model4, all_titles = create_boolean_model_from_csv(file_path,'overview')
    model5, all_titles = create_boolean_model_from_csv(file_path,'director')
    model6, all_titles = create_boolean_model_from_csv(file_path,'cast')

    return [model1,model2,model3,model4,model5,model6]



nltk.download('stopwords')

def clean_and_tokenize(text):
    # Get the stop words for English
    stop_words = set(stopwords.words('english'))

    # Step 1: Convert to lowercase
    text = text.lower()

    # Step 2: Correct spelling mistakes
    corrected_text = str(TextBlob(text).correct())

    # Step 3: Remove extra characters (keep only alphanumeric and spaces)
    corrected_text = re.sub(r'[^a-z0-9\s]', '', corrected_text)

    # Step 4: Tokenize the text
    tokens = corrected_text.split()

    # Step 5: Remove stop words
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens




def get_query_result_or(model, words):
    results = {}

    # Get the result dictionary from the or_query method
    query_results = model.or_query(words)

    # Merge the query results into the results dictionary
    for movie, count in query_results.items():
        if movie in results:
            results[movie] += count  # Increment count if movie already exists
        else:
            results[movie] = count   # Add new movie to the dictionary

    return results


def get_query_result_and(model,words):
  results = set()
  results = results.union(model.and_query(words))
  return results




model_list= boolean_model_creator()

def process_strings(string_list):
    tokenized_list = [clean_and_tokenize(text) for text in string_list]
    return tokenized_list

def query_function(paragraph):
  string_count_map = defaultdict(int)
  result = answers_to_common_question(paragraph)
  result = process_strings(result)
  returned_strings=''
  for i in range(6):
    returned_dict = get_query_result_or(model_list[i],result[i])
    # print(returned_dict)
    for string in returned_dict:
        string_count_map[string] += returned_dict[string]

  return dict(list(sorted(string_count_map.items(), key=lambda item: item[1], reverse=True))[:10])



app = Flask(__name__)
CORS(app)

# Home route
@app.route('/')
def home():
    return "Hello, World! Welcome to the public API."

# API route to accept a string as a query parameter
@app.route('/api', methods=['GET'])
def api_data():
    # Get the 'input' query parameter from the URL
    input_string = request.args.get('input')

    # Check if the input string is provided
    if input_string is None:
        return jsonify({"error": "No input string provided"}), 400

    # Process the string using the function
    output_string = json.dumps(query_function(input_string))

    # Return the processed string
    return jsonify({"original": input_string, "processed": output_string, "status": "success"})



# Function to run the Flask app
def run_app():
    app.run(port=2637)

# Start the Flask app in a new thread
# thread = threading.Thread(target=run_app)
# thread.daemon = True 
# thread.start()
run_app()

# Add your ngrok authentication token here
# auth_token = '2n5kqTc9HwrLFd7SdymYst3iATA_5UcDDzSprQpdDfcn3Hko5'
# ngrok.set_auth_token(auth_token)

# # Start ngrok tunnel to expose the Flask app
# public_url = ngrok.connect(2637)
# print(f"Public URL: {public_url}")