from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import AssetMonitoring


@login_required
def view_list(request):
    user = request.user
    assets = AssetMonitoring.objects.filter(user=user)
    return render(request, 'interface/view_list.html', {'assets': assets})

@login_required
def update(request, id):
    return render("update")

@login_required
def register(request):
    return render("register")

