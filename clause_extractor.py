import spacy

# Load English sentence tokenizer
nlp = spacy.load("en_core_web_sm")

def extract_clauses(text, min_length=30):
    """
    Extract meaningful clauses from raw text using spaCy sentence segmentation.
    
    Args:
        text (str): Raw input text
        min_length (int): Minimum length of clause to include (in characters)

    Returns:
        list[str]: Cleaned, filtered list of clauses
    """
    doc = nlp(text)
    clauses = []

    for sent in doc.sents:
        clause = sent.text.strip()

        # Filters
        if len(clause) < min_length:
            continue
        if clause.lower() in ["page", "terms", "date", "name"]:
            continue
        if clause.replace(" ", "").isdigit():
            continue

        clauses.append(clause)

    return clauses
