import os
import asyncio
from playwright.async_api import async_playwright
from jinja2 import Environment, FileSystemLoader

async def render_pdf(slide_data, output_filename="brochure.pdf"):
    print("🎨 Rendering Slides...")

    # 1. Setup Jinja2 Template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("gamma_theme.html")
    
    # 2. Inject Data into HTML
    html_content = template.render(slides=slide_data.get("slides", []))
    
    # Save temp file
    temp_html = "temp_slides.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 3. Playwright PDF Generation
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load file
        abs_path = os.path.abspath(temp_html)
        await page.goto(f"file://{abs_path}")
        
        # Configure for "Slide Deck" feel (Landscape A4)
        await page.pdf(
            path=output_filename,
            width="297mm", # A4 Landscape Width
            height="210mm", # A4 Landscape Height
            print_background=True
        )
        
        await browser.close()
    
    # Cleanup
    if os.path.exists(temp_html):
        os.remove(temp_html)
        
    print(f"✅ Generated: {output_filename}")
