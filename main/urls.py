from django.urls import path
from main.views import show_main, create_news, show_news

# import fungsi show_xml dan show_json
from main.views import show_xml, show_json

# import fungsi show_xml_by_id dan show_json_by_id
from main.views import show_json_by_id, show_xml_by_id

# import fungsi register
from main.views import register

# import fungsi login_user
from main.views import login_user

# import fungsi logout_user
from main.views import logout_user

# import fungsi edit_news
from main.views import edit_news

# import fungsi delete_news
from main.views import delete_news

# import fungsi add_news_entry_ajax
from main.views import add_news_entry_ajax

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

    # Penambahan path url untuk fungsi register pada bagian views.py
    path('register/', register, name='register'),

    # Penambahan path url untuk mengakses fungsi login_user()
    path('login/', login_user, name='login'),

    # Penambahan path url untuk mengakses fungsi logout_user
    path('logout/', logout_user, name='logout'),

    # Penambahan path url untuk mengakses fungsi edit_news
    path('news/<uuid:id>/edit', edit_news, name='edit_news'),

    # Penambahan path url untuk mengakses fungsi delete_news
    path('news/<uuid:id>/delete', delete_news, name='delete_news'),

    # Penambahan path url untuk mengakses fungsi add_news_entry_ajax
    path('create-news-ajax', add_news_entry_ajax, name='add_news_entry_ajax'),
]
