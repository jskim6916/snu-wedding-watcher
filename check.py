import os, requests, re, bs4

URLS = [
 "https://snufacultyclub.com/page.php?pgid=wedding4&year=2026&month=4",
 "https://snufacultyclub.com/page.php?pgid=wedding4&year=2026&month=5"
]

def vacant(html_doc):
    soup = bs4.BeautifulSoup(html_doc, "html.parser")
    # Saturday row contains '토'; slot index 5 == 예식5부(18:30)
    for row in soup.select("table tr"):
        if '토' in row.get_text():
            cells = row.find_all('td')
            if len(cells) >= 6:
                return "예약완료" not in cells[5].get_text(strip=True)
    return False

openings = [u for u in URLS if vacant(requests.get(u, timeout=15).text)]
if openings:
    msg = f"🎉 빈 슬롯 발견! {', '.join(openings)}"
    requests.post(os.environ['SLACK_WEBHOOK'], json={"text": msg})
