from django.shortcuts import render, redirect
from apps.authentication.models import Profile
from apps.authentication.decorators import no_login_required

# URL: /
# HTTP Method: GET
# Description: Main landing page
@no_login_required
def main(request):
    context = {'title': 'Home'}
    return render(request, 'main.html', context)

# URL: partials/features
# HTTP Method: GET
# Description: Features section of landing page
def features(request):
    context = {'title': 'Home'}
    return render(request, 'partials/features.html', context)

# URL: partials/showcase1
# HTTP Method: GET
# Description: Showcase section of landing page
def showcase1(request):
    context = {'title': 'Home'}
    return render(request, 'partials/showcase1.html', context)

# URL: partials/faqs
# HTTP Method: GET
# Description: FAQs section of landing page
def faqs(request):
    context = {'title': 'Home'}
    return render(request, 'partials/faqs.html', context)

# URL: /credits
# HTTP Method: GET
# Description: Credits page
def credits(request):
    context = {'title': 'Credits'}
    return render(request, 'credits.html', context)