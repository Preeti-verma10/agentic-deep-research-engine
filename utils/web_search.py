import requests


def search_sources(query):

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 10,
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

        sources = []

        if "query" not in data:
            return []

        for item in data["query"]["search"]:

            title = item["title"]

            title = title.replace(" ", "_")

            sources.append(
                f"https://en.wikipedia.org/wiki/{title}"
            )

        return sources

    except Exception as e:

        print("Search Error:", e)

        return []