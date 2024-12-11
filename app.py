from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

# Configure OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
API_GATEWAY_URL = "https://zr86zuw8ie.execute-api.us-east-1.amazonaws.com/default/generateEmail"
GET_EMAILS_API_URL = "https://rzruww4oeb.execute-api.us-east-1.amazonaws.com/default/queryEmail"

# Items per page for pagination
ITEMS_PER_PAGE = 5


@app.route("/", methods=["GET", "POST"])
def index():
    """Route to generate an email based on user input."""
    email_draft = None
    if request.method == "POST":
        purpose = request.form.get("purpose")
        tone = request.form.get("tone")
        additional_details = request.form.get("details")

        # Generate prompt for LLM
        prompt = f"""
        Write a professional email for the following scenario:
        - Purpose: {purpose}
        - Tone: {tone}
        - Additional Details: {additional_details}
        """
        print(prompt)

        try:
            # Use OpenAI's chat model
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates professional emails.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                max_tokens=200,
                temperature=0.7,
            )
            email_draft = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            email_draft = f"Error generating email: {e}"

        if not email_draft.startswith("Error generating email:"):
            try:
                # Store email draft in the backend
                _ = requests.post(
                    API_GATEWAY_URL,
                    json={
                        "purpose": purpose,
                        "tone": tone,
                        "details": additional_details,
                        "draft": email_draft,
                    },
                )
            except Exception as e:
                email_draft = f"Error saving email: {e}"
                print(f"Error: {e}")

    return render_template("index.html", email_draft=email_draft)


@app.route("/history", methods=["GET"])
def history():
    """Route to display email history with pagination."""
    try:
        # Query all emails from the API Gateway
        api_response = requests.get(GET_EMAILS_API_URL)
        if api_response.status_code == 200:
            email_history = api_response.json().get("emails", [])
        else:
            email_history = []
            print(f"Failed to fetch emails: {api_response.json()}")
    except Exception as e:
        email_history = []
        print(f"Error fetching email history: {e}")

    # Handle pagination
    page = int(request.args.get("page", 1))
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated_emails = email_history[start:end]

    # Determine pagination controls
    has_next = end < len(email_history)
    has_prev = start > 0

    return render_template(
        "history.html",
        email_history=paginated_emails,
        page=page,
        has_next=has_next,
        has_prev=has_prev,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
