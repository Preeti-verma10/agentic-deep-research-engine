import re


def chunk_text(text, chunk_size=1200):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    chunks = []

    current_chunk = ""

    for sentence in sentences:

        if (
            len(current_chunk)
            + len(sentence)
            < chunk_size
        ):

            current_chunk += sentence + " "

        else:

            chunks.append(
                current_chunk.strip()
            )

            current_chunk = (
                sentence + " "
            )

    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )

    return chunks


def retrieve_relevant_chunks(
    query,
    chunks,
    top_k=5
):

    query_words = set(
        re.findall(
            r"\w+",
            query.lower()
        )
    )

    scored_chunks = []

    for chunk in chunks:

        chunk_words = set(
            re.findall(
                r"\w+",
                chunk.lower()
            )
        )

        score = len(
            query_words.intersection(
                chunk_words
            )
        )

        if score > 0:

            score += len(chunk) / 1000

            scored_chunks.append(
                (score, chunk)
            )

    scored_chunks.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        chunk
        for score, chunk
        in scored_chunks[:top_k]
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

            if len(sentence) < 80:
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

            if sentence not in seen:

                seen.add(sentence)

                evidence.append(sentence)

    return evidence[:15]