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
st.subheader("Autonomous Forensic Video Analysis")

uploaded_file = st.file_uploader("Upload a video for analysis", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # 1. Preview the Video
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.video(uploaded_file)
    
    with col2:
        if st.button("🚀 Analyze Video"):
            with st.spinner("Processing through Edge AI Pipeline..."):
                try:
                    # 2. Forward to Backend API (main.py)
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post("http://localhost:8000/analyze/video", files=files)
                    
                    if response.status_code == 200:
                        res = response.json()
                        score = res["deepfake_score"]
                        decision = res["decision"]
                        explanation = res["explanation"]

                        # 3. Display Results
                        st.success("Analysis Complete")
                        
                        # Big Metric for Score
                        st.metric(label="Deepfake Confidence", value=f"{round(score * 100, 2)}%")
                        
                        # Color-coded Verdict
                        verdict = decision["verdict"]
                        if verdict == "DEEPFAKE":
                            st.error(f"VERDICT: {verdict}")
                        elif verdict == "REAL":
                            st.success(f"VERDICT: {verdict}")
                        else:
                            st.warning(f"VERDICT: {verdict}")

                        # Explanation Card
                        with st.expander("📝 View AI Explanation", expanded=True):
                            st.write(explanation)
                            st.caption(f"Risk Level: {decision['risk_level']}")
                        
                        # Raw JSON for debugging/audit
                        with st.expander("🔍 View Raw Metadata"):
                            st.json(res)

                    else:
                        st.error(f"Backend Error: {response.text}")
                
                except Exception as e:
                    st.error(f"Could not connect to Edge Agent backend: {e}")

else:
    st.info("Please upload a video file to begin analysis.")