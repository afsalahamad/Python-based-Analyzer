# 📊 Smart OCR & File Analyzer

A beautifully responsive, interactive web application built in Python using Streamlit and the Google GenAI SDK. This tool leverages the advanced vision capabilities of Gemini 2.5 Flash to perform intelligent Optical Character Recognition (OCR), visual layout parsing, and conversational document synthesis.

Designed with a fluid grid system, the interface automatically scales and optimizes layouts for a comfortable user experience on both desktop screens and mobile smartphones.

---

## 🔗 Live Production Demo
👉 [Click Here to Use the Live Web App](https://python-based-analyzer-2vbhknumyjwzfui7ddykxc.streamlit.app)

---

## 🚀 Key Features

* 📱 Complete Mobile Responsiveness: Custom fluid layout structure that scales seamlessly from ultra-wide PC monitors down to smartphone displays.
* 🌓 Universal Theme Adaptation: Smart text inheritance styling that remains perfectly readable across both native Light Mode and Dark Mode environments.
* ⚙️ High-Fidelity Interactive Grid: Large, thumb-friendly choice selectors replacing small checkboxes, letting users customize their text analysis with a tap.
* 🚨 High-Contrast UI Callouts: Vibrant, stylized actions buttons and fluid thumbnail constraints that keep large document files centered and compact.
* 🔒 Enterprise Secrets Isolation: Built-in production architecture utilizing Streamlit Cloud Environment variables to protect confidential API access keys.

---

## 📋 Custom Prompt Matrix Engine

Users can tap individual blocks or mix-and-match settings simultaneously to change what the AI looks for:

1. 🔍 OCR Text [ACTIVE / OFF]: Commands the core model engine to parse all alphanumeric blocks exactly as they appear while preserving spacing.
2. 📝 Explanation [ACTIVE / OFF]: appends a clear, conversational description breaking down what the transaction, scene, or document context implies.
3. 🔬 Deep Analysis [ACTIVE / OFF]: Triggers a granular graphic investigation inspecting structural charts, blueprints, logos, signatures, or nested layout geometry.

---

## 🛠️ Step-by-Step Local Deployment

1. System Prerequisites
Ensure you have Python 3.10 or higher running on your system.

2. Clone and Jump to Target Folder
Open your command terminal and execute:
git clone https://github.com/afsalahamad/Python-based-Analyzer.git
cd Python-based-Analyzer

3. Local Environment Verification
Install dependencies locally using pip:
pip install streamlit google-genai pillow

4. Apply API Access Configuration
Open your gui_app.py file inside your editor and locate the configuration segment to substitute your fallback key manually:
MY_API_KEY = "YOUR_CONFIDENTIAL_API_KEY_HERE"

5. Boot the Local Server Instance
Run the local compiler to instantiate your dashboard environment:
streamlit run gui_app.py

---

## 🌍 GitHub Cloud Deployment Guide

To keep the platform public without revealing your local API keys, deploy the asset to Streamlit Cloud using the configurations below:

1. Repository Mapping Structure
Ensure your repo contains the following runtime structural maps:
├── gui_app.py        <- Main UI app entry point
└── requirements.txt  <- Tells cloud environments what dependencies to build

2. Requirements Manifest File
Ensure your requirements.txt contains exactly these lines:
streamlit
google-genai
pillow

3. Cloud Secrets Assignment
Inside your Streamlit Share Dashboard settings panel, drop your variables securely inside Advanced Settings -> Secrets:
GEMINI_API_KEY = "your_actual_confidential_production_api_key"

---

## 🤝 Contributing & Scope

Contributions, layout modifications, or feature proposals are absolutely welcome. Feel free to submit an active branch fork request, open an issue card, or play around with adding multi-language translation flags next!

© 2026 Afsal Hamad. All Rights Reserved.
