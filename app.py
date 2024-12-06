from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Configure OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample email history
email_history = [
    {
        "purpose": "Follow-up on job application",
        "tone": "Formal",
        "details": "I interviewed last week for the Product Manager role and wanted to follow up on the status of my application.",
        "draft": """Subject: Follow-Up on Product Manager Job Application

Dear [Hiring Manager's Name],

I hope this email finds you well. I wanted to follow up on my application for the Product Manager position and inquire about any updates regarding the status of my candidacy. I greatly enjoyed our conversation during the interview on [date] and am very enthusiastic about the opportunity to contribute to [Company Name].

Please let me know if there is any additional information I can provide to assist in your decision-making process. I look forward to hearing from you soon.

Best regards,
[Your Full Name]
"""
    },
    {
        "purpose": "Request for meeting reschedule",
        "tone": "Casual",
        "details": "I need to reschedule our team sync meeting planned for Monday due to a conflict with another engagement.",
        "draft": """Subject: Request to Reschedule Monday's Meeting

Hi Team,

I hope you're all doing well! I wanted to reach out to let you know that I have a scheduling conflict with our team sync on Monday. Would it be possible to move it to Tuesday or another time that works for everyone?

Let me know your availability, and I’ll do my best to accommodate. Thanks for your understanding!

Best,
[Your Name]
"""
    },
    {
        "purpose": "Introduce a new product to a client",
        "tone": "Persuasive",
        "details": "We have launched a new AI-powered tool that streamlines customer support, and I believe it could greatly benefit their operations.",
        "draft": """Subject: Enhance Your Customer Support with Our New AI Tool

Dear [Client's Name],

I’m excited to share with you our latest innovation: an AI-powered tool designed to streamline customer support processes and elevate your service efficiency. This tool has already helped organizations like [Example Company] reduce response times by 30% and improve customer satisfaction.

I’d love to schedule a quick call to discuss how this tool could be customized to meet your specific needs. Are you available for a 15-minute chat this week? Let me know a time that works for you.

Looking forward to your response.

Best regards,
[Your Name]
"""
    }
]


@app.route("/", methods=["GET", "POST"])
def index():
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
                model="gpt-3.5-turbo",  # Switch to the supported model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates professional emails.",
                    },
                    {
                        "role": "user",
                        "content": f"Generate an email for the following: Purpose: {purpose}, Tone: {tone}, Additional Details: {additional_details}",
                    },
                ],
                max_tokens=200,
                temperature=0.7,
            )
            email_draft = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            email_draft = f"Error generating email: {e}"

    return render_template("index.html", email_draft=email_draft)

@app.route("/history", methods=["GET"])
def history():
    return render_template("history.html", email_history=email_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
