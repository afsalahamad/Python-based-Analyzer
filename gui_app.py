import streamlit as st
from google import genai
from PIL import Image

# ==========================================================
# 🔑 API KEY CONFIGURATION
# ==========================================================
# If deploying to Streamlit Cloud, it reads from advanced secrets.
# For local testing, replace the string below with your actual key.
try:
    if "GEMINI_API_KEY" in st.secrets:
        MY_API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        MY_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # <-- Paste your local test key here
except Exception:
    MY_API_KEY = "YOUR_GEMINI_API_KEY_HERE"      # <-- Paste your local test key here
# ==========================================================

# Initialize the Gemini Client
try:
    if MY_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not MY_API_KEY:
        st.error("⚠️ Missing API Key! Please paste your Gemini API key inside the 'gui_app.py' code or configure Streamlit Secrets.")
        st.stop()
        
    client = genai.Client(api_key=MY_API_KEY)
except Exception as e:
    st.error(f"❌ Error initializing Gemini Client: {e}")
    st.stop()

# --- Page UI Configuration ---
st.set_page_config(page_title="Smart OCR Analyzer", page_icon="📊", layout="wide")

st.title("📊 Smart OCR & File Analyzer Dashboard")
st.markdown("Upload any flattened PDF document or text-based image to extract details, perform OCR, or request custom deep explanations.")
st.markdown("---")

# Create two columns for clean layout alignment
col_input, col_output = st.columns([1, 1.5])

with col_input:
    st.subheader("📁 Upload & Configuration")
    
    # 1. File Uploader Widget
    uploaded_file = st.file_uploader(
        "Drag and drop or browse files", 
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp', 'pdf']
    )
    
    # 2. Output Radio Choice Menu
    analysis_type = st.radio(
        "What analysis configuration do you want?",
        [
            "1. Only extracted text (Pure OCR)",
            "2. Text + Simple explanation about the given file",
            "3. Full package: Text + Explanation + Detailed visual layout analysis"
        ]
    )
    
    # 3. Execution Button
    analyze_button = st.button("🚀 Run Smart Analysis", use_container_width=True)

with col_output:
    st.subheader("🖥️ Result Window")
    
    if uploaded_file is not None:
        # Show file preview details
        st.info(f"Loaded File: {uploaded_file.name} ({uploaded_file.type})")
        
        # Display visual image preview if user uploaded an image
        if uploaded_file.type.startswith("image/"):
            img_preview = Image.open(uploaded_file)
            st.image(img_preview, caption="Uploaded File Preview", use_container_width=True)
            processing_data = img_preview
        else:
            st.warning("📄 PDF files uploaded will be sent securely to the processor stream directly without live preview thumbnail.")
            processing_data = uploaded_file.getvalue()

        # Handle Action Triggers
        if analyze_button:
            with st.spinner("🤖 Processing file via Gemini GenAI... Please wait."):
                choice = analysis_type.split(".")[0]
                
                # Dynamic Prompt Logic assignment
                if choice == "1":
                    prompt = "Perform OCR: Read and extract all visible text exactly as it appears. Do not explain or summarize anything else."
                elif choice == "2":
                    prompt = "1. Perform OCR: Extract all readable text exactly as it appears.\n2. Provide a simple, clear explanation about what is happening in this image or document."
                else:
                    prompt = """
                    Analyze this uploaded document/image entirely. 
                    1. Perform OCR: Extract all readable text exactly as it appears.
                    2. Identify Visuals: If there are any diagrams, charts, signatures, logos, or photos, describe exactly what they are and what they represent.
                    3. Final Summary: Provide a detailed, structured description of the overall content, purpose, and layout of the file.
                    """

                try:
                    # Run generative call handling context variations
                    if uploaded_file.type.startswith("image/"):
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[processing_data, prompt]
                        )
                    else:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[prompt, processing_data]
                        )
                    
                    st.success("✅ Analysis Complete!")
                    st.markdown("### 📊 Extracted Breakdown Output:")
                    st.write(response.text)
                    
                except Exception as ai_err:
                    st.error(f"AI Generation Failed: {ai_err}")
    else:
        st.write("Awaiting document upload. Your results will render dynamically here once you trigger processing configuration.")