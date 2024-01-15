from django.conf import settings
from django.core.mail import send_mail
from .models import Reply

def notify_new_replay(pk):
    reply= Reply.objects.get(id=pk)
    send_mail(
        sibject=f'MMORPG - Новый отклик на ваше объяление',
        message=f'Здраствуйте, {reply.post.author}.\n'
                f'На ваше объявление "{reply.post.title}" новый отклик./n'
                f'Автор оклика, {reply.author} отвутил следующее:/n "{reply.text}",',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reply.post.aythor.email,],
        )

def notify_accept_reply(pk):
    reply = Reply.objects.get(id=pk)
    send_mail(
        subject=f'MMORPG - отклик принят.',
        message=f'Здраствуйте, {reply.author}.\n'
                f'Ваш отклик на объявление "{reply.post.title}" принят.\n'
                f'Посмотреть объявление можно здесь: "{reply.post.id}",',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reply.author.email,],
        )