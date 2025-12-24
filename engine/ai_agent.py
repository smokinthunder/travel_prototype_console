import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# MOCK MODE: Set to True if you don't have an API key right now
MOCK_MODE = False 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an expert Travel Designer and UI Architect. 
Your goal is to convert raw itinerary data into a JSON structure for a visual slide deck (Gamma-style).

RULES:
1. Tone: Match the 'vibe' provided in metadata.
2. Structure: Break the output into a list of 'slides'.
3. Layouts: Assign a 'layout_type' to each slide. Options: ['title_hero', 'split_left', 'split_right', 'grid_gallery'].
4. Images: Since we don't have real images, output strict PLACEHOLDER descriptions in 'image_prompt'.
5. Content: Write compelling marketing copy. Do not make up facts, but polish the descriptions.
"""

def generate_presentation_json(raw_data):
    if MOCK_MODE:
        print("⚠️  Running in MOCK MODE (No API Call)")
        return mock_response()

    print("🧠 Sending data to AI Model...")
    
    response = client.chat.completions.create(
        model="gpt-4o",  # Use your GPT-5.1 access here
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Convert this raw trip data into a Presentation JSON:\n{json.dumps(raw_data)}"}
        ]
    )

    return json.loads(response.choices[0].message.content)

def mock_response():
    # Fallback if no API key
    return {
        "slides": [
            {
                "layout": "title_hero",
                "title": "Escape to the Amalfi Coast",
                "subtitle": "A Curated Journey for The Anderson Family",
                "image_prompt": "https://placehold.co/1920x1080/1e293b/FFF?text=Amalfi+Coast"
            },
            {
                "layout": "split_right",
                "title": "Day 1: Arrival in Positano",
                "body": "Welcome to paradise. Your private chauffeur awaits at Naples Airport to whisk you away to Le Sirenuse.",
                "details": ["Stay: Le Sirenuse (5-Star)", " amenity: Infinity Pool"],
                "image_prompt": "https://placehold.co/1080x1920/e2e8f0/1e293b?text=Le+Sirenuse"
            }
        ]
    }
