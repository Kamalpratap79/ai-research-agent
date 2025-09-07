from newspaper import Article

def extract_content(urls):
    extracted = []
    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            extracted.append({
                "title": article.title,
                "text": article.text[:2000],  # limit to first 2000 chars
                "url": url,
                "date": article.publish_date
            })
        except:
            continue
    return extracted
