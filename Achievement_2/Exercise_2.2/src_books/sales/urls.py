from django.urls import path
from .views import home

# specify app name
app_name = 'sales'

# specify url path
urlpatterns = [
   path('', home),
]