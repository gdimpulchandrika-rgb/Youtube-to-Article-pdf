import streamlit as st
import os
import zipfile
import time
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ------------------ Setup ------------------
st.set_page_config(page_title="YouTube → Website Generator", layout="wide")

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(
    model='gemini-flash-lite-latest',
    temperature=0.3
)

st.title("🎥 YouTube → Website Generator")
st.write("Convert YouTube videos into article-style websites")

# ------------------ LOAD TRANSCRIPT ONCE ------------------
@st.cache_data
def load_data(link: str):
    loader = YoutubeLoader.from_youtube_url(link)
    docs = loader.load()
    transcript = docs[0].page_content

    return {
        "transcript": transcript,
        "is_long": len(transcript) > 3000
    }

# ------------------ PROMPT ------------------
article_prompt = ChatPromptTemplate.from_template("""
You are a Professional Article Writer.

Convert the transcript into a structured article.

RULES:
- Ignore intro, ads, sponsors
- Focus on technical content
- Use headings, bullet points
- Add code snippets if needed
- End with summary

Transcript:
{transcript}
""")

# ------------------ SHORT SUMMARIZER ------------------
def short_summarizer(data):
    return (article_prompt | llm | StrOutputParser()).invoke({
        "transcript": data["transcript"]
    })

# ------------------ LONG SUMMARIZER ------------------
def get_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=8000,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def long_summarizer(data):
    text = data["transcript"]
    chunks = get_chunks(text)

    summaries = []

    for i, chunk in enumerate(chunks[:3]):  # LIMIT for speed
        st.write(f"🔹 Processing chunk {i+1}...")

        summary = (article_prompt | llm | StrOutputParser()).invoke({
            "transcript": chunk
        })

        summaries.append(summary)

    return "\n\n".join(summaries)

# ------------------ SMART ROUTER ------------------
smart_summarizer = RunnableLambda(load_data) | RunnableBranch(
    (lambda x: x["is_long"], RunnableLambda(long_summarizer)),
    RunnableLambda(short_summarizer)
)

# ------------------ WEB GENERATOR ------------------
web_prompt = ChatPromptTemplate.from_template("""
You are a Senior Frontend Developer.

Generate FULL webpage:

FORMAT:
--html--
<html code>
--html--

--css--
<style code>
--css--

--js--
<script code>
--js--

Content:
{article}
""")

web_chain = web_prompt | llm | StrOutputParser()

# ------------------ SAFE SPLIT ------------------
def extract(text, tag):
    parts = text.split(tag)
    return parts[1].strip() if len(parts) > 1 else ""

# ------------------ MAIN FUNCTION ------------------
def generate_website(article):
    response = web_chain.invoke({"article": article})

    html = extract(response, "--html--")
    css = extract(response, "--css--")
    js = extract(response, "--js--")

    return html, css, js

# ------------------ UI ------------------
url = st.text_input("Enter YouTube URL")

if st.button("Generate"):

    if not url:
        st.warning("Please enter a URL")
        st.stop()

    start_time = time.time()

    progress = st.empty()

    # STEP 1
    progress.text("📥 Loading transcript...")
    data = load_data(url)

    # STEP 2
    progress.text("🧠 Generating article...")
    article = smart_summarizer.invoke(url)

    # STEP 3
    progress.text("🎨 Generating website...")
    html, css, js = generate_website(article)

    if not html:
        st.error("❌ Website generation failed")
        st.stop()

    # STEP 4
    progress.text("📦 Saving files...")
    os.makedirs("output", exist_ok=True)

    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    with open("output/style.css", "w", encoding="utf-8") as f:
        f.write(css)

    with open("output/script.js", "w", encoding="utf-8") as f:
        f.write(js)

    zip_path = "output/website.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write("output/index.html", "index.html")
        zipf.write("output/style.css", "style.css")
        zipf.write("output/script.js", "script.js")

    end_time = time.time()

    st.success(f"✅ Done in {round(end_time - start_time, 2)} sec!")

    # DOWNLOAD
    with open(zip_path, "rb") as f:
        st.download_button("📥 Download Website", f, "website.zip")

    # PREVIEW
    st.subheader("🔍 Preview")
    st.components.v1.html(html, height=600, scrolling=True)