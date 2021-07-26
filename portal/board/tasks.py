from celery import shared_task

from django.core.mail import EmailMultiAlternatives


@shared_task
def send_mail(mail_to, mail_subject, mail_txt_content, mail_html_content):
    msg = EmailMultiAlternatives(
        subject=mail_subject,
        body=mail_txt_content,
        to=[mail_to],
    )
    msg.attach_alternative(mail_html_content, "text/html")

    msg.send()


# @shared_task
# def do_mailing():
#     end_date = datetime.now().replace(hour=8, minute=0, second=0)
#     start_date = end_date - timedelta(weeks=1)

#     for person in django.contrib.auth.get_user_model().objects.all():
#         send_post = Post.objects.filter(
#             creation_time__range=(start_date, end_date),
#             categories__in=Mailing.objects.filter(subscribers=person).
#             values('category')
#             )
#         if send_post:
#             html_content = render_to_string(
#                 'mailing_list.html',
#                 {
#                     'post': send_post,
#                     'user': person,
#                 }
#             )

#             msg_text = gettext(
#                 'Hello, %(name)s. New articles for the week:'
#             ) % {'name': person.username}

#             posts_list_txt = ', '.join([post.header for post in send_post])

#             msg = EmailMultiAlternatives(
#                 subject=gettext('New articles list'),
#                 body=msg_text+'\n'+posts_list_txt,
#                 # body=f'Здравствуй, {person.username}.'
#                 # f'Список новых статей за неделю:'
#                 # f'{posts_list_txt}',
#                 from_email='sf.testmail@yandex.ru',
#                 to=[person.email],
#             )
#             msg.attach_alternative(html_content, "text/html")

#             msg.send()
