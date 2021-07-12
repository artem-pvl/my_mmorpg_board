from django.views.generic import DetailView, ListView, CreateView, UpdateView,\
    DeleteView

from .models import Ad, Reply

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


class AdCreate(CreateView):
    model = Ad
    template_name = ''
    context_object_name = 'ad_create'


class AdEdit(UpdateView):
    model = Ad
    template_name = ''
    context_object_name = 'ad_edit'


class AdDelete(DeleteView):
    model = Ad
    template_name = ''
    context_object_name = 'ad_delete'


class ReplyList(ListView):
    model = Reply
    template_name = ''
    context_object_name = 'reply_list'


class ReplyCreate(CreateView):
    model = Reply
    template_name = ''
    context_object_name = 'reply_create'


class ReplyEdit(UpdateView):
    model = Reply
    template_name = ''
    context_object_name = 'reply_edit'
