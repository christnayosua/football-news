from django.urls import path
from main.views import show_main, create_news, show_news

# import fungsi show_xml dan show_json
from main.views import show_xml, show_json

# import fungsi show_xml_by_id dan show_json_by_id
from main.views import show_json_by_id, show_xml_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', create_news, name='create_news'),
    path('news/<str:id>/', show_news, name='show_news'),

    # Menambahkan path url untuk mengakses fungsi show_xml dan show_json
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),

    # Menambahkan path url untuk mengakses fungsi show_xml_by_id dan show_json_by_id
    path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),
]
