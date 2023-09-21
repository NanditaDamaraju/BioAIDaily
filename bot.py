import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from dateutil.parser import parse
from dateutil.tz import tzlocal
import openai
import random
import streamlit as st

# Set your Google Custom Search API key and Custom Search Engine ID.
# You'd need to set up a Custom Search Engine to search google.com and modify it to focus on Google News.
API_KEY = 'AIzaSyAvJaffif8jhRSmzJWgminfn_Cugb0uZfY'
CSE_ID = '03b2050395b7640d1'

@st.cache_resource
def fetch_rss_articles(query_terms, days_old=2):
    """Fetches the latest articles from Google News RSS based on provided query terms."""
    # Here, we make the date_limit timezone-aware using tzlocal()
    date_limit = (datetime.now(tz=tzlocal()) - timedelta(days=days_old))

    rss_url = f"https://news.google.com/rss/search?q={query_terms}&hl=en-US&gl=US&ceid=US:en"
    response = requests.get(rss_url)

    if response.status_code != 200:
        print(f"Error fetching news from Google News RSS: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'xml')
    items = soup.find_all('item')

    # Filter articles based on the publication date
    recent_articles = []
    for item in items:
        pub_date_str = item.pubDate.text  # Extract the publication date
        pub_date = parse(pub_date_str)  # Convert the date string to a datetime object

        # Now both pub_date and date_limit are timezone-aware, and can be compared
        if pub_date >= date_limit:
            recent_articles.append({
                "title": item.title.text,
                "link": item.link.text
            })

    return recent_articles



def display_articles_with_checkboxes():
    st.title("News Summary")
    
    # Create a text input field for query terms with a default value
    query_terms = st.text_input("Enter query terms:", "biotech AND (machine learning or AI)")

    if query_terms:  # Fetch articles only if query_terms are provided
        articles = fetch_rss_articles(query_terms)

        # Dictionary to store checkbox states
        selected_articles = {}

        for article in articles:
            # Checkbox for each article
            selected = st.checkbox(article['title'], key=article['link'])

            if selected:
                # Add selected articles to the dictionary
                selected_articles[article['title']] = article['link']
        
        # If any article is selected, display its link
        if selected_articles:
            st.subheader("Selected Articles:")
            for title, link in selected_articles.items():
                st.write(f"[{title}]({link})")




def post_news_summary():
    # Define the search terms for articles
    query_terms = "(biotech OR gene OR diagnostic OR drug) AND (machine learning or AI)"
    
    articles = fetch_rss_articles(query_terms)

    for article in articles:
        # content = extract_article_content(article["link"])
        url = article["link"]
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        
        print(f"\n\n{article['title']}\nURL: {final_url}")

if __name__ == "__main__":
    display_articles_with_checkboxes()

