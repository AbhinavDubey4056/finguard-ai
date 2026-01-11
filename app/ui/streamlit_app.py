def process_analysis(uploaded_file, endpoint_url):
    """Reusable function to process files and display results consistently."""
    with st.spinner("Processing through Edge AI Pipeline..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(endpoint_url, files=files)
            
            if response.status_code == 200:
                res = response.json()
                score = res["deepfake_score"]
                decision = res["decision"]
                explanation = res["explanation"]

                st.success("Analysis Complete")
                st.metric(label="Deepfake Confidence", value=f"{round(score * 100, 2)}%")
                
                verdict = decision["verdict"]
                if verdict == "DEEPFAKE":
                    st.error(f"VERDICT: {verdict}")
                elif verdict == "REAL":
                    st.success(f"VERDICT: {verdict}")
                else:
                    st.warning(f"VERDICT: {verdict}")

                with st.expander("📝 View AI Explanation", expanded=True):
                    st.write(explanation)
                    st.caption(f"Risk Level: {decision['risk_level']}")
            else:
                st.error(f"Backend Error: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to Edge Agent backend: {e}")
            
            
            
            
"""
app/ui/streamlit_app.py

Responsibilities:
- Provide a user-friendly interface for video uploads.
- Communicate with the FastAPI backend.
- Visualize detection scores, risk levels, and AI explanations.
"""

import streamlit as st
import requests
import os

# Page Configuration
st.set_page_config(
    page_title="Deepfake Edge Agent",
    page_icon="🛡️",
    layout="wide"
)

# Sidebar: Info and Configuration
with st.sidebar:
    st.title("🛡️ Agent Control")
    st.markdown("---")
    st.info("System Mode: **EDGE_OFFLINE**")
    st.write("This agent analyzes videos for digital manipulation locally.")
    
    # Optional threshold adjustment for visualization
    threshold = st.slider("Sensitivity Threshold", 0.0, 1.0, 0.75)

# Main Dashboard UI

st.title("Deepfake Detection Dashboard")
st.subheader("Autonomous Forensic Analysis")

# Create tabs for Video and Audio analysis
tab_video, tab_audio = st.tabs(["🎥 Video Analysis", "🎙️ Audio Analysis"])

with tab_video:
    uploaded_video = st.file_uploader("Upload a video for analysis", type=["mp4", "avi", "mov"], key="video_uploader")
    if uploaded_video:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.video(uploaded_video)
        with col2:
            if st.button("🚀 Analyze Video"):
                # Call existing /analyze/video endpoint
                process_analysis(uploaded_video, "http://localhost:8000/analyze/video")

with tab_audio:
    uploaded_audio = st.file_uploader("Upload audio for analysis", type=["wav", "mp3", "flac"], key="audio_uploader")
    if uploaded_audio:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.audio(uploaded_audio) # Standard Streamlit audio player
        with col2:
            if st.button("🚀 Analyze Audio"):
                # Call new /analyze/audio endpoint
                process_analysis(uploaded_audio, "http://localhost:8000/analyze/audio")