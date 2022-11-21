from NFLrating.celery import app
from django.core.mail import send_mail
from django.contrib.auth.models import User
from mainapp.services import in_seven_days
from datetime import date


@app.task
def send_beat_mail():
    """ Send message to user after 7 days have passed since last random voting. """
    for user in User.objects.all():
        if in_seven_days(user=user) is None:
            pass
        elif in_seven_days(user=user) <= date.today():
            send_mail(
                'Notification ',
                'Seven days have passed.'
                'You should make a random voting on "NFL Player Rankings'
                '  site to get all functions on the site again".',
                'ruslan84598459@gmail.com',
                [user.email],
                fail_silently=False,
            )
