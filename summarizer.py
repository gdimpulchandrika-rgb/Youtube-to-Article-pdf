print("🚀 OPTIMIZED FAST CODE RUNNING")

import os
from dotenv import load_dotenv
import zipfile

from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableBranch
from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import RecursiveCharacterTextSplitter

# -------------------- ENV --------------------
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

# -------------------- MODEL --------------------
llm = ChatGoogleGenerativeAI(model='gemini-flash-lite-latest')

# -------------------- LOAD TRANSCRIPT (ONLY ONCE) --------------------
def load_transcript(link: str):
    loader = YoutubeLoader.from_youtube_url(link)
    docs = loader.load()
    transcript = docs[0].page_content
    return {
        "transcript": transcript,
        "is_long": len(transcript) > 3000  # better threshold
    }

# -------------------- PROMPT --------------------
article_prompt = ChatPromptTemplate.from_template("""
You are an Professional Article Writer.

Convert the following transcript into a **professional article**:

**RULES**:
- Ignore intro, ads, subscribe messages
- Focus only on technical content
- Use first-person tone
- Use headings, bullet points
- Add code snippets if needed
- End with short summary

Transcript:
{transcript}
""")

# -------------------- SHORT SUMMARIZER --------------------
def short_summarizer(data):
    return (article_prompt | llm | StrOutputParser()).invoke({
        "transcript": data["transcript"]
    })

# -------------------- LONG SUMMARIZER (FAST VERSION) --------------------
def long_summarizer(data):
    text = data["transcript"]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=8000,   # BIG chunks → fewer API calls
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    summaries = []

    for chunk in chunks[:3]:   # LIMIT chunks (speed boost)
        summary = (article_prompt | llm | StrOutputParser()).invoke({
            "transcript": chunk
        })
        summaries.append(summary)

    final_summary = "\n\n".join(summaries)

    return final_summary

# -------------------- SMART ROUTER --------------------
smart_summarizer = RunnableLambda(load_transcript) | RunnableBranch(
    (lambda x: x["is_long"], RunnableLambda(long_summarizer)),
    RunnableLambda(short_summarizer)
)

# -------------------- WEBPAGE GENERATOR --------------------
web_prompt = ChatPromptTemplate.from_template("""
You are a Senior Frontend Developer.

Generate FULL website code.

FORMAT STRICTLY:

--html--
<html code>
--html--

--css--
<style code>
--css--

--js--
<script code>
--js--

CONTENT:
{article}
""")

web_chain = web_prompt | llm | StrOutputParser()

# -------------------- FINAL PIPELINE --------------------
final_chain = smart_summarizer | RunnableLambda(lambda x: {"article": x}) | web_chain

# -------------------- RUN --------------------
url = "https://www.youtube.com/watch?v=xPh5ihBWang"

result = final_chain.invoke(url)

# -------------------- SAFE EXTRACT --------------------
def extract_section(text, tag):
    parts = text.split(tag)
    return parts[1].strip() if len(parts) > 1 else ""

html = extract_section(result, "--html--")
css = extract_section(result, "--css--")
js = extract_section(result, "--js--")

# -------------------- SAVE FILES --------------------
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("style.css", "w", encoding="utf-8") as f:
    f.write(css)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(js)

# -------------------- ZIP --------------------
with zipfile.ZipFile("website.zip", "w") as zipf:
    zipf.write("index.html")
    zipf.write("style.css")
    zipf.write("script.js")

print("✅ Done! Website generated and zipped.")