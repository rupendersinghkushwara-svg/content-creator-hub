import streamlit as st
import time
from google import genai

st.set_page_config(page_title="Content Creator Hub", page_icon="🚀", layout="wide")
st.title("🚀 All-in-One Content Creator Hub")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Gemini API Key नहीं मिली! कृपया Streamlit Settings -> Secrets में GEMINI_API_KEY सेट करें।")
else:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"API Client बनाने में समस्या: {e}")

    st.sidebar.header("📌 Quick Navigation")
    menu = st.sidebar.radio("Go to:", ["Daily Checklist", "🤖 AI Content Ideas", "Free Design Tools"])

    if menu == "Daily Checklist":
        st.subheader("📋 Today's Creator Tasks")
        st.checkbox("Check Trending Hashtags")
        st.checkbox("Brainstorm 3 Content Ideas")
        st.checkbox("Design Post Graphic (Canva/Figma)")
        st.checkbox("Schedule & Publish Posts")
        st.checkbox("Analyze Yesterday's Engagement")
        if st.button("Save Daily Progress"):
            st.success("Progress Saved Successfully!")

    elif menu == "🤖 AI Content Ideas":
        st.subheader("🤖 AI Powered Content & Hashtag Generator")
        
        niche = st.text_input("अपना टॉपिक या नीश (Niche) लिखें:", placeholder="उदा: Tech, Fitness, Digital Marketing, Vlogging")
        content_type = st.selectbox("कंटेंट का प्रकार चुनें:", ["Instagram Reel / Short Script", "YouTube Video Ideas", "Viral Hashtags", "Post Captions"])
        
        if st.button("Generate Ideas 🚀"):
            if niche:
                with st.spinner("AI आपके लिए विचार जनरेट कर रहा है..."):
                    prompt = f"Give me 3 creative, high-engaging ideas for {content_type} on the topic '{niche}'. Include hooks, main content, and recommended hashtags."
                    
                    # 503 एरर से बचने के लिए बैकअप मॉडल्स की लिस्ट
                    models_to_try = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-2.0-flash"]
                    success = False

                    for model_name in models_to_try:
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt,
                            )
                            st.markdown("### 💡 AI Recommendations:")
                            st.write(response.text)
                            success = True
                            break # अगर सफलता मिल जाए तो लूप बंद करें
                        except Exception as e:
                            if "503" in str(e):
                                time.sleep(1) # 1 सेकंड रुककर अगला मॉडल ट्राई करें
                                continue
                            else:
                                st.error(f"त्रुटि ({model_name}): {e}")
                                break
                    
                    if not success:
                        st.warning("⚠️ Google के AI सर्वर पर इस समय बहुत अधिक ट्रैफिक है। कृपया कुछ सेकंड बाद फिर से प्रयास करें!")
            else:
                st.warning("कृपया पहले अपना टॉपिक या नीश लिखें!")

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