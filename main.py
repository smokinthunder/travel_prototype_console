import asyncio
from data.raw_lego_data import get_selected_trip_data
from engine.ai_agent import generate_presentation_json
from engine.renderer import render_pdf

async def main():
    print("🚀 Starting Travel Prototype Console App...")
    
    # 1. Get the "Lego" Data (Simulating Agent selection)
    raw_data = get_selected_trip_data()
    print(f"📦 Input Data Loaded: {raw_data['meta']['client_name']} to {raw_data['meta']['destination']}")

    # 2. Pass to AI (GPT 5.1)
    # The AI decides the layout and writes the copy
    slide_json = generate_presentation_json(raw_data)
    
    # 3. Handle Placeholder Images (Simulating Auto-Picker)
    # In a real app, this logic would query the DB or Unsplash API
    print("🖼️  Injecting Placeholder Images...")
    for slide in slide_json.get("slides", []):
        if "image_prompt" not in slide or "http" not in slide["image_prompt"]:
             # Simple placeholder logic
            slide["image_prompt"] = "assets/car.jpg"

    # 4. Generate PDF
    await render_pdf(slide_json, output_filename="Travel_Itinerary_AI.pdf")

if __name__ == "__main__":
    asyncio.run(main())
