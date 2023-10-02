from django.urls import path
from .views import NewList, Newid, NewCreate, NewUpdate, NewDelete, SearchList, subscriptions

urlpatterns = [

    path('news_list/', NewList.as_view(), name= 'index'),
    path('new/<int:pk>', Newid.as_view(), name='news_id'),                 # переход по динамическим страницам


    path('create/', NewCreate.as_view(), name= 'create'),                           # переход на страницу добавления записи
    path('<int:pk>/updata', NewUpdate.as_view(), name='updata'),
    path('<int:pk>/delete/', NewDelete.as_view(),name = 'delete'),
    path('search/', SearchList.as_view(), name='search'),

    path('subscriptions/', subscriptions, name='subscriptions')

]
