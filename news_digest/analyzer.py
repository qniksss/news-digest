import pandas as pd
from collections import Counter
import re

# Слова которые не несут смысла — игнорируем
STOP_WORDS = {
    "в", "на", "с", "по", "из", "за", "к", "о", "у", "от", "до", "не",
    "и", "а", "но", "или", "что", "как", "это", "для", "при", "об",
    "во", "со", "без", "под", "над", "про", "через", "между",
    "он", "она", "они", "его", "её", "их", "им", "ему",
    "все", "всё", "уже", "еще", "ещё", "тоже", "также", "даже",
    "стало", "рассказал", "сообщил", "заявил", "назвал", "описаны",
    "известно", "стали", "могут", "будет", "было", "были", "может"
}


def load_news():
    df = pd.read_csv("news.csv", encoding="utf-8-sig")
    print(f"Загружено {len(df)} новостей")
    return df


def get_top_words(df, n=30):
    # Собираем все заголовки в одну строку
    all_titles = " ".join(df["title"].dropna().tolist()).lower()

    # Оставляем только русские слова длиннее 3 букв
    words = re.findall(r"[а-яё]{4,}", all_titles)

    # Фильтруем стоп-слова
    words = [w for w in words if w not in STOP_WORDS]

    # Считаем частоту
    counter = Counter(words)
    top = counter.most_common(n)

    print(f"\nТоп-{n} слов в заголовках:")
    for word, count in top:
        print(f"  {word}: {count}")

    return top


def get_news_by_source(df):
    print("\nНовостей по источникам:")
    print(df["source"].value_counts().to_string())


if __name__ == "__main__":
    df = load_news()
    get_news_by_source(df)
    top_words = get_top_words(df)