from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
from django.template.loader import render_to_string

from django.views.generic import DetailView, ListView, CreateView, UpdateView,\
    DeleteView
from django_filters.views import FilterView

from .models import Ad, Reply, News
from .filters import AdFilter
from .tasks import send_mail

# from django.shortcuts import render

# Create your views here.


class AdList(ListView):
    model = Ad
    template_name = "ad_list.html"
    context_object_name = 'ads'
    ordering = ['-creation_time']
    paginate_by = 30


class AdDetail(DetailView):
    model = Ad
    template_name = "ad_detail.html"
    context_object_name = 'ad'


class AdFiltered(LoginRequiredMixin, FilterView):
    # model = Ad
    filterset_class = AdFilter
    template_name = 'ad_filtered.html'
    context_object_name = 'ad_filtered'
    ordering = ['-creation_time']
    paginate_by = 5

    def get_queryset(self):
        # queryset = Ad.objects.filter(user_id=self.request.user)
        queryset = Ad.objects.filter(user_id=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reply_list'] = Reply.objects.filter(
            ad_id__in=Ad.objects.filter(user_id=self.request.user)
        ).order_by('is_approved', '-creation_time')
        return context

    def form_valid(self, form):
        print(form.instance)
        return super().form_valid(form)


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
    template_name = 'reply_list.html'
    context_object_name = 'reply_list'
    ordering = ['-creation_time']
    paginate_by = 30

    def get_queryset(self):
        queryset = Reply.objects.\
            filter(user_id=self.request.user).order_by('-creation_time')
        return queryset


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
    ordering = ['-creation_time']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_mailing_list'] = self.request.user.groups.filter(
                name='mailing_list'
            ).exists()
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'


class NewsMailingConfirm(LoginRequiredMixin, PermissionRequiredMixin,
                         DetailView):
    model = News
    template_name = 'news_confirm_mailing.html'
    context_object_name = 'news'
    permission_required = ('board.create_news',)


@permission_required('board.create_news')
def news_mailing_confirm(reqest, pk):
    site = 'https://{domain}'.format(
        domain=Site.objects.get_current().domain,
    )

    url = '{domain}{path}'.format(
        domain=site,
        path=reverse('news_detail_view', args=[pk]),
    )

    mailing_news = News.objects.get(id=pk)
    mailing_users = get_user_model().objects.filter(
        groups__name='mailing_list',
    )

    for user in mailing_users:
        user_email = user.email
        html_content = render_to_string(
            'email/mail_mailing_news.html',
            {
                'news': mailing_news,
                'site': site,
                'url': url,
                'user': user_email,
            }
        )
        txt_content = render_to_string(
            'email/mail_mailing_news.txt',
            {
                'news': mailing_news,
                'site': site,
                'url': url,
                'user': user_email,
            }
        )
        subject = render_to_string(
            'email/subject_mailing_news.txt',
            {
                'site': site,
                'news': mailing_news,
            }
        )
        mail_to = [user_email]

        send_mail.delay(mail_to, subject, txt_content, html_content)
    return redirect(reverse('news_list_view'))


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    fields = ['header', 'news']
    template_name = 'news_create.html'
    context_object_name = 'news_create'
    success_url = '/board/news'
    permission_required = ('board.create_news',)

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    fields = ['header', 'news']
    template_name = 'news_create.html'
    context_object_name = 'news_create'
    success_url = '/board/news'
    permission_required = ('board.change_news',)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'news_delete.html'
    context_object_name = 'news_delete'
    success_url = '/board/news'
    permission_required = ('board.delete_news',)


@login_required
def news_subscribe(request):
    group, created = Group.objects.get_or_create(name='mailing_list')
    group.user_set.add(request.user)

    return redirect(reverse('news_list_view'))


@login_required
def news_unsubscribe(request):
    group, created = Group.objects.get_or_create(name='mailing_list')
    group.user_set.remove(request.user)

    return redirect(reverse('news_list_view'))
