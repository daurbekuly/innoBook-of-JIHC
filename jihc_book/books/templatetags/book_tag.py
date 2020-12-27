from django import template
from books.models import Category, Book

register = template.Library()



@register.simple_tag()
def get_categories():
    """Вывод всех категории"""
    return Category.objects.all()


@register.inclusion_tag('books/tags/last_book.html')
def get_last_books(count=5):
    books = Book.objects.order_by("id")[:count]
    return {"last_books": books}
