import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from PIL import Image

# ----------------- Page Config -----------------
st.set_page_config(page_title="Content Creator Hub", layout="wide")

st.title("🚀 All-in-One Content Creator & Social Media Hub")

# ----------------- Sidebar Navigation -----------------
option = st.sidebar.selectbox(
    "Choose a Module",
    [
        "Daily Get Up & Planner",
        "Hashtag Generator", 
        "Content Ideas", 
        "Analytics Dashboard", 
        "Stock Photos Search", 
        "Design Tools Directory"
    ]
)

# ----------------- 1. Daily Get Up & Planner -----------------
if option == "Daily Get Up & Planner":
    st.header("🌅 Morning Get Up & Content Routine")
    st.write("Start your day with a productive mindset and structured tasks.")
    
    wake_up_time = st.time_input("What time did you get up today?")
    st.success(f"You got up at {wake_up_time}. Let's make today count!")
    
    st.subheader("📋 Today's Creator Tasks")
    c1 = st.checkbox("Check Trending Hashtags")
    c2 = st.checkbox("Brainstorm 3 Content Ideas")
    c3 = st.checkbox("Design Post Graphic (Canva/Figma)")
    c4 = st.checkbox("Schedule & Publish Posts")
    c5 = st.checkbox("Analyze Yesterday's Engagement")
    
    if st.button("Save Daily Progress"):
        st.balloons()
        st.success("Great job starting your day!")

# ----------------- 2. Hashtag Generator -----------------
elif option == "Hashtag Generator":
    st.header("🏷️ Hashtag Generator")
    keyword = st.text_input("Enter your niche/topic (e.g., fitness, AI, travel):")
    if st.button("Generate Hashtags"):
        if keyword:
            base_tags = [
                f"#{keyword}", f"#{keyword}Life", f"#{keyword}Tips", 
                f"#Best{keyword.capitalize()}", f"#{keyword}Daily", 
                f"#{keyword}Community", f"#{keyword}Trends"
            ]
            st.success("Generated Hashtags:")
            st.code(" ".join(base_tags))
        else:
            st.warning("Please enter a keyword.")

# ----------------- 3. Content Ideas Generator -----------------
elif option == "Content Ideas":
    st.header("💡 Content Idea Generator")
    topic = st.text_input("Enter your main content topic:")
    if st.button("Get Ideas"):
        if topic:
            ideas = [
                f"Top 5 tools for {topic} in 2026",
                f"Common mistakes people make in {topic}",
                f"A step-by-step beginner guide to {topic}",
                f"Why {topic} is important for your growth",
                f"Future trends in {topic} you should know"
            ]
            st.subheader("Ideas for your next post/video:")
            for idx, idea in enumerate(ideas, 1):
                st.write(f"{idx}. {idea}")
        else:
            st.warning("Please enter a topic.")

# ----------------- 4. Analytics Dashboard -----------------
elif option == "Analytics Dashboard":
    st.header("📊 Social Media Analytics (Demo)")
    data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Reach': [1200, 1500, 1100, 1800, 2100, 2500, 2300],
        'Engagement': [300, 450, 250, 500, 600, 800, 750]
    })
    fig = px.line(data, x='Day', y=['Reach', 'Engagement'], title="Weekly Performance")
    st.plotly_chart(fig)

# ----------------- 5. Stock Photos Search -----------------
elif option == "Stock Photos Search":
    st.header("🖼️ Free Stock Media Finder")
    query = st.text_input("Search for images:")
    if st.button("Search Images"):
        if query:
            st.image(f"https://source.unsplash.com/600x400/?{query}", caption=f"Result for: {query}")
        else:
            st.warning("Enter a topic to search images.")

# ----------------- 6. Design Tools Directory -----------------
elif option == "Design Tools Directory":
    st.header("🛠️ Design & AI Tools Directory")
    tools = {
        "Design": ["Canva (canva.com)", "Photopea (photopea.com)", "Figma (figma.com)", "GIMP (gimp.org)"],
        "AI Tools": ["Upscayl (upscayl.org)", "Vidyo AI (vidyo.ai)", "TextBlaze (blaze.today)"],
        "Infographics": ["Google Charts", "Visme", "Datamatic"]
    }
    for category, list_of_tools in tools.items():
        st.subheader(category)
        for tool in list_of_tools:
            st.write(f"- {tool}")