from django.views.generic import DetailView, ListView, CreateView, UpdateView,\
    DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Ad, Reply, News
from .filters import AdFilter

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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['reply_list'] = Reply.objects.filter(
    #         ad_id=self.kwargs['pk'], is_approved=True
    #     )
    #     return context


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
            ad_id__in=Ad.objects.filter(user_id=self.request.user)
        ).order_by('is_approved', '-creation_time')
        return context


class AdCreate(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ['category_id', 'header', 'ad']
    template_name = 'ad_create.html'
    context_object_name = 'ad_create'
    success_url = '/board/ad'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class AdEdit(LoginRequiredMixin, UpdateView):
    model = Ad
    fields = ['category_id', 'header', 'ad']
    template_name = 'ad_create.html'
    context_object_name = 'ad_create'
    success_url = '/board/ad'


class AdDelete(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ad_delete.html'
    context_object_name = 'ad_delete'
    success_url = '/board/ad'


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'reply_list.html'
    context_object_name = 'reply_list'
    ordering = ['-creation_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reply_list'] = Reply.objects.filter(user_id=self.request.user)
        return context


class ReplyConfirmApprove(LoginRequiredMixin, DetailView):
    model = Reply
    template_name = "reply_approve.html"
    context_object_name = 'reply'


@login_required
def approve_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    if request.user.id == reply.ad_id.user_id.id:
        reply.is_approved = True
        reply.save()

    return redirect('/board/ad/filtered')


class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'reply_create.html'
    fields = ['reply']
    context_object_name = 'reply_create'
    success_url = '/board/ad'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.ad_id = Ad.objects.get(id=self.kwargs['ad_id'])
        return super().form_valid(form)


class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'reply_delete.html'
    context_object_name = 'reply_delete'
    success_url = '/board/ad/filtered'


class NewsList(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_editor'] = self.request.user.groups.\
            filter(name='news_edit').exists()
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_editor'] = self.request.user.groups.\
            filter(name='news_edit').exists()
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    fields = ['header', 'news']
    template_name = 'news_create.html'
    context_object_name = 'news_create'
    success_url = '/board/news'
    permission_required = ('board.news_editor',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_editor'] = self.request.user.groups.\
            filter(name='news_edit').exists()
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    fields = ['header', 'news']
    template_name = 'news_create.html'
    context_object_name = 'news_create'
    success_url = '/board/news'
    permission_required = ('board.news_editor',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_editor'] = self.request.user.groups.\
            filter(name='news_edit').exists()
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'news_delete.html'
    context_object_name = 'news_delete'
    success_url = '/board/news'
    permission_required = ('board.news_editor',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_editor'] = self.request.user.groups.\
            filter(name='news_edit').exists()
        return context
