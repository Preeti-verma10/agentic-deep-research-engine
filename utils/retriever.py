import re


def chunk_text(text, chunk_size=1800):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []

    current = ""

    for sentence in sentences:

        if len(current) + len(sentence) < chunk_size:

            current += sentence + " "

        else:

            chunks.append(current.strip())

            current = sentence + " "

    if current:

        chunks.append(current.strip())

    return chunks


def retrieve_relevant_chunks(
    query,
    chunks,
    top_k=5
):

    query_words = set(
        re.findall(r"\w+", query.lower())
    )

    scored = []

    for chunk in chunks:

        chunk_lower = chunk.lower()

        words = set(
            re.findall(r"\w+", chunk_lower)
        )

        keyword_score = len(
            query_words.intersection(words)
        )

        phrase_bonus = 0

        if query.lower() in chunk_lower:
            phrase_bonus += 8

        if "definition" in query.lower() and "definition" in chunk_lower:
            phrase_bonus += 3

        if "history" in query.lower() and "history" in chunk_lower:
            phrase_bonus += 3

        if "application" in query.lower() and "application" in chunk_lower:
            phrase_bonus += 3

        if "future" in query.lower() and "future" in chunk_lower:
            phrase_bonus += 3

        if "advantage" in query.lower() and "advantage" in chunk_lower:
            phrase_bonus += 3

        if "limitation" in query.lower() and "limitation" in chunk_lower:
            phrase_bonus += 3

        score = keyword_score + phrase_bonus

        if score > 0:

            scored.append(

                (
                    score,
                    chunk
                )

            )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [

        chunk

        for score, chunk

        in scored[:top_k]

    ]


def extract_evidence(chunks):

    evidence = []

    seen = set()

    for chunk in chunks:

        sentences = re.split(

            r'(?<=[.!?])\s+',

            chunk

        )

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) < 60:
                continue

            if len(sentence) > 280:
                continue

            sentence = re.sub(

                r"\[\d+\]",

                "",

                sentence

            )

            sentence = re.sub(

                r"\s+",

                " ",

                sentence

            )

            lower = sentence.lower()

            if lower in seen:
                continue

            seen.add(lower)

            evidence.append({

                "evidence": sentence

            })

    return evidence[:12]