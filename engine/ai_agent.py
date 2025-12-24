import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# CHECK 1: Ensure API Key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file.")

client = OpenAI(api_key=api_key)

# CHECK 2: Use the correct model name. 
# If 'gpt-5.2' throws an error, switch back to 'gpt-4o' or 'gpt-4-turbo'
MODEL_NAME = "gpt-4o" 

SYSTEM_PROMPT = """
You are a High-End Travel Director. Create a cinematic, slide-by-slide visual journey.

YOUR TASK:
Convert the raw itinerary into a JSON list of slides. 
Break down each day into multiple focused slides to keep it "skimmable" and visual.

REQUIRED SLIDE FLOW:
1. **Title Slide**: Trip Name & Client Name.
2. **Timeline Slide**: A visual summary of the whole trip (List of Day Titles).
3. **Day Loops**: For each day, generate:
    a. "Day Intro" Slide: A short, punchy summary of what happens that day.
    b. "Feature" Slides: Separate slides for key Hotels or Major Activities. 
       (e.g., Don't just list the hotel in the text; give the Hotel its own slide with a 'hotel_focus' layout).

LAYOUT TYPES TO USE:
- 'title_hero' (For the Trip Title)
- 'timeline_view' (For the trip overview)
- 'day_intro' (Minimal text, big number "Day 1")
- 'hotel_focus' (Dedicated to accommodation, emphasize luxury)
- 'activity_focus' (Dedicated to an experience, emphasize emotion)

JSON STRUCTURE:
{
  "slides": [
    {
      "layout": "timeline_view",
      "title": "Your Journey at a Glance",
      "timeline_items": [
         {"day": "Day 1", "title": "Arrival in Positano"},
         {"day": "Day 2", "title": "Capri by Boat"}
      ]
    },
    {
      "layout": "day_intro",
      "day_label": "Day 1",
      "title": "The Amalfi Arrival",
      "image_prompt": "Sunset over Positano"
    },
    {
      "layout": "hotel_focus",
      "title": "Le Sirenuse",
      "tags": ["5-Star", "Sea View"],
      "body": "A legendary hotel with an infinity pool overlooking the bay.",
      "image_prompt": "Le Sirenuse pool"
    }
  ]
}
"""

def generate_presentation_json(raw_data):
    print(f"🧠 Sending data to AI Model ({MODEL_NAME})...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Create slides for this trip data:\n{json.dumps(raw_data)}"}
            ]
        )
        
        content = response.choices[0].message.content
        
        # DEBUG: Print what the AI actually sent back
        print("\n--- RAW AI RESPONSE ---")
        print(content)
        print("-----------------------\n")

        parsed_json = json.loads(content)
        
        # SAFETY FIX: Ensure 'slides' key exists
        if "slides" not in parsed_json:
            print("⚠️ JSON format warning: Root key 'slides' missing. Attempting auto-fix.")
            # If AI returned a list directly, wrap it
            if isinstance(parsed_json, list):
                parsed_json = {"slides": parsed_json}
            # If AI returned a different key (like 'presentation'), use that
            elif len(parsed_json.keys()) == 1:
                key = list(parsed_json.keys())[0]
                parsed_json = {"slides": parsed_json[key]}
            
        return parsed_json

    except Exception as e:
        print(f"❌ AI Generation Error: {e}")
        # Return a fallback slide so the PDF isn't empty
        return {
            "slides": [
                {
                    "layout": "title_hero",
                    "title": "Error Generating Content",
                    "subtitle": str(e),
                    "image_prompt": ""
                }
            ]
        }
