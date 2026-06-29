import os
import sys
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

# ==========================================
# 🔑 INSERT YOUR API KEY HERE
# ==========================================
MY_API_KEY = "INSERT YOUR API KEY HERE"
# ==========================================

# Initialize the Gemini Client using the key defined above
try:
    if MY_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not MY_API_KEY:
        print("Error: Please replace 'YOUR_GEMINI_API_KEY_HERE' with your actual Gemini API key inside the code.")
        sys.exit(1)
        
    client = genai.Client(api_key=MY_API_KEY)
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    sys.exit(1)

def get_user_choice():
    print("\n" + "="*40)
    print("📋 SELECT OUTPUT TYPE")
    print("="*40)
    print("1. Only extracted text (Pure OCR)")
    print("2. Only extracted text + Simple explanation about the given image")
    print("3. Full package: Text + Explanation + Detailed deep analysis")
    print("="*40)
    
    while True:
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("❌ Invalid input. Please type 1, 2, or 3.")

def analyze_file(file_path_str):
    file_path = Path(file_path_str)
    
    if not file_path.exists():
        print(f"Error: File '{file_path_str}' not found.")
        return

    # Ask the user what they want BEFORE running the AI
    choice = get_user_choice()

    # Dynamic prompt assignment based on user choice
    if choice == '1':
        prompt = "Perform OCR: Read and extract all visible text exactly as it appears. Do not explain or summarize anything else."
    elif choice == '2':
        prompt = "1. Perform OCR: Extract all readable text exactly as it appears.\n2. Provide a simple, clear explanation about what is happening in this image or document."
    else:
        prompt = """
        Analyze this uploaded document/image entirely. 
        1. Perform OCR: Extract all readable text exactly as it appears.
        2. Identify Visuals: If there are any diagrams, charts, signatures, logos, or photos, describe exactly what they are and what they represent.
        3. Final Summary: Provide a detailed, structured description of the overall content, purpose, and layout of the file.
        """

    print(f"\n🔄 Processing '{file_path.name}' based on your preference... Please wait.")

    try:
        # Check if file is an image
        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.bmp']:
            image = Image.open(file_path)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[image, prompt]
            )
            
        # Check if file is a PDF
        elif file_path.suffix.lower() == '.pdf':
            uploaded_file = client.files.upload(file=file_path)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[uploaded_file, prompt]
            )
            
            # Clean up cloud file
            client.files.delete(name=uploaded_file.name)
            
        else:
            print("Unsupported file format. Please use a PDF or an Image (PNG, JPG, etc.).")
            return

        # Print the final result back to the terminal
        print("\n" + "="*50)
        print("📊 ANALYSIS RESULTS")
        print("="*50 + "\n")
        print(response.text)
        print("\n" + "="*50)

    except Exception as e:
        print(f"\nAn error occurred during processing: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <path_to_file>")
        print("Example: python analyzer.py receipt.jpg")
        sys.exit(1)
        
    target_file = sys.argv[1]
    analyze_file(target_file)