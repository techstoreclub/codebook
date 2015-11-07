from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404
from django.contrib.auth import views
from django.shortcuts import redirect
from django.template import loader, RequestContext
from topics.models import Topic
from topics.settings_context import settings_context


def create_account_view(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.data['username'], password=form.data['password1'])
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    template = loader.get_template('registration/create_account.html')
    context = RequestContext(request, {
        'topics': [Topic.get_tree_top(get_current_site(request))],
        'form': form
    })
    return HttpResponse(template.render(context))


def login_view(request):
    extra_context = {
        'topics': [Topic.get_tree_top(get_current_site(request))],
        'next': request.GET.get("next"),
        'fromlink': True if request.GET.get("fromlink") == 'true' else False
    }
    extra_context.update(settings_context(request))
    template_response = views.login(request, extra_context=extra_context)
    return template_response


def password_reset_view(request):
    extra_context = {
        'topics': [Topic.get_tree_top(get_current_site(request))],
    }
    template_response = views.password_reset(request, extra_context=extra_context)
    return template_response


def password_reset_confirm_view(request):
    extra_context = {
        'topics': [Topic.get_tree_top(get_current_site(request))],
    }
    template_response = views.password_reset(request, extra_context=extra_context)
    return template_response


def logout_view(request):
    if request.POST:
        next_link = "." if not request.POST.get("next") else request.POST.get("next")
        logout(request)
        return redirect(next_link)

    raise Http404("Logout must be called from the link on the website, not directly")
