# import requests


# def search_sources(query):

#     url = "https://en.wikipedia.org/w/api.php"

#     params = {
#         "action": "query",
#         "list": "search",
#         "srsearch": query,
#         "srlimit": 8,
#         "format": "json"
#     }

#     try:

#         response = requests.get(
#             url,
#             params=params,
#             headers={
#                 "User-Agent": "Mozilla/5.0"
#             },
#             timeout=10
#         )

#         data = response.json()

#         if "query" not in data:
#             return []

#         sources = []

#         skip_words = [
#             "disambiguation",
#             ".ai",
#             "AI boom",
#             "AI bubble",
#             "AI slop",
#             "Ai",
#             "Outline of",
#             "Index of"
#         ]

#         for item in data["query"]["search"]:

#             title = item["title"]

#             skip = False

#             for word in skip_words:

#                 if word.lower() in title.lower():
#                     skip = True
#                     break

#             if skip:
#                 continue

#             title = title.replace(" ", "_")

#             url = (
#                 "https://en.wikipedia.org/wiki/"
#                 + title
#             )

#             if url not in sources:
#                 sources.append(url)

#         return sources

#     except Exception as e:

#         print("Search Error:", e)

#         return []

from ddgs import DDGS


def search_sources(query):

    sources = []

    trusted_domains = [
        ".gov",
        ".edu",
        "wikipedia.org",
        "ibm.com",
        "microsoft.com",
        "aws.amazon.com",
        "cloud.google.com",
        "openai.com",
        "coursera.org",
        "geeksforgeeks.org",
        "towardsdatascience.com",
        "kaggle.com",
        "scikit-learn.org",
        "tensorflow.org",
        "pytorch.org"
    ]

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=12
            )

            trusted = []
            others = []

            for result in results:

                url = result.get("href", "")

                if not url.startswith("http"):
                    continue

                if ".pdf" in url.lower():
                    continue

                if url in trusted or url in others:
                    continue

                if any(domain in url for domain in trusted_domains):
                    trusted.append(url)
                else:
                    others.append(url)

            sources = trusted + others

    except Exception as e:

        print("Search Error:", e)

    return sources[:8]