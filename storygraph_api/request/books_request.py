import requests
from storygraph_api.exception_handler import request_exception

class BooksScraper:
    @staticmethod
    @request_exception
    def fetch_url(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content

    @staticmethod
    def main(book_id):
        url = f"https://app.thestorygraph.com/books/{book_id}"
        return BooksScraper.fetch_url(url)

    @staticmethod
    def community_reviews(book_id):
        url = f"https://app.thestorygraph.com/books/{book_id}/community_reviews"
        return BooksScraper.fetch_url(url)

    @staticmethod
    def content_warnings(book_id):
        url = f"https://app.thestorygraph.com/books/{book_id}/content_warnings"
        return BooksScraper.fetch_url(url)

    @staticmethod
    def search(query):
        formatted_query = query.replace(' ', '%20')
        url = f"https://app.thestorygraph.com/browse?search_term={formatted_query}"
        return BooksScraper.fetch_url(url)
