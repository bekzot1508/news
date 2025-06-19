from django.urls import path
from .views import  news_list, news_detail, ContactpageView,HomePageView, LocalNewsView, ForiegnNewsView, TechnologyNewsView, SportNewsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name='all_news_list'),
    path("news/<slug:news>/", news_detail, name='news_detail_page'),
    path('news/contact-us/', ContactpageView.as_view(), name='contact_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('tech/', TechnologyNewsView.as_view(), name='tech_news_page'),
    path('foriegn/', ForiegnNewsView.as_view(), name='foreign_news_page'),
]