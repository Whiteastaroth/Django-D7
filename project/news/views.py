from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import NewForm
from .filters import NewFilter
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import New, Category, Subscription

class NewList(ListView):
    model = New
    template_name = 'new/index.html'
    ordering = ['-date']
    ontext_object_name = 'new'
    paginate_by = 10

class SearchList(ListView):
    model = New
    ordering = ['-date']
    template_name = 'new/search.html'
    context_object_name = 'new'
    paginate_by = 10



    def get_filter(self):
        return NewFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {**super().get_context_data(*args, **kwargs), 'filter': self.get_filter(), }

class Newid(DetailView):
    model = New
    template_name = 'new/news_id.html'
    context_object_name = 'new'

class NewCreate(PermissionRequiredMixin,  CreateView):
    permission_required = ('news.add_new',)
    model = New
    form_class = NewForm
    template_name = 'new/create.html'


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_record',)
    model = New
    form_class = NewForm                             # Для формы обновления, используем уже созданный класс RecordForm из form.py
    template_name = 'new/create.html'
    success_url = reverse_lazy('index')

class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_record',)
    model = New
    template_name = 'new/news_delete.html'
    success_url = reverse_lazy('index')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
        ).order_by('title')
    return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions}, )

