# Penambahan import modul untuk meretriksi akses halaman main dan news detail
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News

# Tambahan import untuk mengembalikan data dalam bentuk XML
from django.http import HttpResponse
from django.core import serializers

# Penambahan impor modul untuk form registrasi, login, dan logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Penambahan import modul untuk menggunakan data dari cookies
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# Import tambahan untuk menampilkan data di halaman utama dengan AJAX
from django.http import HttpResponseRedirect, JsonResponse

# Import tambahan untuk menangani request AJAX
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Melindungi serangan XSS
from django.utils.html import strip_tags

# Penambahan fungsi yang menangani request AJAX
@csrf_exempt
@require_POST
def add_news_entry_ajax(request):
    # Melindungi aplikasi web dari serangan XSS
    title = strip_tags(request.POST.get("title")) # strip HTML tags!
    content = strip_tags(request.POST.get("content")) # strip HTML tags!

    title = request.POST.get("title")
    content = request.POST.get("content")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    new_news = News(
        title=title, 
        content=content,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_news.save()

    return HttpResponse(b"CREATED", status=201)

# Penambahan fungsi untuk delete_news
def delete_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

# Penambahan fungsi untuk mengedit news
def edit_news(request, id):
    news = get_object_or_404(News, pk=id)
    form = NewsForm(request.POST or None, instance=news)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_news.html", context)

# Penambahan fungsi untuk mekanisme logout
def logout_user(request):
    # Konfigurasi untuk menghapus cookie last_login setelah logout
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# Penambahan fungsi login untuk mengautentikasi pengguna yang ingin login 
def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      # Konfigurasi untuk menyimpan cookie baru, last_login, yang berisi timestamp terakhir kali user melakukan login 
      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

# Penambahan function register untuk menghasilkan formulir registrasi secara otomatis
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

# Fungsi untuk mengembalikan data berdasarkan ID dalam bentuk XML
def show_xml_by_id(request, news_id):
    # Menambahkan block try_except untuk menangani apabila news_id tidak ditemukan dalam database
   try:
       news_item = News.objects.filter(pk=news_id)
       xml_data = serializers.serialize("xml", news_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except News.DoesNotExist:
       return HttpResponse(status=404)

# Fungsi untuk mengembalikan data berdasarkan ID dalam bentuk JSON
def show_json_by_id(request, news_id):
    try:
        # Mengubah objek NEWS menjadi dictionary -> based by id
        news = News.objects.select_related('user').get(pk=news_id)
        data = {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
            'user_username': news.user.username if news.user_id else None,
        }
        # Mengembalikan data 
        return JsonResponse(data)
    except News.DoesNotExist:
        # Handle jika data tidak ditemukan 
        return JsonResponse({'detail': 'Not found'}, status=404)
    
# Fungsi baru untuk mengembalikan data dalam bentuk XML
def show_xml(request):
     news_list = News.objects.all()
     xml_data = serializers.serialize("xml", news_list)
     return HttpResponse(xml_data, content_type="application/xml")

# Fungsi baru untuk mengembalikan data dalam bentuk JSON
def show_json(request):
    # Konfigurasi untuk mengubah objek NEWS menjadi dictionary
    news_list = News.objects.all()
    data = [
        {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
        }
        for news in news_list
    ]

    # Mengirimkan data dalam format JSON ke client
    # Mengembalikan dalam bentuk list 
    return JsonResponse(data, safe=False)

# Penambahan konfigurasi untuk mengimplementasikan decorator yang baru saja diimport
@login_required(login_url='/login')
def show_main(request):
    # Penambahan konfigurasi untuk melakukan filter news yang telah dibuat sebelumnya
    # hal tersebut akan menampilkan halaman utama setelah user login
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        news_list = News.objects.all()
    else:
        news_list = News.objects.filter(user=request.user)

    context = {
        'npm' : '2406495691',
        'name': 'Christna Yosua Rotinsulu',
        'class': 'PBP A',
        'news_list': news_list,
        # Penambahan attribute last_login untuk menunjukkan timestamp terakhir user melakukan login
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        # Penambahan konfigurasi agar Django tidak langsung menyimpan objek hasil form ke database
        news_entry = form.save(commit = False)
        news_entry.user = request.user
        news_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_news.html", context)

# Penambahan decorator
@login_required(login_url='/login')
def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, "news_detail.html", context)