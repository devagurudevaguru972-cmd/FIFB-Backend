import os

from fastapi import APIRouter
from pydantic import BaseModel

from openai import OpenAI
from dotenv import load_dotenv

from app.db.mongo import user_collection
from app.db.mongo import chat_collection

load_dotenv()

router = APIRouter()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


class ChatRequest(BaseModel):
    message: str
    user_id: str


@router.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message

    # Demo user from MongoDB
    user = user_collection.find_one({
    "user_id": request.user_id
})

    # User finance data
    finance_context = f"""
User Details:
user_id: {user.get('user_id', 'Unknown')}
Savings: {user.get('savings', 0)}
Loan: {user.get('loan', 0)}
Insurance: {user.get('insurance', 0)}
Salary: {user.get('salary', 0)}
City: {user.get('city', 'Unknown')}
"""
    try:

        response = client.chat.completions.create(
            model="gpt-4o",

            messages=[

                {
                    "role": "system",
                    "content": f"""
                    You are an advanced Finance AI Assistant.

Your role is to help users with:

- Mutual Funds
- SIP Investments
- Stock Market Basics
- Savings Advice
- Loan Management
- Insurance Guidance
- Budget Planning
- Financial Planning
- Tax Saving Ideas
- Personal Finance Education

Rules:

1. Always give clear and beginner-friendly answers.
2. Explain financial concepts in simple language.
3. Give practical examples when needed.
4. If user asks investment advice, suggest low-risk and safe options first.
5. Encourage smart saving habits.
6. Never give illegal or harmful financial advice.
7. Use the user's financial data while answering.
8. If user's savings are low, suggest saving strategies.
9. If user's loan is high, suggest debt reduction ideas.
10. If user asks about SIP or Mutual Funds, explain risk level, returns, and long-term benefits clearly.
11. Speak professionally but friendly.
12. Keep answers concise and useful.

You can also:
- Compare investment options
- Explain finance terms
- Suggest budgeting plans
- Explain EMI calculations
- Help with wealth planning

Always behave like a smart AI financial advisor:

                    Use this finance data while answering:

                    {finance_context}
                    """
                },

                {
                    "role": "user",
                    "content": user_message
                }

            ]
        )

        reply = response.choices[0].message.content
        # Save chat history

        chat_collection.insert_one({

           "user_id": user["user_id"],

           "question": user_message,

           "answer": reply

})

    except Exception as e:

        reply = f"Error: {str(e)}"

    return {
        "reply": reply
    }
