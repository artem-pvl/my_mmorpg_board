from django.views.generic import DetailView, ListView, CreateView, UpdateView,\
    DeleteView

from .models import Ad, Reply
from .filters import AdFilter

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required

# from django.shortcuts import render

# Create your views here.


class AdList(ListView):
    model = Ad
    template_name = "ad_list.html"
    context_object_name = 'ads'


class AdDetail(DetailView):
    model = Ad
    template_name = "ad_detail.html"
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reply_list'] = Reply.objects.filter(ad_id=self.kwargs['pk'])
        return context


class AdFiltered(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ad_filtered.html'
    context_object_name = 'ad_filtered'
    ordering = ['-creation_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdFilter(
            self.request.GET,
            queryset=Ad.objects.filter(user_id=self.request.user)
        )
        context['reply_list'] = Reply.objects.filter(
            ad_id=Ad.objects.filter(user_id=self.request.user)
        )
        return context


class AdCreate(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ['category_id', 'header', 'ad']
    template_name = 'ad_create.html'
    context_object_name = 'ad_create'
    success_url = '/board/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class AdEdit(UpdateView):
    model = Ad
    fields = ['category_id', 'header', 'ad']
    template_name = 'ad_create.html'
    context_object_name = 'ad_edit'
    success_url = '/board/'


class AdDelete(DeleteView):
    model = Ad
    template_name = 'ad_delete.html'
    context_object_name = 'ad_delete'
    success_url = '/board/'


class ReplyList(ListView):
    model = Reply
    template_name = ''
    context_object_name = 'reply_list'
    ordering = '-creation_time'


class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'reply_create.html'
    fields = ['reply']
    context_object_name = 'reply_create'
    success_url = '/board/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.ad_id = Ad.objects.get(id=self.kwargs['ad_id'])
        return super().form_valid(form)


class ReplyEdit(UpdateView):
    model = Reply
    template_name = ''
    context_object_name = 'reply_edit'
