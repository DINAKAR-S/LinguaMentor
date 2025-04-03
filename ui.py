import streamlit as st
import requests

st.set_page_config(page_title="🧠 Language Tutor", layout="centered")
st.title("🧠 AI Language Learning Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "preferences_set" not in st.session_state:
    st.session_state.preferences_set = False
if "starter_shown" not in st.session_state:
    st.session_state.starter_shown = False

# Sidebar for setting preferences
with st.sidebar:
    st.header("🎯 Learning Preferences")
    known = st.selectbox("Your native language", ["English", "Tamil", "Hindi", "French"])
    target = st.selectbox("Language you want to learn", ["Tamil", "Hindi", "French"])
    level = st.selectbox("Your current level", ["Absolute Beginner", "Beginner", "Intermediate"])
    scene = st.selectbox("Choose a scenario", ["Café", "Restaurant", "Airport", "Hotel", "Shopping", "Casual Chat"])

    if st.button("✅ Set Preferences"):
        st.session_state.preferences_set = True
        st.session_state.chat_history = []
        st.session_state.starter_shown = False
        st.success("Preferences set! Let's start chatting.")

st.divider()

# Chat functionality
if st.session_state.preferences_set:
    if not st.session_state.starter_shown:
        intro = f"🎬 You're in a **{scene}** scenario. Let's begin learning **{target}**! What would you say first?"
        st.session_state.chat_history.append({"user": None, "bot": intro})
        st.session_state.starter_shown = True

    for chat in st.session_state.chat_history:
        if chat["user"]:
            st.markdown(f"**👤 You:** {chat['user']}")
        st.markdown(f"**🤖 AI:** {chat['bot']}")

    user_input = st.text_input("💬 Your message", key=f"input_{len(st.session_state.chat_history)}")

    if st.button("▶️ Send"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                turn_count = len([c for c in st.session_state.chat_history if c["user"]])
                awaiting = (turn_count % 4 == 1 and turn_count > 0)

                payload = {
                    "known_language": known,
                    "target_language": target,
                    "level": level,
                    "scene": scene,
                    "user_input": user_input,
                    "turns": turn_count,
                    "awaiting_conclusion": awaiting
                }

                res = requests.post("http://localhost:8000/chat", json=payload)
                if res.status_code == 200:
                    try:
                        data = res.json()
                        reply = data.get("response", "⚠️ AI did not return a valid message.")
                    except Exception as e:
                        reply = f"⚠️ Could not process AI reply: {e}"

                    st.session_state.chat_history.append({"user": user_input, "bot": reply})
                    st.rerun()
                else:
                    st.error("❌ Error communicating with backend.")
        else:
            st.warning("Type something first!")

else:
    st.info("ℹ️ Please set your learning preferences in the sidebar.")

st.divider()

# Show the feedback and new scene options after review
if st.button("📊 Show Mistake Review"):
    review = requests.get("http://localhost:8000/review").json()
    mistakes = review.get("summary", [])
    advice = review.get("review_advice", "")

    if mistakes:
        st.subheader("🧠 Your Mistakes & Feedback")
        for idx, (u, c, e) in enumerate(mistakes, 1):
            st.markdown(f"**{idx}.** ❌ `{u}` → ✅ `{c}`")
            st.markdown(f"🧠 {e}")
        st.subheader("📈 Learning Suggestions")
        st.markdown(advice)
    else:
        st.success("✅ No mistakes found. Excellent!")

    st.subheader("📝 Next Steps:")
    st.markdown("""
        If you need a new scene, change preferences in the sidebar and click 'Set Preferences'.
        Otherwise, if you'd like to continue with the same scene, type "continue" below and we can keep practicing with follow-up questions.
    """)
    continue_option = st.text_input("Type 'continue' to keep chatting in the current scene.")

    if continue_option.strip().lower() == "continue":
        st.session_state.chat_history = []  # Reset for continued conversation
        st.success("Let's continue! Type your next message in the scene you selected.")
        st.rerun()  # This will reset the conversation in the current scene

    else:
        st.info("Type 'continue' to keep going.")
