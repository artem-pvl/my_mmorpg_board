from django.views.generic import DetailView, ListView, CreateView, UpdateView,\
    DeleteView
from django.urls import reverse

from .models import Ad, Reply

from django.contrib.auth.mixins import LoginRequiredMixin

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


class ReplyCreate(CreateView):
    model = Reply
    template_name = ''
    context_object_name = 'reply_create'


class ReplyEdit(UpdateView):
    model = Reply
    template_name = ''
    context_object_name = 'reply_edit'
