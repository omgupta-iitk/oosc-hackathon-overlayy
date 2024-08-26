import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
prompt_template = """
Generate two good questions from the following context in around 80 characters each and then respond with a JSON object like below :
{{
"Question 1": "Question", 
"Question 2": "Question",
}}
Context:\n {context}?\n

"""
load_dotenv()

GOOGLE_API_KEY = 'AIzaSyBVGNTYqXhyg2v-d15dJn9oYxqJAJRHHLI' #os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

tweet_prompt = PromptTemplate.from_template(prompt_template)

tweet_chain = LLMChain(llm=llm, prompt=tweet_prompt, verbose=False)
def parse_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return []
def run():
    lists = parse_file_to_list("segment.txt")
    questions = []
    for l in lists:
        with open(l,'r') as file:
            data = file.read()
            resp = tweet_chain.run(context = data)
            json_output = json.loads(resp)

            questions.append(json_output['Question 1'])
            questions.append(json_output['Question 2'])
            
    return questions

