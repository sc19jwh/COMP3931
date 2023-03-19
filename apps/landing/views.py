from django.shortcuts import render
from apps.authentication.models import Profile

def test(request):
    context = {'title': 'Home', 'profile': Profile.objects.get(user=request.user)}
    return render(request, 'test.html', context)
