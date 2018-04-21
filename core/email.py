# from dbmail import send_db_mail
# from django.conf import settings
#
# class Email:
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def send(slug, recipient, *args, **kwargs):
#         """
#         :param slug: email template -slug
#         :param recipient: recipient email address
#         :return: None
#         """
#         if settings.NOTIFY_EMAIL == 'True':
#             send_db_mail(slug, recipient, *args, use_celery=True, **kwargs)
