from django.http import JsonResponse
from django.shortcuts import render


def health_check(request):
    return JsonResponse({"status": "ok"})


def error_400_view(request, exception):
    return render(request, "errors/400.html", status=400)


def error_401_view(request, exception=None):
    return render(request, "errors/401.html", status=401)


def error_403_view(request, exception):
    return render(request, "errors/403.html", status=403)


def error_404_view(request, exception):
    return render(request, "errors/404.html", status=404)


def error_408_view(request, exception=None):
    return render(request, "errors/408.html", status=408)


def error_500_view(request):
    return render(request, "errors/500.html", status=500)


def error_502_view(request, exception=None):
    return render(request, "errors/502.html", status=502)


def error_503_view(request, exception=None):
    return render(request, "errors/503.html", status=503)
