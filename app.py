import streamlit as st
import time
import requests
import io
import random
import os
from PIL import Image, ImageDraw
from google import genai

# Background video processing
try:
    from moviepy.editor import ImageClip, concatenate_videoclips
except Exception as e:
    pass

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
        "🎬 Fully Automated AI Video Studio",
        "📋 Daily Checklist", 
        "🤖 AI Content Ideas", 
        "Free Design Tools"
    ])

    if menu == "🎬 Fully Automated AI Video Studio":
        st.subheader("🎬 Instant AI Cartoon Video & Clickbait Thumbnail Generator")
        st.write("आपको कोई टॉपिक लिखने की ज़रूरत नहीं है! बस कैटेगरी चुनें और 1-क्लिक में ऑटोमैटिक AI वीडियो बनाएं।")

        selected_category = st.radio(
            "वीडियो की कैटेगरी चुनें (Choose Category):",
            ["👻 Horror Cartoon (डरावना कार्टून)", "😂 Funny Cartoon (फनी कार्टून)", "🧘 Motivational Cartoon (शांत/मोटिवेशनल)"],
            horizontal=True
        )

        # Pre-configured catchy clickbait titles with emojis according to category
        if "Horror" in selected_category:
            catchy_titles = [
                "गलती से भी रात में मत देखना! 💀😱",
                "हिम्मत है तो अकेले देखकर दिखाओ! 🎃👻",
                "इसे देखने के बाद नींद नहीं आएगी! 🧟‍♂️🤯",
                "WAIT FOR THE END! 😱🔥"
            ]
            default_prompt_theme = "spooky animated witch and creepy ghost scaring in dark night background vertical 9:16 reel"
        elif "Funny" in selected_category:
            catchy_titles = [
                "हँसी रोक कर दिखाओ! 😂🤣",
                "देखते-देखते हँसते-हँसते पागल हो जाओगे! 🤣💥",
                "इस वीडियो को देखने के बाद हँसी नहीं रुकेगी! 😂🙈",
                "100% FUNNY! DONT LAUGH CHALLENGE 🤣😜"
            ]
            default_prompt_theme = "funny animated playful cat chasing tiny mouse making hilarious face expressions 9:16 vertical reel"
        else:
            catchy_titles = [
                "गुस्सा आए तो शांत रहना सीखो 🧘✨",
                "यह बात आपकी जिंदगी बदल देगी 💡🌟",
                "NEVER GIVE UP ON YOUR DREAMS 🔥💪",
                "मन को शांत रखने का सबसे बड़ा रहस्य 🌸🕊️"
            ]
            default_prompt_theme = "wise cartoon monk meditating in peaceful bamboo forest soft lighting 9:16 vertical reel"

        selected_thumbnail_title = st.selectbox("थंबनेल के लिए आकर्षक टाइटल (Headline Text):", catchy_titles)

        if st.button("Generate Fully Automated Video 🎥"):
            random_seed = random.randint(10000, 999999)
            
            # Step 1: Generate AI Script Automatically
            with st.spinner("1. AI स्वयं स्टोरी और सीन्स तय कर रहा है..."):
                try:
                    script_prompt = f"Write a fast-paced, action-focused story description for {selected_category}. No dialogue/voiceover needed, only character expressions and emotions for an 18-20 second Short/Reel. Seed: {random_seed}"
                    script_response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=script_prompt
                    )
                    st.success("✅ AI स्टोरी स्क्रिप्ट तैयार!")
                    st.text_area("📄 Generated Story Outline:", script_response.text, height=120)
                except Exception as e:
                    st.error(f"स्क्रिप्ट जनरेशन में त्रुटि: {e}")
                    st.stop()

            # Step 2: Generate Thumbnail Image & Overlay Big Text
            with st.spinner("2. 3D कार्टून थंबनेल और बड़े अक्षरों वाला पोस्टर तैयार हो रहा है..."):
                try:
                    prompt_encoded = default_prompt_theme.replace(" ", "%20")
                    thumb_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=720&height=1280&nologo=true&seed={random_seed}"
                    
                    response = requests.get(thumb_url)
                    if response.status_code == 200:
                        base_img = Image.open(io.BytesIO(response.content))
                        
                        # Add Big Bold Clickbait Text Box
                        thumb_img = base_img.copy()
                        draw = ImageDraw.Draw(thumb_img)
                        draw.rectangle([(10, 40), (710, 240)], fill=(0, 0, 0, 210))
                        draw.text((25, 80), selected_thumbnail_title, fill="yellow")

                        # Save locally
                        thumb_path = "thumbnail_frame.png"
                        base_path = "main_frame.png"
                        output_mp4 = "final_output_reel.mp4"

                        thumb_img.save(thumb_path)
                        base_img.save(base_path)

                        st.image(thumb_img, caption="0.1s High Impact Clickbait Thumbnail", width=280)

                        # Step 3: Render MP4 Video File
                        with st.spinner("3. 0.1s थंबनेल युक्त MP4 वीडियो रेंडर की जा रही है..."):
                            try:
                                from moviepy.editor import ImageClip, concatenate_videoclips
                                thumb_clip = ImageClip(thumb_path).set_duration(0.1)
                                main_clip = ImageClip(base_path).set_duration(19.9)
                                
                                final_video = concatenate_videoclips([thumb_clip, main_clip], method="compose")
                                final_video.write_videofile(output_mp4, fps=24, codec="libx264")

                                with open(output_mp4, "rb") as f:
                                    video_data = f.read()

                                st.success("🎉 आपकी AI वीडियो और थंबनेल सफलतापूर्वक तैयार हो चुके हैं!")
                                st.video(video_data)

                                st.download_button(
                                    label="Download Complete MP4 Video 📥",
                                    data=video_data,
                                    file_name="ai_generated_reel.mp4",
                                    mime="video/mp4"
                                )
                            except Exception as video_err:
                                st.error(f"वीडियो कनवर्टर एरर: {video_err}")
                    else:
                        st.error("इमेज सर्वर रेस्पॉन्स नहीं दे रहा है।")
                except Exception as e:
                    st.error(f"प्रोसेसिंग में समस्या: {e}")

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
        niche = st.text_input("अपना टॉपिक या नीश (Niche) लिखें:", placeholder="उदा: Tech, Fitness, Vlogging")
        content_type = st.selectbox("कंटेंट का प्रकार चुनें:", ["Instagram Reel / Short Script", "YouTube Video Ideas", "Viral Hashtags", "Post Captions"])
        
        if st.button("Generate Ideas 🚀"):
            if niche:
                with st.spinner("AI आपके लिए विचार जनरेट कर रहा है..."):
                    prompt = f"Give me 3 creative ideas for {content_type} on topic '{niche}'."
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