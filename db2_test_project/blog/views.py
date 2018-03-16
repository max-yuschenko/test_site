from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
# from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import MyUser, Post
from django.core.mail import EmailMessage
# Create your views here.


def home(request):
    # if request.user.is_active:
    #     return posts(request)
    return render(request, 'home.html')


def activation_check(user):
    return user.is_active


# @login_required
@user_passes_test(activation_check, login_url="/login/")
def posts(request):
    post_list = Post.objects.all()
    print(post_list)
    paginator = Paginator(post_list, 3)

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'posts.html', {'posts': posts})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your DB2 blog account.'
            message = render_to_string('activation_acc_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': user.pk,  # asd'#urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # message = f"""Hello, {user.email}!
            # Finish registration by click: http://{current_site.domain}{% url activate uidb64=uid token=token %}"""
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = uidb64  # force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return render(request, 'email_confirmation.html', {})
    else:
        return HttpResponse('Activation link is invalid!')
