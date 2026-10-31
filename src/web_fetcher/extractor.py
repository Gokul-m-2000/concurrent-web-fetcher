from bs4 import BeautifulSoup


def extract_content(html : str) -> tuple[str | None , str]:
    soup=BeautifulSoup(html,"html.parser")
    if soup.title:
        title=soup.title.get_text(strip=True)
    else:
        title=None
    elements=soup.find_all(["script","style","nav","footer","header"])
    for element in elements:
        element.decompose()

    text=soup.get_text(separator=" ",strip=True)
    

    return title,text

