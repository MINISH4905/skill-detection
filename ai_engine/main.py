# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_generator import generate_topics
from domains import DOMAINS

app = FastAPI(title="NextGen LLaMA AI Engine")


class TopicRequest(BaseModel):
    domain: str
    count: int = 10


@app.get("/")
def home():
    return {"message": "LLaMA AI Engine Running"}


@app.get("/domains")
def get_domains():
    return {"domains": DOMAINS}


@app.post("/topics")
def get_topics(request: TopicRequest):

    if request.domain not in DOMAINS:
        raise HTTPException(status_code=404, detail="Domain not supported")

    topics = generate_topics(request.domain, request.count)

    return {
        "domain": request.domain,
        "topics": topics
    }