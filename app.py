import os
import time
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with the API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    # Get the message from the request data
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Send the message to OpenAI API using your client syntax
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        # Extract the assistant's response using dot notation
        assistant_response = completion.choices[0].message.content

        return jsonify({"response": assistant_response}), 200

    except Exception as e:
        error_message = str(e)

        # Check for quota limit errors and stop retries
        if "insufficient_quota" in error_message:
            return jsonify({"error": "Insufficient quota. Please check your API plan."}), 429

        # Optional: Add a delay before retrying
        time.sleep(1)

        print(f"Error: {e}")  # Print the error message to the console
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
