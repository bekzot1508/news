from django.urls import path
from .views import news_list, news_detail, ContactpageView, HomePageView, LocalNewsView, ForiegnNewsView, \
    TechnologyNewsView, SportNewsView, NewsDeleteView, NewsUpdateView, NewsCreateView, admin_page_view, \
    Commentform, SearchResultsList

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name='all_news_list'),
    path("news/<slug:news>/", news_detail, name='news_detail_page'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('contact-us/', ContactpageView.as_view(), name='contact_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('tech/', TechnologyNewsView.as_view(), name='tech_news_page'),
    path('foriegn/', ForiegnNewsView.as_view(), name='foreign_news_page'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name='search_results'),
]