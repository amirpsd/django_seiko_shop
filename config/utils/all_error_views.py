from django.shortcuts import render



def handler404(request, exception):
    data = {}
    return render(request, 'main/404.html', data, status=404)


def handler403(request, exception):
    data = {}
    return render(request, 'main/404.html', data, status=403)


def handler500(request, exception):
    data = {}
    return render(request, 'main/404.html', data, status=500)


