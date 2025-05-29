from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def generate_summary(text: str, max_length=200, min_length=30) -> str:
    if len(text.strip()) == 0:
        return "No text to summarize."
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']
