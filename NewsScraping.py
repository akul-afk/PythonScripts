import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from textblob import TextBlob
import csv
import spacy
import matplotlib.pyplot as plt

try:
    import en_core_web_sm
except ImportError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

import en_core_web_sm
nlp = en_core_web_sm.load()

site_configs = [
    {
        "url": "https://www.bbc.com/mundo",
        "tag": "h3",
        "class": "bbc-pam0zn e47bds20",
        "src_language": "es"
    },
    {
        "url": "https://www.bbc.com/hindi",
        "tag": "h3",
        "class": "bbc-1kr00f0 e47bds20",
        "src_language": "hi"
    },
    {
        "url": "https://www.bbc.com/punjabi",
        "tag": "h3",
        "class": "bbc-1hwukd e47bds20",
        "src_language": "pa"
    },
    {
        "url": "https://www.bbc.com/portuguese",
        "tag": "h3",
        "class": "bbc-pam0zn e47bds20",
        "src_language": "pt"
    },
    {
        "url": "https://www.bbc.com/japanese",
        "tag": "h3",
        "class": "bbc-7k6nqm e47bds20",
        "src_language": "ja"
    },
    {
        "url": "https://www.bbc.com/russian",
        "tag": "h3",
        "class": "bbc-pam0zn e47bds20",
        "src_language": "ru"
    }
]

def fetch_headlines(url, headline_tag, headline_class=None):
    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')
        if headline_class:
            headlines = soup.find_all(headline_tag, class_=headline_class)
        else:
            headlines = soup.find_all(headline_tag)
        return [headline.get_text(strip=True) for headline in headlines[:5]]
    except Exception as e:
        print(f"Error fetching headlines from {url}: {e}")
        return []

def translate_headlines(headlines, src_language):
    translator = GoogleTranslator(source=src_language, target='en')
    translated_headlines = []
    for headline in headlines:
        try:
            translated_headlines.append(translator.translate(headline))
        except Exception as e:
            print(f"Error translating headline: {headline}. Error: {e}")
            translated_headlines.append(headline)  # Fallback to original if translation fails
    return translated_headlines

def analyze_sentiment(headline):
    analysis = TextBlob(headline)
    return analysis.sentiment.polarity

def perform_ner(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

csv_filename = "translated_headlines_with_sentiment_and_ner.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Source', 'Original Headline', 'Translated Headline', 'Polarity', 'Entities']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for config in site_configs:
        headlines = fetch_headlines(config['url'], config['tag'], config['class'])
        translated_headlines = translate_headlines(headlines, config['src_language'])

        print(f"\nTop 5 headlines from {config['url']} (original):")
        for idx, headline in enumerate(headlines, 1):
            print(f"{idx}. {headline}")

        print(f"\nTop 5 headlines from {config['url']} (translated to English):")
        for idx, headline in enumerate(translated_headlines, 1):
            print(f"{idx}. {headline}")

        for original, translated in zip(headlines, translated_headlines):
            polarity = analyze_sentiment(translated)
            entities = perform_ner(translated)
            writer.writerow({
                'Source': config['url'],
                'Original Headline': original,
                'Translated Headline': translated,
                'Polarity': polarity,
                'Entities': entities
            })

print(f"\nTranslated headlines with sentiment analysis and NER have been saved to {csv_filename}")
