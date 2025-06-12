# YouTube Video Summarizer & Q&A (Streamlit App)

A web app that:
- Accepts a YouTube URL
- Fetches the video's transcript
- Summarizes the content using OpenAI GPT
- Lets you ask questions about the video

## Setup

1. **Clone this repo** (or copy the files into a folder)

2. **Install requirements**

```bash
pip install -r requirements.txt
```

3. **Run the app**

```bash
streamlit run app.py
```

4. **Add your OpenAI API Key**

- Enter it in the sidebar when prompted.
- Get a key here: https://platform.openai.com/account/api-keys

## Deployment

- **Streamlit Cloud:** Push this repo to GitHub and [deploy on Streamlit Cloud](https://streamlit.io/cloud).
- **Hugging Face Spaces:** Use a Streamlit space, point to this repo.
- **Locally:** As above.

## Notes

- Only works with videos that have transcripts (auto or manual captions).
- For longer videos, summarization/Q&A may be less accurate (token limit).
- Swap in HuggingFace models if you wish—let us know if you need help!