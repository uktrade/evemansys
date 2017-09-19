from django.shortcuts import redirect, render


def home(request):
    if hasattr(request.user, 'is_employee') and request.user.is_employee:
        return redirect('/b/')

    return render(request, 'pages/home.html')
