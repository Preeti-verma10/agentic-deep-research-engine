import requests


def search_sources(query):

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 8,
        "format": "json"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        data = response.json()

        if "query" not in data:
            return []

        sources = []

        skip_words = [
            "disambiguation",
            ".ai",
            "AI boom",
            "AI bubble",
            "AI slop",
            "Ai",
            "Outline of",
            "Index of"
        ]

        for item in data["query"]["search"]:

            title = item["title"]

            skip = False

            for word in skip_words:

                if word.lower() in title.lower():
                    skip = True
                    break

            if skip:
                continue

            title = title.replace(" ", "_")

            url = (
                "https://en.wikipedia.org/wiki/"
                + title
            )

            if url not in sources:
                sources.append(url)

        return sources

    except Exception as e:

        print("Search Error:", e)

        return []