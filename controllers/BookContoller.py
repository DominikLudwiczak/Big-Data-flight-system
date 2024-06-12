from fastapi.routing import APIRouter
from services.BookingService import BookingService
import uuid

router = APIRouter(prefix="/books", tags=["books"])

class BookController:
    def __init__(self):
        self.BookingService = BookingService()

    @router.get("/")
    def getAllBooks(self):
        return self.BookingService.getAllBooks()

    @router.get("/{bookId}")
    def getBook(self, bookId: uuid.UUID):
        return self.BookingService.getBook(bookId)

    @router.post("/")
    def addBook(self, title: str, author: str, year: int, pages: int):
        self.BookingService.addBook(title, author, year, pages)

    @router.delete("/{bookId}")
    def deleteBook(self, bookId: uuid.UUID):
        self.BookingService.deleteBook(bookId)