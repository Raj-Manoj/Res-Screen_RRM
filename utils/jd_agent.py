
def extract_text_from_pdf(path):
    return "We are looking for a Data Scientist with strong analytical skills to join our team."

def summarize_jd(text):
    return text[:100] + "..." if len(text) > 100 else text
