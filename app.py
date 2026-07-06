from process_incoming import ask_question
import streamlit as st
import process_incoming

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Teaching Assistant")
st.markdown("Ask questions about your course videos.")

# Sidebar
st.sidebar.header("Search Filters")
course = st.sidebar.selectbox(
    "Course",
    ["Big Data Analysis and Python for Data Science"]
)
video = st.sidebar.selectbox(
    "Video",
    ["All Videos"]
)
st.write("---")
videos = sorted(process_incoming.df["title"].unique())

selected_video = st.selectbox(
    "Choose Video (Optional)",
    ["All Videos"] + videos
)
question = st.text_input(
    "Ask your question"
)

if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:
        with st.spinner("Searching course content..."):

            result = ask_question(
                        question,
                        selected_video,
                        st.session_state.chat_history
                    )
            
            if result:

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": result["answer"]
                    }
                )

            st.success("Answer")

            st.markdown("## 💬 Answer")
            st.info(result["answer"])

            if st.button("🗑️ Clear Conversation"):

                    st.session_state.chat_history = []
                    st.rerun()