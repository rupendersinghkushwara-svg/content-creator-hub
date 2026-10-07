import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="Content Creator Hub", page_icon="🚀", layout="wide")

st.title("🚀 All-in-One Content Creator Hub")

# Gemini Client Initialization using Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Gemini API Key नहीं मिली! कृपया Streamlit Settings -> Secrets में GEMINI_API_KEY सेट करें।")
else:
    client = genai.Client(api_key=api_key)

    # Sidebar Navigation
    st.sidebar.header("📌 Quick Navigation")
    menu = st.sidebar.radio("Go to:", ["Daily Checklist", "🤖 AI Content Ideas", "Free Design Tools"])

    # 1. Daily Checklist
    if menu == "Daily Checklist":
        st.subheader("📋 Today's Creator Tasks")
        st.checkbox("Check Trending Hashtags")
        st.checkbox("Brainstorm 3 Content Ideas")
        st.checkbox("Design Post Graphic (Canva/Figma)")
        st.checkbox("Schedule & Publish Posts")
        st.checkbox("Analyze Yesterday's Engagement")
        if st.button("Save Daily Progress"):
            st.success("Progress Saved Successfully!")

    # 2. AI Content Generator
    elif menu == "🤖 AI Content Ideas":
        st.subheader("🤖 AI Powered Content & Hashtag Generator")
        
        niche = st.text_input("अपना टॉपिक या नीश (Niche) लिखें:", placeholder="उदा: Tech, Fitness, Digital Marketing, Vlogging")
        content_type = st.selectbox("कंटेंट का प्रकार चुनें:", ["Instagram Reel / Short Script", "YouTube Video Ideas", "Viral Hashtags", "Post Captions"])
        
        if st.button("Generate Ideas 🚀"):
            if niche:
                with st.spinner("AI आपके लिए विचार जनरेट कर रहा है..."):
                    prompt = f"Give me 3 creative, high-engaging ideas for {content_type} on the topic '{niche}'. Include hooks, main content, and recommended hashtags."
                    response = gemini-2.0-flash(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                    st.markdown("### 💡 AI Recommendations:")
                    st.write(response.text)
            else:
                st.warning("कृपया पहले अपना टॉपिक या नीश लिखें!")

    # 3. Free Design Tools Directory
    elif menu == "Free Design Tools":
        st.subheader("🛠️ Free Tools for Content Creators")
        tools = {
            "Design": ["Canva (canva.com)", "Photopea (photopea.com)"],
            "AI Tools": ["Upscayl (upscayl.org)", "Vidyo AI (vidyo.ai)"],
            "Infographics": ["Google Charts", "Visme", "Datamatic"]
        }
        for category, list_of_tools in tools.items():
            st.write(f"**{category}**")
            for tool in list_of_tools:
                st.write(f"- {tool}")