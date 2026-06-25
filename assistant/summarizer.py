# ai/summarizer.py

def summarize(text):

    sentences = text.split(".")

    summary = sentences[:3]

    return ". ".join(summary)