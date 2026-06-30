import streamlit as st
from google import genai
from PIL import Image

# ==========================================================
# 🔑 API KEY CONFIGURATION
# ==========================================================
try:
    if "GEMINI_API_KEY" in st.secrets:
        MY_API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        MY_API_KEY = "AYOUR_GEMINI_API_KEY_HERE"  # <-- Paste your local test key here
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
    /* Centering the main header and description */
    .centered-title {
        text-align: center;
        font-size: calc(2.2rem + 1.5vw) !important;
        font-weight: bold;
        margin-bottom: 0.5rem;
        /* FIXED: This automatically switches between white and dark gray based on the user's theme */
        color: inherit !important; 
    }
    .centered-subtitle {
        text-align: center;
        color: #ADD8E6;
        font-size: calc(1.0rem + 0.3vw) !important;
        margin-bottom: 2rem;
    }
    
    /* Enlarge the section labels */
    .big-label {
        font-size: 1.4rem !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
    }

    /* Restricting maximum image preview height so it doesn't break mobile workflows */
    .stImage img {
        max-height: 300px !important;
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        display: block;
        border-radius: 8px;
    }

    /* Style ONLY the standalone main Execute button to be red. 
       Excludes choice buttons sitting inside grid columns. */
    div.stButton > button:not(div[data-testid="stColumn"] button) {
        background-color: #D32F2F !important; /* Rich Crimson Red */
        color: white !important;
        font-weight: bold !important;
        font-size: 1.25rem !important;
        padding: 0.6rem 1rem !important;
        border: none !important;
        border-radius: 8px !important;
        transition: background-color 0.3s ease, transform 0.1s ease !important;
    }
    
    /* Hover state modification strictly for the standalone red execution button */
    div.stButton > button:not(div[data-testid="stColumn"] button):hover {
        background-color: #B71C1C !important; /* Deeper cherry red on hover */
        color: white !important;
        border: none !important;
    }
    
    /* Style optimization for text tracking within choice buttons */
    div[data-testid="stColumn"] div.stButton > button {
        white-space: pre-wrap !important;
    }

    /* Custom Footer Styling */
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 0.9rem;
        color: #888888;
        margin-top: 50px;
    }
    .footer a {
        color: #D32F2F !important; /* Matches your red theme */
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
st.markdown('<div class="centered-subtitle">Upload any document or image to cleanly extract structured context via Gemini 2.5 Flash</div>', unsafe_allow_html=True)
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
        "Upload Image or PDF", 
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp', 'pdf'],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<p class="big-label">⚙️ Analysis Options</p>', unsafe_allow_html=True)
    st.caption("Click the giant buttons below to select/deselect features before analyzing:")

    # High-fidelity, macro-sized selectable button rows
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

    # Extra spacing before execution
    st.markdown(" ")
    analyze_button = st.button("🚀 EXECUTE SMART ANALYSIS", use_container_width=True)

with col_output:
    st.markdown('<p class="big-label">🖥️ Output Preview Window</p>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        if uploaded_file.type.startswith("image/"):
            img_preview = Image.open(uploaded_file)
            st.image(img_preview, caption=f"Active Target: {uploaded_file.name}")
            processing_data = img_preview
        else:
            st.info(f"📄 Active File: **{uploaded_file.name}** (PDF stream processing actively loaded.)")
            processing_data = uploaded_file.getvalue()

        # Handle Action Execution
        if analyze_button:
            with st.spinner("🤖 Synthesizing file layout and text context..."):
                
                # Dynamically construct the systemic task prompt
                prompt_parts = []
                if st.session_state.opt_ocr:
                    prompt_parts.append("Perform OCR: Read and extract all visible text exactly as it appears. Maintain formatting structure.")
                if st.session_state.opt_explain:
                    prompt_parts.append("Provide a simple, clear explanation about what is happening in this image or document context.")
                if st.session_state.opt_deep:
                    prompt_parts.append("Identify Visuals: Detect any diagrams, charts, signatures, logos, or photos, and describe exactly what they represent within the document structural layout.")
                
                if not prompt_parts:
                    st.warning("⚠️ Please select at least one of the large analysis options block modules above!")
                    st.stop()
                    
                final_prompt = "\n\n".join(prompt_parts)

                try:
                    if uploaded_file.type.startswith("image/"):
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[processing_data, final_prompt]
                        )
                    else:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[final_prompt, processing_data]
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