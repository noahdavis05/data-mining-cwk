from dotenv import load_dotenv
from openai import OpenAI
import os,json

# script to take the data I have, and turn it into loads of smaller questions using an LLM

load_dotenv()
api_key = os.getenv('API_KEY')
client = OpenAI(
    api_key=api_key
)

filename = "processed_data/star_wars_data.jsonl"
output_file = "processed_data/question_and_answers.jsonl"

with open(filename, 'r') as file:
    for line in file:
        data = json.loads(line)
        text = data['text']
        # make a request to LLM to convert this large bit of text into loads of smaller questions
        response = client.responses.create(
            model = "gpt-4o-mini",
            instructions = '''
           You are being used to help me convert large sections of text into lots of smaller questions and answers.

            You can reuse sections of text if you would like. Try to only use text from the input you are given, but if needed, you may add small pieces of your own language to make it flow naturally.

            Important Instructions:
            - Do not reduce the overall volume of text you are given.
            - Generate as many questions and answers as needed to match the input's volume.
            - Only output a single plain string.
            - Each Question and Answer pair must be formatted as:
                Instruction: YOUR GENERATED QUESTION HERE\n\nResponse: YOUR GENERATED RESPONSE HERE
            - Separate each complete Question-Answer pair using "~~" (two tilde characters).
            - Do not add any extra characters, comments, or formatting outside the required structure.
            - Do not wrap the output in any JSON, code blocks, or quotation marks.

            Example output:
            Instruction: Who is Luke Skywalker?\n\nResponse: Luke Skywalker is a legendary Jedi Master known for his role in the Galactic Civil War.~~Instruction: What did Luke Skywalker do during the Battle of Yavin?\n\nResponse: Luke destroyed the Death Star during the Battle of Yavin.~~Instruction: Who trained Luke Skywalker?\n\nResponse: Luke was trained by Obi-Wan Kenobi and Yoda.

            Only output the plain string exactly in this format, nothing else.
            ''',
            input = text
        )
        try:
            output_string = response.output_text
            print(output_string)
            data = output_string.split("~~")
            # open output file and write prompts
            output = open(output_file,"a")
            for item in data:
                temp_dict = {"text":item}
                output.write(json.dumps(temp_dict) + "\n")
            output.close()
        except Exception as e:
            print("error: ", e)
