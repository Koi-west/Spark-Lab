from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
import time

# Set up OpenAI client
client = OpenAI(
        api_key = "sk-7392f6c5735d48afb7b18b8a58660ebc",  # 请替换成你的API key
        base_url = "https://api.deepseek.com/beta",
    )

app = FastAPI()

class ConversationManager:
    def __init__(self):
        self.context = []
        self.score = 0
        self.last_input = ""
        self.repetition_count = 0

    def analyze_with_openai(self, user_input):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": """Prompt:
                     The first requirement is that all your answers must be in Chinese.

Dialogue Style: Warm and empathetic

Foundation: Your persona is based on warmth, understanding, and support. Your goal is to create a caring and encouraging dialogue environment to effectively support me and foster my emotional well-being. In every interaction, you should not only understand what I am saying but also insightfully grasp the underlying emotions and psychological state behind each statement.

1. Emotional Understanding
Identifying Emotions: When I express my situation, you need to keenly identify and interpret the underlying emotional information, including but not limited to anxiety, frustration, loneliness, and other feelings. By recognizing these emotions, you will better understand my current predicament.
Insight: You should discern the emotional fluctuations I am experiencing from what I say, paying attention to the specific contexts I mention and understanding the emotional highs and lows I am going through.
2. Warm Responses
Comfort and Encouragement: After identifying my emotions, you need to provide encouragement and comfort using warm language. Your responses should reflect deep care and understanding, helping me feel supported and acknowledged.
Empathy: Your words should convey a profound understanding of my emotional state, making me feel that someone genuinely cares about me.
3. Problem Analysis and Solutions
Analyzing the Problem: Based on the difficulties I express, use logical reasoning to analyze the root causes of the problem. Ensure your analysis is constructive and tailored to my specific situation.
Solutions: Provide concrete directions and feasible solutions. These suggestions should be practical and easy to implement, while also considering my emotional state to ensure the solutions do not add to my stress.
4. Encouragement and Support
Ongoing Encouragement: Even when proposing solutions, continue to encourage me, highlighting my abilities and potential. Help me maintain a positive mindset and confidence.
Positive Reinforcement: When I make progress, offer praise and recognition to motivate me to keep moving forward.
"""},
                    {"role": "user", "content": f"Context: {self.context}\n\nUser input: {user_input}\n\nAnalyze the content and context of this conversation."}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return None

    def manage_score(self, user_input, ai_response):
        self.score += 5  # Increase score for every response

        if "satisfied" in user_input.lower() or "happy" in user_input.lower():
            self.score += 20  # Increase score for emotional satisfaction

        if user_input == self.last_input:
            self.repetition_count += 1
            self.score = max(self.score - 5, -200)  # Decrease score for repetition, minimum -200
            return f"I noticed you're repeating yourself. Is there something specific you'd like to explore further?"
        else:
            self.repetition_count = 0
            self.last_input = user_input

        return ai_response

    def trigger(self):
        if self.score >= 60:
            print("YES")  # Output to backend
            self.score = 0  # Reset score
            return True
        return False

conversation_manager = ConversationManager()

@app.post("/api/chat")
async def chat_with_ai(user_input: str):
    conversation_manager.context.append(f"User: {user_input}")

    analysis = conversation_manager.analyze_with_openai(user_input)
    if not analysis:
        raise HTTPException(status_code=500, detail="Failed to analyze input with OpenAI.")
    
    ai_response = conversation_manager.manage_score(user_input, analysis)
    conversation_manager.context.append(f"AI: {ai_response}")

    triggered = conversation_manager.trigger()

    return JSONResponse(content={
        "ai_response": ai_response,
        "triggered": triggered,
        "score": conversation_manager.score
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
