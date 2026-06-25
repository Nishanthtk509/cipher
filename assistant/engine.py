# ai/engine.py

from .search_engine import search_database
from .summarizer import summarize


def generate_answer(question):

    results = search_database(question)

    if not results:
        return "I couldn't find anything related."

    best_match = results[0]

    content = best_match["content"]

    return content[:300] + "..."



    
