import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from collections import Counter
import re

# Поддержка русского языка в графиках
matplotlib.rcParams["font.family"] = "DejaVu Sans"

STOP_WORDS = {
    "в", "на", "с", "по", "из", "за", "к", "о", "у", "от", "до", "не",
    "и", "а", "но", "или", "что", "как", "это", "для", "при", "об",
    "во", "со", "без", "под", "над", "про", "через", "между",
    "он", "она", "они", "его", "её", "их", "им", "ему",
    "все", "всё", "уже", "еще", "ещё", "тоже", "также", "даже",
    "стало", "рассказал", "сообщил", "заявил", "назвал", "описаны",
    "известно", "стали", "могут", "будет", "было", "были", "может"
}


def get_top_words(df, n=15):
    all_titles = " ".join(df["title"].dropna().tolist()).lower()
    words = re.findall(r"[а-яё]{4,}", all_titles)
    words = [w for w in words if w not in STOP_WORDS]
    return Counter(words).most_common(n)


def plot_top_words(top_words):
    words, counts = zip(*top_words)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(words[::-1], counts[::-1], color="steelblue")
    ax.bar_label(bars, padding=3)
    ax.set_title("Топ слов в новостных заголовках", fontsize=14, pad=15)
    ax.set_xlabel("Количество упоминаний")
    plt.tight_layout()
    plt.savefig("top_words.png", dpi=150)
    print("Сохранено: top_words.png")


def plot_wordcloud(df):
    all_titles = " ".join(df["title"].dropna().tolist()).lower()
    words = re.findall(r"[а-яё]{4,}", all_titles)
    words = [w for w in words if w not in STOP_WORDS]
    text = " ".join(words)

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        colormap="Blues",
        max_words=80,
    ).generate(text)

    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Облако слов — российские новости", fontsize=16, pad=15)
    plt.tight_layout()
    plt.savefig("wordcloud.png", dpi=150)
    print("Сохранено: wordcloud.png")


def plot_by_source(df):
    counts = df["source"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(counts, labels=counts.index, autopct="%1.0f%%",
           colors=["steelblue", "coral", "mediumseagreen", "gold"])
    ax.set_title("Распределение новостей по источникам", fontsize=13)
    plt.tight_layout()
    plt.savefig("by_source.png", dpi=150)
    print("Сохранено: by_source.png")


if __name__ == "__main__":
    df = pd.read_csv("news.csv", encoding="utf-8-sig")
    print(f"Загружено {len(df)} новостей\n")

    top_words = get_top_words(df)
    plot_top_words(top_words)
    plot_by_source(df)
    plot_wordcloud(df)

    print("\nГотово! Все графики сохранены в папку проекта.")