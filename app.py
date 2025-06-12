import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
import openai
import re

st.set_page_config(page_title="YouTube Video Summarizer & Q&A", layout="centered")
st.title("📺 YouTube Video Summarizer & Q&A")

def extract_video_id(url):
    patterns = [
        r"youtu\.be/([^\?&]+)",
        r"youtube\.com/watch\?v=([^\?&]+)",
        r"youtube\.com/embed/([^\?&]+)",
        r"youtube\.com/v/([^\?&]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item['text'] for item in transcript])
    except NoTranscriptFound:
        st.error("No transcript found for this video.")
    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
    except VideoUnavailable:
        st.error("Video unavailable.")
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
    return None

def summarize_text(text, api_key):
    openai.api_key = api_key
    prompt = (
        "Summarize the following YouTube video transcript in a concise paragraph:\n\n"
        f"{text}\n\nSummary:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=250,
    )
    return response.choices[0].message.content.strip()

def answer_question(transcript, question, api_key):
    openai.api_key = api_key
    prompt = (
        f"Here is a transcript of a YouTube video:\n\n{transcript}\n\n"
        f"Question: {question}\nAnswer concisely:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()

with st.sidebar:
    st.header("🔑 API Key")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    st.markdown(
        "[Get your API key](https://platform.openai.com/account/api-keys) if you don't have one."
    )

url = st.text_input("Paste YouTube URL here:")

if url:
    video_id = extract_video_id(url)
    if not video_id:
        st.error("Invalid YouTube URL.")
    else:
        st.info("Fetching transcript...")
        transcript = get_transcript(video_id)
        if transcript:
            if api_key:
                if st.button("Summarize Video"):
                    with st.spinner("Summarizing..."):
                        summary = summarize_text(transcript, api_key)
                        st.subheader("Summary")
                        st.write(summary)
                        st.session_state['transcript'] = transcript
                if 'transcript' in st.session_state:
                    st.subheader("Ask a question about the video")
                    user_q = st.text_input("Your question")
                    if user_q and st.button("Get Answer"):
                        with st.spinner("Thinking..."):
                            answer = answer_question(st.session_state['transcript'], user_q, api_key)
                            st.write(f"**A:** {answer}")
            else:
                st.warning("Please enter your OpenAI API key in the sidebar to use summarization and Q&A features.")