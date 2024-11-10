from typing import List, Dict


class Book:
    def __init__(self, title: str, author: str, isbn: str, price: float):
        self.title: str = title
        self.author: str = author
        self.isbn: str = isbn
        self.price:str = price
        self.is_available: bool = True


class Library:
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.borrowed_books: List[str] = []

    def add_book(self, book: Book) -> None:
            self.books[book.isbn] = book
            print(f"Added book: {book.title}")

    def borrow_book(self, isbn: str) -> bool:
        if isbn in self.books and self.books[isbn].is_available:
            self.books[isbn].is_available = False
            self.borrowed_books.append(isbn)
            return True
        return False

    def get_available_books(self) -> List[Book]:
        available_books = []
        for book in self.books.values():
            if book.is_available:
                available_books.append(book)
        return available_books

    def get_expensive_books(self, price_threshold: float) -> List[Book]:
        expensive_books = []
        for book in self.books.values():
            if book.price > price_threshold:
                expensive_books.append(book)
        return expensive_books

    def get_total_value(self) -> float:
        total = 0.0
        for book in self.books.values():
            total += book.price
        return total


def main():
    # Create library instance
    library = Library()

    # Create some books using different numeric types
    books = [
        Book("Python Basics", "John Smith", "123-456", 29.99),
        Book("Advanced Python", "Jane Doe", "456-789", 49.99),
        Book("Data Science", "Bob Wilson", "789-123", 39.99)
    ]

    # Add books to library
    print("Adding books to library:")
    for book in books:
        library.add_book(book)

    # Print total number of books
    print(f"\nTotal books in library: {len(library.books)}")

    # Print available books
    print("\nAvailable books:")
    available_books = library.get_available_books()
    for i in range(len(available_books)):
        book = available_books[i]
        print(f"{i + 1}. {book.title} by {book.author} - ${book.price:.2f}")

    # Borrow a book
    if library.borrow_book("123-456"):
        print("\nSuccessfully borrowed 'Python Basics'")

    # Print expensive books
    print("\nExpensive books (over $30):")
    expensive_books = library.get_expensive_books(30.00)
    for book in expensive_books:
        print(f"- {book.title}: ${book.price:.2f}")

    # Calculate total value
    total_value = library.get_total_value()
    print(f"\nTotal library value: ${total_value:.2f}")


if __name__ == "__main__":
    main()