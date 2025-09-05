from django.urls import path
from .views import BookListView, BookDetailView  # import the class-based view


# specify app name
app_name = 'books'

# specify url path
urlpatterns = [
   path('list/', BookListView.as_view(), name='list'),
   path('list/<pk>', BookDetailView.as_view(), name='detail'),
]

