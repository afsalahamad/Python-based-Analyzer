# 📊 Python-based Analyzer & OCR Terminal Tool

An interactive, terminal-based application built in Python that leverages the Google GenAI SDK to perform intelligent Optical Character Recognition (OCR), visual content identification, and comprehensive document breakdowns. 

Whether you give it an image or a flattened PDF, this tool uses advanced vision capabilities to read text, understand illustrations, and synthesize a structured analysis based on your explicit preferences.

---

## 🚀 Key Features

* Dynamic User Menu: An interactive command-line system that prompts you for your output preference before processing.
* Intelligent OCR: Extracts text from flattened, scanned, or locked files where standard text selection is disabled.
* Visual Graphic Recognition: Identifies logos, diagrams, charts, or signatures and translates their meaning into descriptive text summaries.
* Multi-Format Processing: Ready out-of-the-box for major image formats (.png, .jpg, .jpeg, .webp, .bmp) and multi-page documents (.pdf).
* Safe Keys: Designed to prevent accidental API key leakage when pushing updates.

---

## 📋 Interactive Output Modes

When you pass a document to the tool, it halts and asks you to pick your analysis type:

1. Only Extracted Text (Pure OCR): Returns the exact raw text found in the file without extra commentary or summaries.
2. Text + Simple Explanation: Returns the raw text accompanied by a concise summary explaining what the document or image represents overall.
3. The Full Package (Deep Analysis): Combines raw text extraction, breakdown of visual graphs/logos, and an analysis of the item's document layout and purpose.

---

## 🛠️ Setup & Installation

1. Prerequisites
Make sure you have Python 3.10 or higher installed on your computer.

2. Clone the Repository
Open your terminal and clone your project repository locally:
git clone https://github.com/afsalahamad/Python-based-Analyzer.git
cd Python-based-Analyzer

3. Install Required Dependencies
Install the image processing and official Google GenAI packages via pip by running this command in your terminal:
pip install pillow google-genai

4. Configuration (API Key Placement)
Open your analyzer.py file in a text editor and paste your unique API key string into the dedicated variable near the top:
MY_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY"
(Remember: Keep this key confidential and do not share your modified file publicly!)

---

## 💻 How To Run

To analyze a file, pass its directory path as an argument when calling the script in your terminal:
python analyzer.py your_document_name.png

---

## 📝 Example Usage Interface

When you execute the program, the terminal output will look like this:

PS C:\Users\...> python analyzer.py receipt.jpg

🔄 Processing 'receipt.jpg' based on your preference... Please wait.

========================================
📋 SELECT OUTPUT TYPE
========================================
1. Only extracted text (Pure OCR)
2. Only extracted text + Simple explanation about the given image
3. Full package: Text + Explanation + Detailed deep analysis
========================================
Enter your choice (1, 2, or 3): 2

---

## 🤝 Contributing

Contributions, bug reporting, and feature requests are welcome! If you are a student or developer looking to expand this, feel free to fork the repo and submit a pull request—such as wrapping this core script into a visual web-based browser UI next.