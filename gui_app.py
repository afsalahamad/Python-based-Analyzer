import streamlit as st
from google import genai
from PIL import Image
import io

# Safe library imports
try:
    from pdf2image import convert_from_bytes
except ImportError:
    st.error("Please add 'pdf2image' to your requirements.txt file.")

try:
    from pptx import Presentation
except ImportError:
    st.error("Please add 'python-pptx' to your requirements.txt file.")

# ==========================================================
# 🔑 API KEY CONFIGURATION
# ==========================================================
try:
    if "GEMINI_API_KEY" in st.secrets:
        MY_API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        MY_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
except Exception:
    MY_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
# ==========================================================

# Initialize the Gemini Client
try:
    if MY_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not MY_API_KEY:
        st.error("⚠️ Missing API Key! Please configure your Gemini API key.")
        st.stop()
        
    client = genai.Client(api_key=MY_API_KEY)
except Exception as e:
    st.error(f"❌ Error initializing Gemini Client: {e}")
    st.stop()

# --- Page UI Configuration ---
st.set_page_config(page_title="Smart OCR Analyzer", page_icon="📊", layout="wide")

# Custom CSS for absolute responsiveness, big text, layout centering, and the isolated RED action button
st.markdown("""
    <style>
    .centered-title {
        text-align: center;
        font-size: calc(2.2rem + 1.5vw) !important;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: inherit !important; 
    }
    .centered-subtitle {
        text-align: center;
        color: #A0A0A0;
        font-size: calc(1.0rem + 0.3vw) !important;
        margin-bottom: 1.5rem;
    }
    .welcome-container {
        text-align: center;
        max-width: 800px;
        margin: 0 auto 2.5rem auto;
        padding: 20px;
        background-color: rgba(128, 128, 128, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .welcome-text {
        font-size: 1.15rem !important;
        line-height: 1.6;
        color: inherit;
        margin-bottom: 10px;
    }
    .welcome-features {
        font-size: 1.05rem !important;
        font-weight: 500;
        color: #D32F2F;
        margin-top: 8px;
    }
    .big-label {
        font-size: 1.4rem !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
    }
    .stImage img {
        max-height: 300px !important;
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        display: block;
        border-radius: 8px;
    }
    div.stButton > button:not(div[data-testid="stColumn"] button) {
        background-color: #D32F2F !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.25rem !important;
        padding: 0.6rem 1rem !important;
        border: none !important;
        border-radius: 8px !important;
        transition: background-color 0.3s ease, transform 0.1s ease !important;
    }
    div.stButton > button:not(div[data-testid="stColumn"] button):hover {
        background-color: #B71C1C !important;
        color: white !important;
        border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div.stButton > button {
        font-size: inherit;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 0.9rem;
        color: #888888;
        margin-top: 50px;
    }
    .footer a {
        color: #D32F2F !important;
        text-decoration: none;
        font-weight: bold;
    }
    .footer a:hover {
        text-decoration: underline !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Centralized Title Banner ---
st.markdown('<div class="centered-title">📊 Smart OCR & File Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="centered-subtitle">Upload any document, image, or presentation to cleanly extract structured context via Gemini 2.5 Flash</div>', unsafe_allow_html=True)

# --- FIRST-TIME WELCOME BLOCK ---
if 'first_time_load' not in st.session_state:
    st.session_state.first_time_load = True

if st.session_state.first_time_load:
    st.toast("👋 Welcome to Smart OCR & File Analyzer!")
    welcome_html = """
    <div class="welcome-container">
        <p class="welcome-text">
            🚀 <strong>Welcome!</strong> This production-grade utility combines the analytical layout processing of Python and Streamlit with the multimodal vision intelligence of the <strong>Gemini 2.5 Flash</strong> model engine.
        </p>
        <p class="welcome-features">
            🔍 Intelligent OCR Text Parsing &nbsp;|&nbsp; 📝 Conversational Context Explanations &nbsp;|&nbsp; 🔬 Deep Visual Asset Auditing
        </p>
    </div>
    """
    st.markdown(welcome_html, unsafe_allow_html=True)
    st.session_state.first_time_load = False

st.markdown("---")

# --- Initialize Session States for Selection ---
if 'opt_ocr' not in st.session_state: st.session_state.opt_ocr = True
if 'opt_explain' not in st.session_state: st.session_state.opt_explain = False
if 'opt_deep' not in st.session_state: st.session_state.opt_deep = False

# --- UI Layout Grid Setup ---
col_input, col_output = st.columns([1, 1.2], gap="large")

with col_input:
    st.markdown('<p class="big-label">📁 Drag & Drop Document</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload Image, PDF, or PowerPoint", 
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp', 'pdf', 'pptx'],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<p class="big-label">⚙️ Analysis Options</p>', unsafe_allow_html=True)
    st.caption("Click the giant buttons below to select/deselect features before analyzing:")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button(
            f"🔍 OCR Text\n[{'ACTIVE' if st.session_state.opt_ocr else 'OFF'}]", 
            use_container_width=True, 
            type="primary" if st.session_state.opt_ocr else "secondary"
        ):
            st.session_state.opt_ocr = not st.session_state.opt_ocr
            st.rerun()

    with btn_col2:
        if st.button(
            f"📝 Explanation\n[{'ACTIVE' if st.session_state.opt_explain else 'OFF'}]", 
            use_container_width=True, 
            type="primary" if st.session_state.opt_explain else "secondary"
        ):
            st.session_state.opt_explain = not st.session_state.opt_explain
            st.rerun()

    with btn_col3:
        if st.button(
            f"🔬 Deep Analysis\n[{'ACTIVE' if st.session_state.opt_deep else 'OFF'}]", 
            use_container_width=True, 
            type="primary" if st.session_state.opt_deep else "secondary"
        ):
            st.session_state.opt_deep = not st.session_state.opt_deep
            st.rerun()

    st.markdown(" ")
    analyze_button = st.button("🚀 EXECUTE SMART ANALYSIS", use_container_width=True)

with col_output:
    st.markdown('<p class="big-label">🖥️ Output Preview Window</p>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        file_name = uploaded_file.name.lower()
        processing_data = None
        is_pptx = file_name.endswith('.pptx')
        is_pdf = file_name.endswith('.pdf')
        
        if not is_pdf and not is_pptx:
            # Native image path
            img_preview = Image.open(uploaded_file)
            st.image(img_preview, caption=f"Active Target: {uploaded_file.name}")
            processing_data = img_preview
        elif is_pdf:
            st.info(f"📄 Active PDF Document: **{uploaded_file.name}**")
            try:
                pdf_images = convert_from_bytes(uploaded_file.read(), first_page=1, last_page=1)
                if pdf_images:
                    processing_data = pdf_images[0]
                    st.image(processing_data, caption="First Page Preview (Converted)", use_container_width=True)
            except Exception as pdf_err:
                st.warning("⚠️ Visual preview unavailable. Passing document payload directly.")
                uploaded_file.seek(0)
                processing_data = uploaded_file.getvalue()
        elif is_pptx:
            st.info(f"📊 Active PowerPoint Presentation: **{uploaded_file.name}**")
            try:
                prs = Presentation(uploaded_file)
                pptx_text_parts = []
                for i, slide in enumerate(prs.slides, 1):
                    pptx_text_parts.append(f"--- Slide {i} ---")
                    for shape in slide.shapes:
                        if hasattr(shape, "text") and shape.text.strip():
                            pptx_text_parts.append(shape.text.strip())
                
                # Bundle the slide details into a solid context block for the prompt pipeline
                processing_data = "\n".join(pptx_text_parts)
                st.success(f"✅ Successfully parsed {len(prs.slides)} slides! Ready for analysis.")
            except Exception as pptx_err:
                st.error(f"Failed to parse PowerPoint structure: {pptx_err}")

        # Handle Action Execution
        if analyze_button and processing_data is not None:
            with st.spinner("🤖 Synthesizing file layout and text context..."):
                prompt_parts = []
                if st.session_state.opt_ocr:
                    prompt_parts.append("Perform OCR / Content Extraction: Read and extract all contents exactly as they appear. Maintain structure.")
                if st.session_state.opt_explain:
                    prompt_parts.append("Provide a clear, cohesive narrative explanation detailing the primary subject matter of this file.")
                if st.session_state.opt_deep:
                    prompt_parts.append("Identify layout and presentation aesthetics: Analyze structural topics, core insights, and provide a granular breakdown.")
                
                if not prompt_parts:
                    st.warning("⚠️ Please select at least one analysis option block module above!")
                    st.stop()
                    
                final_prompt = "\n\n".join(prompt_parts)

                try:
                    # Pass context clean based on string vs object data types
                    if isinstance(processing_data, str):
                        full_content = f"{final_prompt}\n\nHere is the presentation content data text extracted directly from the slides:\n{processing_data}"
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=full_content
                        )
                    else:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[processing_data, final_prompt] if not isinstance(processing_data, bytes) else [final_prompt, processing_data]
                        )
                    
                    st.success("✅ File Successfully Analyzed!")
                    st.markdown("### 📝 Analysis Summary Breakdown:")
                    st.info(response.text)
                    
                except Exception as ai_err:
                    st.error(f"AI Generation Failed: {ai_err}")
    else:
        st.info("Awaiting file upload. Drop an item on the left column block to initiate data rendering.")

# --- Footer Section ---
st.markdown("---") 
footer_html = """
<div class="footer">
    © 2026 Analyzer By Afsal. All Rights Reserved. | 
    🌐 Source Code: <a href="https://github.com/afsalahamad/Python-based-Analyzer" target="_blank">GitHub Repository</a>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)