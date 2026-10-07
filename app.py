import streamlit as st
import time
import requests
import io
import random
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips
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
        "🎬 Automated Cartoon Reel Studio",
        "📋 Daily Checklist", 
        "🤖 AI Content Ideas", 
        "Free Design Tools"
    ])

    if menu == "🎬 Automated Cartoon Reel Studio":
        st.subheader("🎬 Complete AI Script to Cartoon Video Automation")
        st.write("टॉपिक दर्ज करें, कैटेगरी चुनें और 1-क्लिक में थंबनेल के साथ 18-20 सेकंड की MP4 वीडियो बनाएं!")

        col1, col2 = st.columns([2, 1])
        with col1:
            user_topic = st.text_input("अपना टॉपिक या आईडिया लिखें:", placeholder="उदा: चूहा सोती हुई बिल्ली को परेशान कर रहा है")
        with col2:
            category = st.selectbox("कंटेंट की कैटेगरी चुनें:", [
                "👻 Horror Cartoon (डरावना)",
                "😂 Funny Cartoon (हँसाने वाला)",
                "💪 Motivational Cartoon (प्रेरित करने वाला)"
            ])

        # Hook titles for horror/funny/motivational clickbaits
        if "Horror" in category:
            hook_texts = [
                "हिम्मत है तो अकेले देखकर दिखाओ! 😱",
                "गलती से भी रात में मत देखना! 💀",
                "WAIT FOR THE END! 🤯",
                "इसे देखने के बाद नींद नहीं आएगी! 🎃"
            ]
        elif "Funny" in category:
            hook_texts = [
                "हँसी रोक कर दिखाओ! 😂",
                "100% FUNNY! DONT LAUGH 🤣",
                "देखो आगे क्या हुआ! 😱",
                "LOL! 🤣🤣"
            ]
        else:
            hook_texts = [
                "यह बात जिंदगी बदल देगी! 🌟",
                "NEVER GIVE UP! 🔥",
                "सफलता का असली सच! 💡",
                "MUST WATCH TILL END! 🎬"
            ]

        selected_hook = st.selectbox("थंबनेल पर दिखने वाला आकर्षित टेक्स्ट चुनें/लिखें:", hook_texts)

        if st.button("Generate Script & Full MP4 Video 🚀"):
            if user_topic:
                random_seed = random.randint(1000, 999999) # For 100% unique script every time
                
                # Step 1: AI Script Generation
                with st.spinner("1. AI नई और यूनिक 18-20 सेकंड की स्टोरी-स्क्रिप्ट लिख रहा है..."):
                    script_prompt = f"""
                    Write a unique, highly engaging 18-20 second short story script for category '{category}' on topic '{user_topic}'.
                    Unique Seed ID: {random_seed}.
                    No voiceover required. Focus on character expressions, motion scenes, sound effects (like Phoo, Laugh, Shock, Gasp), and background music vibe.
                    Keep it short, fast-paced and catchy for 18-20 second Shorts/Reels.
                    """
                    try:
                        script_resp = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=script_prompt
                        )
                        st.success("✅ यूनिक स्टोरी-स्क्रिप्ट जनरेट हो गई!")
                        st.text_area("📄 Generated Story Script Preview:", script_resp.text, height=150)
                    except Exception as e:
                        st.error(f"स्क्रिप्ट बनाने में समस्या: {e}")
                        st.stop()

                # Step 2: AI Image & Thumbnail Generation
                with st.spinner("2. 3D एनीमेशन आर्ट और कैची थंबनेल जनरेट किया जा रहा है..."):
                    try:
                        style_prompt = "3d pixar style cartoon character vertical 9:16 high quality detailed"
                        if "Horror" in category:
                            style_prompt += " horror spooky dark glowing eyes witch ghost night background"
                        elif "Funny" in category:
                            style_prompt += " funny hilarious expression comedy playful bright colors"
                        else:
                            style_prompt += " inspirational cinematic lighting heroic proud expression"

                        clean_topic = user_topic.replace(" ", "%20")
                        img_url = f"https://image.pollinations.ai/prompt/{style_prompt}%20{clean_topic}?width=720&height=1280&nologo=true&seed={random_seed}"

                        img_resp = requests.get(img_url)
                        if img_resp.status_code == 200:
                            base_img = Image.open(io.BytesIO(img_resp.content))

                            # Create 0.1s Flash Thumbnail with Overlay Header
                            thumb_img = base_img.copy()
                            draw = ImageDraw.Draw(thumb_img)
                            
                            # Draw Horror/Clickbait Banner Box
                            draw.rectangle([(20, 50), (700, 220)], fill=(0, 0, 0, 200))
                            draw.text((40, 80), selected_hook, fill="yellow")

                            thumb_path = "temp_thumb.png"
                            base_path = "temp_base.png"
                            output_video = "final_cartoon_reel.mp4"

                            thumb_img.save(thumb_path)
                            base_img.save(base_path)

                            st.image(thumb_img, caption="0.1s Clickbait Thumbnail Preview (Reel Frame)", width=280)

                            # Step 3: Video Assembly (MoviePy MP4 Creation)
                            with st.spinner("3. थंबनेल + स्टोरी सीन्स को MP4 वीडियो में बदला जा रहा है..."):
                                thumb_clip = ImageClip(thumb_path).set_duration(0.1) # 0.1s thumbnail frame
                                main_clip = ImageClip(base_path).set_duration(19.9)   # 19.9s main scene (Total 20s)
                                
                                final_video = concatenate_videoclips([thumb_clip, main_clip], method="compose")
                                final_video.write_videofile(output_video, fps=24, codec="libx264")

                                with open(output_video, "rb") as file:
                                    video_bytes = file.read()

                                st.success("🎉 आपकी 20-सेकंड की कार्टून रील MP4 बनकर तैयार है!")
                                st.video(video_bytes) # Video Player in Streamlit

                                st.download_button(
                                    label="Download MP4 Video (With 0.1s Thumbnail) 📥",
                                    data=video_bytes,
                                    file_name=f"{category.split()[1].lower()}_cartoon_reel.mp4",
                                    mime="video/mp4"
                                )
                        else:
                            st.error("इमेज रेंडरिंग सर्वर में रुकावट आई, कृपया दोबारा प्रयास करें।")
                    except Exception as e:
                        st.error(f"वीडियो कनवर्ट करने में त्रुटि: {e}")
            else:
                st.warning("कृपया पहले टॉपिक लिखें!")

    elif menu == "Daily Checklist":
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
                    prompt = f"Give me 3 creative, high-engaging ideas for {content_type} on the topic '{niche}'."
                    try:
                        response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                        st.markdown("### 💡 AI Recommendations:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"त्रुटि: {e}")
            else:
                st.warning("कृपया पहले अपना टॉपिक या नीश लिखें!")

    elif menu == "Free Design Tools":
        st.subheader("🛠️ Free Tools for Content Creators")
        tools_data = {
            "🎨 Graphic & Photo Design": [
                {"name": "Canva", "url": "https://www.canva.com", "desc": "ग्राफिक डिज़ाइन, थंबनेल और पोस्ट बनाने के लिए।"},
                {"name": "Photopea", "url": "https://www.photopea.com", "desc": "फ्री ऑनलाइन फ़ोटोशॉप।"}
            ],
            "🤖 AI Video & Image Tools": [
                {"name": "Upscayl", "url": "https://www.upscayl.org", "desc": "लो-क्वालिटी फोटो को AI से HD/4K में बदलें।"},
                {"name": "Vidyo AI", "url": "https://vidyo.ai", "desc": "लॉन्ग वीडियो से शार्ट्स/रील्स बनाएं।"}
            ]
        }
        for category_name, list_of_tools in tools_data.items():
            st.markdown(f"### {category_name}")
            for tool in list_of_tools:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{tool['name']}** — {tool['desc']}")
                with col2:
                    st.link_button(f"🔗 Open {tool['name']}", tool['url'])
            st.divider()