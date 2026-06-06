import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.howstat.com"

MATCH_LIST_URL = (
    "https://www.howstat.com/cricket/Statistics/Matches/MatchList.asp"
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/webp,*/*;q=0.8"
    ),
    "Connection": "keep-alive",
}


scraper = cloudscraper.create_scraper()

scraper.headers.update(headers)


def get_match_links():
    response = scraper.get(MATCH_LIST_URL)

    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "MatchScorecard.asp" in href:
            if href.startswith("../"):
                href = href.replace("../", "")

            full_link = BASE_URL + "/" + href.lstrip("/")
            links.append(full_link)

    # Remove duplicates and keep last 10
    links = list(dict.fromkeys(links))[:10]

    print(f"Found {len(links)} match links")

    return links


def scrape_match(url):
    response = scraper.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    data = {
        "match": "N/A",
        "date": "N/A",
        "venue": "N/A",
        "result": "N/A",
        "top_scorer": "N/A"
    }

    try:
        # Match title
        title_tag = soup.find("td", {"class": "ScorecardHeader"})

        if title_tag:
            data["match"] = title_tag.text.strip()

        text = soup.get_text(" ", strip=True)

        # Date
        if "Date:" in text:
            data["date"] = (
                text.split("Date:")[1]
                .split("Venue:")[0]
                .strip()
            )

        # Venue
        if "Venue:" in text:
            data["venue"] = (
                text.split("Venue:")[1]
                .split("Toss:")[0]
                .strip()
            )

        # Result
        if "won" in text:
            result_text = text.split("won")[0]
            data["result"] = (
                result_text.split(".")[-1].strip()
                + " won"
            )

        # Top scorer logic
        tables = soup.find_all("table")

        best_score = 0
        best_player = "N/A"

        for table in tables:
            rows = table.find_all("tr")

            for row in rows:
                cols = row.find_all("td")

                if len(cols) >= 3:
                    try:
                        player_name = cols[0].text.strip()
                        runs = int(cols[2].text.strip())

                        if runs > best_score:
                            best_score = runs
                            best_player = player_name

                    except:
                        continue

        if best_score > 0:
            data["top_scorer"] = (
                f"{best_player} - {best_score}"
            )

    except Exception as e:
        print("Error scraping:", url)
        print(e)

    return data


def main():
    print("Starting scraper...")

    links = get_match_links()

    all_data = []

    for i, link in enumerate(links):
        print(f"Scraping {i + 1}/{len(links)}")

        match_data = scrape_match(link)
        all_data.append(match_data)

        time.sleep(2)

    df = pd.DataFrame(all_data)

    df.to_csv("match_data.csv", index=False)

    print("✅ Data saved to match_data.csv")


if __name__ == "__main__":
    main()