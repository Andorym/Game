from django.conf import settings
from django.core.mail import send_mail
from .models import Reply

def notify_new_replay(pk):
    reply= Reply.objects.get(id=pk)
    send_mail(
        sibject=f'MMORPG - ����� ������ �� ���� ���������',
        message=f'�����������, {reply.post.author}.\n'
                f'�� ���� ���������� "{reply.post.title}" ����� ������./n'
                f'����� ������, {reply.author} ������� ���������:/n "{reply.text}",',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reply.post.aythor.email,],
        )

def notify_accept_reply(pk):
    reply = Reply.objects.get(id=pk)
    send_mail(
        subject=f'MMORPG - ������ ������.',
        message=f'�����������, {reply.author}.\n'
                f'��� ������ �� ���������� "{reply.post.title}" ������.\n'
                f'���������� ���������� ����� �����: "{reply.post.id}",',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reply.author.email,],
        )