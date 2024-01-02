from fastapi import FastAPI
from Service.start_model import openaiCallAPI
from Service.chat_service import chatService
import os, json
from model import messageChatbot, ChatMessage
from database.db import connect_db, disconnect_db, get_database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env_data = openaiCallAPI.get_env()
openaiAPI = openaiCallAPI(env_data['api_key'])

@app.get("/")
async def root():
    return {"data": {"message" : "Chatbot Service is available"}}

##### CONNECT DATABASE
@app.on_event("startup")
async def startup_db():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_db():
    await disconnect_db()

database = get_database()
#--------------------------------

@app.get("/get-chat/{id}")
async def get_chat(id:int):
    chat_history = await get_chat_session(int(id))
    return chat_history

@app.post("/chat/{session_chat}", response_model=ChatMessage)
async def chat(session_chat:int, messageChat: messageChatbot):
    response = chatService.chatbot(openaiAPI, messageChat.message)
    response_data = {
        "session_id": session_chat,
        "message" : messageChat.message,
        "bot_reply": response
    }
    await create_chat_session(session_id=session_chat, message=messageChat.message, bot_reply=response)
    return response_data

@app.get("/amount-chat")
async def get_chat():
    amount = await get_amount_chat_session()
    return {"chat_amount": amount}

@app.get("/delete-chat/{id}")
async def get_chat(id:int):
    await delete_chat_session(int(id))
    response = {"status":f"Success delete session chat {id}"}
    return response

# ---- query -----
async def get_amount_chat_session():
    query = "SELECT DISTINCT session_id FROM chat_sessions"
    result = await database.fetch_all(query)
    distinct_sessions = [row['session_id'] for row in result]
    return distinct_sessions

async def create_chat_session(session_id: int, message: str, bot_reply:str):
    query = "INSERT INTO chat_sessions (session_id, message, bot_reply) VALUES (:session_id, :message, :bot_reply)"
    values = {"session_id": session_id, "message": message, "bot_reply":bot_reply}
    await database.execute(query, values)

async def get_chat_session(session_id: int):
    query = "SELECT id, session_id, message, bot_reply FROM chat_sessions WHERE session_id = :session_id"
    values = {"session_id": session_id}
    return await database.fetch_all(query, values)

async def delete_chat_session(session_id: int):
    query = "DELETE FROM chat_sessions WHERE session_id = :session_id"
    values = {"session_id": session_id}
    await database.execute(query, values)

