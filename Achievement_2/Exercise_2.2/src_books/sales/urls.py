from django.urls import path
from .views import home, records

# specify app name
app_name = 'sales'

# specify url path
urlpatterns = [
   path('', home, name='home'),
   path('records/', records, name='records')
]