import streamlit as st
from utils import generate

st.set_page_config(page_title="LockBoostAI", layout="wide")

st.title("🔒 LockBoostAI — Content Idea Generator")
st.write("Ultra-light AI tool for creators, marketers & gamers.")

st.divider()

# Input Form
with st.form("input_form"):
    st.subheader("⚙️ Generation Settings")

    topic = st.text_input("Topic", placeholder="ex: Tekken combos, crypto basics, UX tips...", key="topic")

    col1, col2 = st.columns(2)

    with col1:
        platform = st.selectbox(
            "Platform",
            ["Instagram", "TikTok", "LinkedIn", "YouTube", "Twitter"],
            index=0
        )
    with col2:
        model = st.selectbox(
            "OpenAI Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            index=0
        )

    audience = st.text_input(
        "Target Audience",
        placeholder="ex: pro gamers, business owners, gen z creators..."
    )

    tone = st.text_input(
        "Tone",
        placeholder="ex: energetic, tactical, friendly, educational..."
    )

    submit = st.form_submit_button("🚀 Generate Content Ideas")

st.divider()

# Output
if submit:
    if not topic:
        st.error("Topic is required.")
    else:
        st.subheader("🧠 Generated Ideas")
        results = generate(topic, platform, audience, tone, model)

        for i, idea in enumerate(results, start=1):
            with st.container(border=True):
                st.markdown(f"### {i}. {idea['title']}")
                st.write(f"**Hook:** {idea['hook']}")
                st.write(f"**Caption:** {idea['caption']}")

                tags = " ".join(idea["hashtags"])
                st.write(f"**Hashtags:** {tags}")

                st.write(f"**Format:** {idea['format']}")