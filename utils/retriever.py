import re


def chunk_text(text, chunk_size=1000):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    chunks = []

    current_chunk = ""

    for sentence in sentences:

        if (
            len(current_chunk) +
            len(sentence)
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

            scored_chunks.append(
                (score, chunk)
            )

    scored_chunks.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        chunk
        for score, chunk
        in scored_chunks[:top_k]
    ]


def extract_evidence(chunks):

    evidence = []

    for chunk in chunks:

        sentences = re.split(
            r'(?<=[.!?])\s+',
            chunk
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) < 60:
                continue

            sentence = re.sub(
                r"\[\d+\]",
                "",
                sentence
            )

            evidence.append(
                sentence
            )

    unique = []

    for item in evidence:

        if item not in unique:

            unique.append(item)

    return unique[:10]