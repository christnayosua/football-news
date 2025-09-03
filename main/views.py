from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2406495691',
        'name': 'Christna Yosua Rotinsulu',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)