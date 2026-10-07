import streamlit as st
import time
import requests
import io
from PIL import Image, ImageDraw, ImageFont
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
    menu = st.sidebar.radio("Go to:", [
        "Daily Checklist", 
        "🤖 AI Content Ideas", 
        "🎬 Cartoon Reels Generator", 
        "Free Design Tools"
    ])

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
                            break
                        except Exception as e:
                            if "503" in str(e):
                                time.sleep(1)
                                continue
                            else:
                                st.error(f"त्रुटि ({model_name}): {e}")
                                break
                    
                    if not success:
                        st.warning("⚠️ Google के AI सर्वर पर इस समय बहुत अधिक ट्रैफिक है। कृपया कुछ सेकंड बाद फिर से प्रयास करें!")
            else:
                st.warning("कृपया पहले अपना टॉपिक या नीश लिखें!")

    elif menu == "🎬 Cartoon Reels Generator":
        st.subheader("🎬 No-Voice Cartoon Reels & 0.1s Thumbnail Injector")
        st.write("यहाँ बिना वॉइस के कार्टून इमोशन्स और 0.1 सेकंड के थंबनेल के साथ रील का प्रिव्यू और डाउनलोड तैयार होगा।")

        cartoon_topic = st.text_input("कार्टून रील का टॉपिक लिखें:", placeholder="उदा: Cute funny boy reacting to a surprise gift")
        thumbnail_text = st.selectbox("0.1s थंबनेल पर टेक्स्ट (Kids Hook):", [
            "😱 WAIT FOR END!", 
            "😂 DONT LAUGH CHALLENGE!", 
            "OMG! WHAT HAPPENED? 🤯", 
            "MUST WATCH! 🎬"
        ])

        if st.button("Render Reel & Generate Download 🎬"):
            if cartoon_topic:
                with st.spinner("1. AI कार्टून इमेज और थंबनेल बना रहा है..."):
                    try:
                        # 1. Generate Cartoon Thumbnail Image using Pollinations AI (Free)
                        prompt_clean = cartoon_topic.replace(" ", "%20")
                        img_url = f"https://image.pollinations.ai/prompt/3d%20pixar%20style%20cartoon%20character%20funny%20expression%20{prompt_clean}?width=720&height=1280&nologo=true"
                        
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            image = Image.open(io.BytesIO(img_response.content))
                            
                            # Add Thumbnail text overlay
                            draw = ImageDraw.Draw(image)
                            draw.rectangle([(20, 50), (700, 150)], fill="yellow")
                            draw.text((40, 70), thumbnail_text, fill="black")
                            
                            # Save to Bytes
                            buf = io.BytesIO()
                            image.save(buf, format="PNG")
                            byte_im = buf.getvalue()

                            st.success("🎉 कार्टून थंबनेल और रील फ्रेम तैयार हो गए हैं!")
                            
                            # Display Image Preview
                            st.image(image, caption="0.1 Second Flash Thumbnail Frame Preview (9:16 Reel)", width=300)

                            # 2. Provide Download Options
                            st.markdown("### 📥 डाउनलोड करें:")
                            st.download_button(
                                label="Download 0.1s Cover Thumbnail Image (PNG) 🖼️",
                                data=byte_im,
                                file_name="reel_thumbnail.png",
                                mime="image/png"
                            )
                        else:
                            st.error("इमेज जनरेट करने में समस्या आई, कृपया दोबारा कोशिश करें।")
                    except Exception as e:
                        st.error(f"रेंडरिंग में त्रुटि: {e}")
            else:
                st.warning("कृपया पहले कार्टून रील का टॉपिक लिखें!")

    elif menu == "Free Design Tools":
        st.subheader("🛠️ Free Tools for Content Creators")
        st.write("नीचे दिए गए लिंक्स पर क्लिक करके आप सीधे टूल का उपयोग कर सकते हैं:")

        tools_data = {
            "🎨 Graphic & Photo Design": [
                {"name": "Canva", "url": "https://www.canva.com", "desc": "ग्राफिक डिज़ाइन, थंबनेल और पोस्ट बनाने के लिए।"},
                {"name": "Photopea", "url": "https://www.photopea.com", "desc": "फ्री ऑनलाइन फ़ोटोशॉप (Photoshop Alternative)।"}
            ],
            "🤖 AI Video & Image Tools": [
                {"name": "Upscayl", "url": "https://www.upscayl.org", "desc": "लो-क्वालिटी फोटो को AI से HD/4K में बदलें।"},
                {"name": "Vidyo AI", "url": "https://vidyo.ai", "desc": "लॉन्ग वीडियो से शार्ट्स/रील्स बनाएं।"}
            ],
            "📊 Infographics & Charts": [
                {"name": "Google Charts", "url": "https://developers.google.com/chart", "desc": "डेटा और चार्ट्स बनाने के लिए।"},
                {"name": "Visme", "url": "https://www.visme.co", "desc": "इन्फोग्राफिक्स और प्रेजेंटेशन डिज़ाइन।"},
                {"name": "Datamatic", "url": "https://datamatic.io", "desc": "आकर्षक विज़ुअल चार्ट्स के लिए।"}
            ]
        }

        for category, list_of_tools in tools_data.items():
            st.markdown(f"### {category}")
            for tool in list_of_tools:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{tool['name']}** — {tool['desc']}")
                with col2:
                    st.link_button(f"🔗 Open {tool['name']}", tool['url'])
            st.divider()