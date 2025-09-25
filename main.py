import streamlit as st
import requests

# Streamlit page configuration
st.set_page_config(
    page_title="Leaf Disease Detection",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e3f2fd 0%, #f7f9fa 100%);
}
.result-card {
    background: rgba(255,255,255,0.95);
    border-radius: 18px;
    box-shadow: 0 4px 24px rgba(44,62,80,0.10);
    padding: 2.5em 2em;
    margin-top: 1.5em;
    margin-bottom: 1.5em;
    transition: box-shadow 0.3s;
}
.result-card:hover {
    box-shadow: 0 8px 32px rgba(44,62,80,0.18);
}
.disease-title {
    color: #1b5e20;
    font-size: 2.2em;
    font-weight: 700;
    margin-bottom: 0.5em;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px #e0e0e0;
}
.section-title {
    color: #1976d2;
    font-size: 1.25em;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.timestamp {
    color: #616161;
    font-size: 0.95em;
    margin-top: 1.2em;
    text-align: right;
}
.info-badge {
    display: inline-block;
    background: #e3f2fd;
    color: #1976d2;
    border-radius: 8px;
    padding: 0.3em 0.8em;
    font-size: 1em;
    margin-right: 0.5em;
    margin-bottom: 0.3em;
}
.symptom-list, .cause-list, .treatment-list {
    margin-left: 1em;
    margin-bottom: 0.5em;
}
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div style='text-align: center; margin-top: 1em;'>
    <span style='font-size:2.5em;'>🌿</span>
    <h1 style='color: #1565c0; margin-bottom:0;'>Leaf Disease Detection</h1>
    <p style='color: #616161; font-size:1.15em;'>Upload a leaf image to detect diseases and get expert recommendations.</p>
</div>
""", unsafe_allow_html=True)

# API URL
api_url = "http://leaf-diseases-detect.vercel.app"

# Layout columns
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader(
        "Upload Leaf Image", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        st.image(uploaded_file, caption="Preview")

with col2:
    if uploaded_file:
        if st.button("🔍 Detect Disease", use_container_width=True):
            with st.spinner("Analyzing image and contacting API..."):
                try:
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                    }
                    response = requests.post(f"{api_url}/disease-detection-file", files=files)

                    if response.status_code == 200:
                        result = response.json()

                        # Display result card
                        st.markdown("<div class='result-card'>", unsafe_allow_html=True)

                        # Invalid image
                        if result.get("disease_type") == "invalid_image":
                            st.markdown("<div class='disease-title'>⚠️ Invalid Image</div>", unsafe_allow_html=True)
                            st.markdown(
                                "<div style='color: #ff5722; font-size: 1.1em; margin-bottom: 1em;'>Please upload a clear image of a plant leaf for accurate disease detection.</div>", unsafe_allow_html=True
                            )

                        # Disease detected
                        elif result.get("disease_detected"):
                            st.markdown(f"<div class='disease-title'>🦠 {result.get('disease_name', 'N/A')}</div>", unsafe_allow_html=True)
                            st.markdown(f"<span class='info-badge'>Type: {result.get('disease_type', 'N/A')}</span>", unsafe_allow_html=True)
                            st.markdown(f"<span class='info-badge'>Severity: {result.get('severity', 'N/A')}</span>", unsafe_allow_html=True)
                            st.markdown(f"<span class='info-badge'>Confidence: {result.get('confidence', 'N/A')}%</span>", unsafe_allow_html=True)

                        # Healthy leaf
                        else:
                            st.markdown("<div class='disease-title'>✅ Healthy Leaf</div>", unsafe_allow_html=True)
                            st.markdown(
                                "<div style='color: #4caf50; font-size: 1.1em; margin-bottom: 1em;'>No disease detected in this leaf. The plant appears to be healthy!</div>", unsafe_allow_html=True
                            )
                            st.markdown(f"<span class='info-badge'>Status: {result.get('disease_type', 'healthy')}</span>", unsafe_allow_html=True)
                            st.markdown(f"<span class='info-badge'>Confidence: {result.get('confidence', 'N/A')}%</span>", unsafe_allow_html=True)

                        # Common sections: Symptoms, Causes, Treatment
                        for section, key in [("Symptoms", "symptoms"), ("Possible Causes", "possible_causes"), ("Treatment", "treatment")]:
                            if result.get(key):
                                st.markdown(f"<div class='section-title'>{section}</div>", unsafe_allow_html=True)
                                st.markdown(f"<ul class='{key}-list'>", unsafe_allow_html=True)
                                for item in result.get(key, []):
                                    st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
                                st.markdown("</ul>", unsafe_allow_html=True)

                        # Timestamp
                        st.markdown(f"<div class='timestamp'>🕒 {result.get('analysis_timestamp', 'N/A')}</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    else:
                        st.error(f"API Error: {response.status_code}")
                        st.write(response.text)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
