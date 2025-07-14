from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .models import Profile
    
# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Muvaffaqqiyatli amalga oshirildi!")
                else:
                    return HttpResponse("sizning profilingiz faol holatda emas")
            else:
                return HttpResponse("Login yoki parolda xatolik bor")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    profil_info = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profil_info,
    }

    return render(request, 'pages/user_profile.html', context)



def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            # ❗ Xatolik bo'lsa, formani qayta render qilamiz
            return render(request, 'account/register.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


# class SignUpView(CreateView):
#       form_class = UserCreationForm
#       success_url = reverse_lazy('login')
#       template_name = 'account/register.html'

class SignUpView(View):

    def get(self, request):
          user_form = UserRegistrationForm()
          return render(request, 'account/register.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return render(request, 'account/register_done.html', {'new_user': new_user})

@login_required
def edt_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class EditUserView(LoginRequiredMixin,View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/profile_edit.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')









