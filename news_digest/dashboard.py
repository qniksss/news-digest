import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import re
import json

STOP_WORDS = {
    "в", "на", "с", "по", "из", "за", "к", "о", "у", "от", "до", "не",
    "и", "а", "но", "или", "что", "как", "это", "для", "при", "об",
    "во", "со", "без", "под", "над", "про", "через", "между",
    "он", "она", "они", "его", "её", "их", "им", "ему",
    "все", "всё", "уже", "еще", "ещё", "тоже", "также", "даже",
    "стало", "рассказал", "сообщил", "заявил", "назвал", "описаны",
    "известно", "стали", "могут", "будет", "было", "были", "может",
    "потом", "после", "двух", "новые", "время", "список"
}

def get_top_words(df, n=15):
    all_titles = " ".join(df["title"].dropna().tolist()).lower()
    words = re.findall(r"[а-яё]{4,}", all_titles)
    words = [w for w in words if w not in STOP_WORDS]
    return Counter(words).most_common(n)

def build_dashboard(df):
    top_words = get_top_words(df)
    words, counts = zip(*top_words)

    # График 1 — топ слов
    fig_words = px.bar(
        x=list(counts)[::-1],
        y=list(words)[::-1],
        orientation="h",
        title="Топ слов в заголовках",
        labels={"x": "Упоминаний", "y": ""},
        color=list(counts)[::-1],
        color_continuous_scale="Blues",
    )
    fig_words.update_layout(showlegend=False, coloraxis_showscale=False)

    # График 2 — по источникам
    source_counts = df["source"].value_counts()
    fig_sources = px.pie(
        values=source_counts.values,
        names=source_counts.index,
        title="Новостей по источникам",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )

    # Список новостей по источникам
    news_html = ""
    for source in df["source"].unique():
        news_html += f'<div class="source-block"><h3>{source}</h3><ul>'
        source_df = df[df["source"] == source].head(7)
        for _, row in source_df.iterrows():
            title = row["title"]
            link = row["link"]
            news_html += f'<li><a href="{link}" target="_blank">{title}</a></li>'
        news_html += "</ul></div>"

    # Собираем HTML
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Новостной дайджест</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #f5f7fa; color: #333; }}
        header {{ background: #1a1a2e; color: white; padding: 24px 40px; }}
        header h1 {{ font-size: 24px; font-weight: 600; }}
        header p {{ opacity: 0.6; margin-top: 4px; font-size: 14px; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 30px 20px; }}
        ..charts-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); min-height: 400px; }}
        .news-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .source-block h3 {{ font-size: 16px; margin-bottom: 12px; color: #1a1a2e; border-bottom: 2px solid #e8eaf0; padding-bottom: 8px; }}
        .source-block ul {{ list-style: none; }}
        .source-block li {{ padding: 7px 0; border-bottom: 1px solid #f0f0f0; font-size: 14px; line-height: 1.4; }}
        .source-block a {{ color: #333; text-decoration: none; }}
        .source-block a:hover {{ color: #4a90d9; }}
        h2 {{ font-size: 18px; margin-bottom: 20px; color: #1a1a2e; }}
    </style>
</head>
<body>
    <header>
        <h1>📰 Новостной дайджест</h1>
        <p>Автоматический анализ российских новостей</p>
    </header>
    <div class="container">
        <div class="charts-row">
            <div class="card" id="chart-words"></div>
            <div class="card" id="chart-sources"></div>
        </div>
        <h2>Последние новости по источникам</h2>
        <div class="news-grid card">
            {news_html}
        </div>
    </div>
    <script>
        var wordsData = {fig_words.to_json()};
        var sourcesData = {fig_sources.to_json()};
        Plotly.newPlot('chart-words', wordsData.data, wordsData.layout, {{responsive: true}});
        Plotly.newPlot('chart-sources', sourcesData.data, sourcesData.layout, {{responsive: true}});
    </script>
</body>
</html>"""

    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Готово! Открой файл dashboard.html в браузере")

if __name__ == "__main__":
    df = pd.read_csv("news.csv", encoding="utf-8-sig")
    build_dashboard(df)