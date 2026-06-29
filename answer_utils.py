import re


MAX_ANSWER_CHARS = 700

SKILL_PATTERNS = [
    "Python", "Java", "JavaScript", "TypeScript", "HTML", "CSS", "SQL",
    "React", "Next.js", "Node.js", "Express.js", "Django", "FastAPI",
    "Flask", "PostgreSQL", "MySQL", "MongoDB", "Redis", "ChromaDB",
    "OpenAI", "Gemini", "LangChain", "RAG", "Machine Learning", "AI",
    "Git", "GitHub", "Jenkins", "CI/CD", "Docker", "Kubernetes", "AWS",
    "Azure", "GCP", "REST API", "Microservices",
]

QUESTION_STOP_WORDS = {
    "a", "about", "all", "an", "and", "are", "ask", "be", "did", "do",
    "does", "for", "from", "give", "has", "have", "in", "is", "it", "me",
    "of", "on", "only", "please", "resume", "show", "tell", "the", "this",
    "to", "what", "which", "who", "with",
}


def _unique(items):
    seen = set()
    result = []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _extract_skills(context):
    matches = []
    for skill in SKILL_PATTERNS:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
        if re.search(pattern, context, flags=re.IGNORECASE):
            matches.append(skill)
    return _unique(matches)


def concise_fallback(question, context):
    """Return a short extractive answer without ever dumping the full context."""
    if re.search(r"\b(skill|skills|technology|technologies|tech stack)\b", question, re.I):
        skills = _extract_skills(context)
        return ", ".join(skills) if skills else "I do not know based on the provided document."

    keywords = {
        word.casefold()
        for word in re.findall(r"[A-Za-z0-9+#.-]{2,}", question)
        if word.casefold() not in QUESTION_STOP_WORDS
    }
    passages = [
        passage.strip(" \t\r\n-•")
        for passage in re.split(r"(?:\n+|(?<=[.!?])\s+|[•])", context)
        if passage.strip(" \t\r\n-•")
    ]
    ranked = sorted(
        passages,
        key=lambda passage: sum(
            keyword in passage.casefold() for keyword in keywords
        ),
        reverse=True,
    )
    relevant = [
        passage for passage in ranked
        if any(keyword in passage.casefold() for keyword in keywords)
    ]
    answer = " ".join(_unique(relevant[:2]))
    if not answer:
        return "I do not know based on the provided document."
    return answer[:MAX_ANSWER_CHARS].rstrip()


def limit_answer(answer):
    """Keep model output concise even if it ignores the prompt."""
    cleaned = (answer or "").strip()
    if not cleaned:
        return "I do not know based on the provided document."
    if len(cleaned) <= MAX_ANSWER_CHARS:
        return cleaned
    return cleaned[:MAX_ANSWER_CHARS].rsplit(" ", 1)[0].rstrip() + "..."
