import os
import asyncio
from playwright.async_api import async_playwright
from jinja2 import Environment, FileSystemLoader

async def render_pdf(slide_data, output_filename="brochure.pdf"):
    print("🎨 Rendering Slides...")
    
    # DEBUG: Check if we actually have slides to render
    slide_count = len(slide_data.get("slides", []))
    print(f"📊 Rendering {slide_count} slides...")

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("gamma_theme.html")
    html_content = template.render(slides=slide_data.get("slides", []))
    
    # Save temp file for inspection
    temp_html = "temp_debug.html" # Renamed to keep it so you can open it manually
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"📝 HTML saved to {temp_html} (Open this file in Chrome to check layout)")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        abs_path = os.path.abspath(temp_html)
        await page.goto(f"file://{abs_path}")
        
        # WAIT for any potential images/fonts to load
        await page.wait_for_timeout(1000) 
        
        await page.pdf(
            path=output_filename,
            width="297mm",
            height="210mm",
            print_background=True # This is critical for colors
        )
        
        await browser.close()
        
    print(f"✅ Generated: {output_filename}")
