import requests
from bs4 import BeautifulSoup


def fetch_document(url):
    """
    Downloads webpage HTML.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        return response.text

    except Exception as e:
        print(f"Fetch Error: {e}")
        return None


def parse_document(html):

    try:
        soup = BeautifulSoup(html, "html.parser")

        paragraphs = soup.find_all("p")

        print("Paragraphs found:", len(paragraphs))

        content = []

        for p in paragraphs:

            text = p.get_text(strip=True)

            if len(text) > 50:
                content.append(text)

        return "\n".join(content)

    except Exception as e:
        print(f"Parse Error: {e}")
        return ""