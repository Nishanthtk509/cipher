from openai import OpenAI
from django.conf import settings
from datetime import datetime
import requests



# OpenRouter Client
client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


SYSTEM_PROMPT = """
You are Cipher, an advanced AI assistant.

You can assist users in almost any profession or field.

Technology:
- Python
- Django
- JavaScript
- React
- APIs
- Databases
- AI & Machine Learning
- DevOps
- Cybersecurity

Design:
- UI/UX Design
- Web Design
- Graphic Design
- Branding
- Figma

Business:
- Marketing
- Sales
- Finance
- Entrepreneurship
- Startups
- Project Management
- HR

Creative:
- Content Writing
- Blogging
- SEO
- Copywriting
- Script Writing

Education:
- Students
- Teachers
- Researchers
- Mathematics
- Science
- Programming

Professional:
- Engineering
- Architecture
- Consulting
- Accounting
- Career Guidance

Personal:
- Productivity
- Goal Planning
- Learning
- Communication

Rules:
- Adapt automatically to the user's profession.
- Give practical and actionable answers.
- Provide production-ready code when requested.
- Explain concepts clearly.
- Be friendly and professional.
- Use search results when provided.
- Never invent real-time information.
"""


def search_web(query):
    """
    Search using Serper.dev
    """

    try:

        url = "https://google.serper.dev/search"

        headers = {
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )

        data = response.json()

        results = []

        for item in data.get("organic", [])[:5]:

            results.append(
                f"""
Title: {item.get('title', '')}
Snippet: {item.get('snippet', '')}
Link: {item.get('link', '')}
"""
            )

        return "\n".join(results)

    except Exception as e:
        return f"Search Error: {str(e)}"


def get_latest_news():

    try:

        url = "https://google.serper.dev/news"

        headers = {
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "q": "latest news"
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )

        data = response.json()

        news = []

        for item in data.get("news", [])[:5]:

            news.append(
                f"• {item.get('title', '')}"
            )

        return "\n".join(news)

    except Exception as e:
        return f"News Error: {str(e)}"


def ask_ai(message):

    current_datetime = datetime.now().strftime(
        "%d %B %Y %I:%M %p"
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1",
        messages=[
            {
                "role": "system",
                "content": f"""
Current Date & Time:
{current_datetime}

{SYSTEM_PROMPT}
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content


def search_and_summarize(query):

    search_results = search_web(query)

    prompt = f"""
User Question:
{query}

Search Results:
{search_results}

Answer the question using the search results.
Provide a concise and accurate answer.
"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def get_cipher_response(message):

    msg = message.lower().strip()

    # =========================
    # IMAGE GENERATION
    # =========================

    image_keywords = [
        "generate image",
        "create image",
        "draw",
        "make image",
        "design image",
        "create logo",
        "generate logo",
        "create poster",
        "design poster",
        "create banner",
        "generate banner",
        "landing page design",
        "ui design"
    ]

    if any(msg.startswith(keyword) for keyword in image_keywords):

        prompt = message

        for keyword in image_keywords:
            prompt = prompt.replace(keyword, "")

        prompt = prompt.strip()

        if not prompt:
            return "Please provide an image description."

        return generate_image(prompt)

    # =========================
    # CURRENT TIME
    # =========================

    if (
        "what time" in msg
        or msg == "time"
        or "current time" in msg
    ):
        return datetime.now().strftime(
            "Current time: %I:%M %p"
        )

    # =========================
    # CURRENT DATE
    # =========================

    if (
        "what date" in msg
        or msg == "date"
        or "today date" in msg
        or "current date" in msg
    ):
        return datetime.now().strftime(
            "Today's date: %d %B %Y"
        )

    # =========================
    # LATEST NEWS
    # =========================

    if (
        "latest news" in msg
        or msg == "news"
    ):
        return get_latest_news()

    # =========================
    # REAL-TIME SEARCH
    # =========================

    realtime_keywords = [
        "today",
        "latest",
        "current",
        "news",
        "winner",
        "won",
        "score",
        "result",
        "ipl",
        "cricket",
        "football",
        "soccer",
        "tennis",
        "match",
        "live",
        "stock",
        "share price",
        "bitcoin",
        "crypto",
        "weather",
        "temperature",
        "election",
        "breaking",
        "president",
        "prime minister",
        "earthquake",
        "flood",
        "gold price",
        "silver price"
    ]

    if any(word in msg for word in realtime_keywords):
        return search_and_summarize(message)

    # =========================
    # NORMAL AI CHAT
    # =========================

    try:
        return ask_ai(message)

    except Exception as e:
        return f"Cipher Error: {str(e)}"

def generate_image(prompt):

    try:

        url = "https://modelslab.com/api/v6/realtime/text2img"

        payload = {
            "key": settings.MODELSLAB_API_KEY,
            "prompt": prompt,
            "negative_prompt": "blurry, low quality",
            "width": "1024",
            "height": "1024",
            "samples": "1"
        }

        response = requests.post(
            url,
            json=payload,
            timeout=120
        )

        data = response.json()

        if "output" in data:
            return data["output"][0]

        return f"Image generation failed: {data}"

    except Exception as e:
        return f"Image Error: {str(e)}"



        