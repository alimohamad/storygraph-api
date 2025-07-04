from datetime import datetime
from enum import Enum
import re
from storygraph_api.request.user_request import UserScraper
from storygraph_api.exception_handler import parsing_exception
from bs4 import BeautifulSoup

class Endpoints(Enum):
    CurrentlyReading = 'currently_reading'
    ToRead = 'to_read'
    BooksRead = 'books_read'
class UserParser:
    @staticmethod
    @parsing_exception 
    def parse_html(html, endpoint):
        soup = BeautifulSoup(html, 'html.parser')
        books_list = []
        books = soup.find_all('div', class_="book-title-author-and-series")
        for book in books:
            book_data = {
                "title": book.find('a').text.strip(),
                "book_id": book.find('a')['href'].split('/')[-1]
            }

            if endpoint == Endpoints.BooksRead:
                date_finished_string = soup.find(string=re.compile("Finished"))
                if date_finished_string:
                    date = datetime.strptime(str(date_finished_string), 'Finished %b %d, %Y\n').date().isoformat()
                    book_data['date_finished'] = date


            books_list.append(book_data)
        data = list({(book['title'], book['book_id'], book['date_finished']): book for book in books_list}.values())
        return data

    @staticmethod
    def currently_reading(uname, cookie):
        content = UserScraper.currently_reading(uname,cookie)
        return UserParser.parse_html(content, Endpoints.CurrentlyReading)

    @staticmethod
    def to_read(uname, cookie):
        content = UserScraper.to_read(uname,cookie)
        return UserParser.parse_html(content, Endpoints.ToRead)

    @staticmethod
    def books_read(uname, cookie):
        content = UserScraper.books_read(uname,cookie)
        return UserParser.parse_html(content, Endpoints.BooksRead)
