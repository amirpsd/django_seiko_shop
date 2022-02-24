from django.shortcuts import render


def handler403(request, exception):
    data = {}
    return render(request, "main/error/403.html", data, status=403)


def handler404(request, exception):
    data = {}
    return render(request, "main/error/404.html", data, status=404)
