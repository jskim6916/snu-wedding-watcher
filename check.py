import os, requests, bs4

URLS = [
    "https://snufacultyclub.com/page.php?pgid=wedding4&year=2026&month=4",
    "https://snufacultyclub.com/page.php?pgid=wedding4&year=2026&month=5",
]

def has_vacancy(html_doc: str) -> bool:
    soup = bs4.BeautifulSoup(html_doc, "html.parser")
    # Look at every Saturday row; column 5 is 예식5부(18:30)
    for row in soup.select("table tr"):
        if "토" in row.get_text():
            cells = row.find_all("td")
            if len(cells) >= 6 and "예약완료" not in cells[5].get_text(strip=True):
                return True
    return False

openings = [url for url in URLS if has_vacancy(requests.get(url, timeout=15).text)]

if openings:
    webhook = os.environ.get("SLACK_WEBHOOK")
    if webhook:
        msg = f"🎉 빈 슬롯 발견! {', '.join(openings)}"
        requests.post(webhook, json={"text": msg}, timeout=15).raise_for_status()
