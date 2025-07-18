from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.models import HitCountMixin
from hitcount.utils import get_hitcount_model
from unicodedata import category

from .models import Category, News
from .forms import ContactForm, Commentform
# Create your views here.
from news_project.custom_permissions import OnlyLoggedSuperUser, UserPassesTestMixin
from django.db.models import Q
from hitcount.views import HitCountMixin

def news_list(request):
    # news_list = News.Published.all()
    news_list = News.objects.filter(status=News.Status.Published)
    context = {'news_list': news_list}
    return render(request, "news/news_list.html", context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin().hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hitcounted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = Commentform(data=request.POST)
        if comment_form.is_valid():
            # yangi comment obyektini yaratamiz lekin DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izox egasini so'rov yuborayotgan Userga bog'ladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = Commentform()
    else:
        comment_form = Commentform()
    context = {
        'news': news,
        'comments': comments,
        'comment_count' : comment_count,
        'comment_form': comment_form,
        'new_comment': new_comment,
    }
    return render(request, 'news/news_detail.html', context)

# def homePageView(request):
#     categories = Category.objects.all()
#     news_list = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:5]
#     local_one = News.objects.filter(
#         status=News.Status.Published,
#         category__name="Mahalliy"
#     )[:1]
#     local_news = News.objects.filter(
#         status=News.Status.Published,
#         category__name="Mahalliy"
#     )[1:5]
#
#     context = {
#         'news_list': news_list,
#         'categories': categories,
#         'local_one': local_one,
#         'local_news': local_news,
#     }
#     return render(request, 'news/home.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:5]
        context['mahalliy_xabarlar'] = News.objects.filter(status=News.Status.Published, category__name="Mahalliy").order_by('-publish_time')[:5]
        context['xorij_xabarlar'] = News.objects.filter(status=News.Status.Published, category__name="Xorij").order_by('-publish_time')[:5]
        context['sport_xabarlar'] = News.objects.filter(status=News.Status.Published, category__name="Sport").order_by('-publish_time')[:5]
        context['texnologiya_xabarlar'] = News.objects.filter(status=News.Status.Published, category__name="texnologiya").order_by('-publish_time')[:5]
        return context








# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> biz bilan bog'langaningiz uchun tashakkur!</h2>")
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'news/contact.html', context)

class ContactpageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {'form': form}
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2> biz bilan bog'langaningiz uchun tashakkur!</h2>")
        context = {'form': form}
        return render(request, 'news/contact.html', context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(status=News.Status.Published, category__name="Mahalliy").order_by('-publish_time')
        return news


class ForiegnNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'Xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(status=News.Status.Published, category__name="Xorij").order_by('-publish_time')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologik_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(status=News.Status.Published, category__name="texnologiya").order_by('-publish_time')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(status=News.Status.Published, category__name="Sport").order_by('-publish_time')
        return news

class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ['title', 'body', 'category', 'status', 'image']
    template_name = "crud/news_edit.html"
    success_url = reverse_lazy("home_page")

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = "crud/news_delete.html"
    success_url = reverse_lazy("home_page")


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = "crud/news_create.html"
    fields = ['title', 'body', 'category', 'status', 'image', 'slug']

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users,
    }

    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
