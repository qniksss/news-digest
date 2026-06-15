import feedparser
import pandas as pd
import ssl

# Отключаем проверку SSL-сертификатов (решение для Mac)
ssl._create_default_https_context = ssl._create_unverified_context

RSS_FEEDS = {
    "Лента.ру": "https://lenta.ru/rss/news",
    "Коммерсантъ": "https://www.kommersant.ru/RSS/news.xml",
    "Meduza": "https://meduza.io/rss/all",
    "Российская газета": "https://rg.ru/xml/index.xml",
}

def fetch_news():
    all_news = []

    for source, url in RSS_FEEDS.items():
        print(f"Загружаю: {source}...")
        feed = feedparser.parse(url)
        print(f"  → получено записей: {len(feed.entries)}")

        for entry in feed.entries[:20]:
            all_news.append({
                "source": source,
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "published": entry.get("published", ""),
                "link": entry.get("link", ""),
            })

    df = pd.DataFrame(all_news)
    if not df.empty:
        df.to_csv("news.csv", index=False, encoding="utf-8-sig")
        print(f"\nГотово! Собрано {len(df)} новостей → сохранено в news.csv")
    else:
        print("\nНовостей не получено.")
    return df

if __name__ == "__main__":
    df = fetch_news()
    if not df.empty:
        print(df[["source", "title"]].head(10))