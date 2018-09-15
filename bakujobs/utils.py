from django.core.mail import send_mail
from django.utils.text import slugify
from django.template import loader
import random
import string

# def mailer(job):
#     template = loader.get_template("bakujobs/email.html")
#     body = template.render({'job': job})
#     mail.send(
#         job.email,
#         "jobsbaki@gmail.com",
#         subject="You just posted a job on bakujobs.az",
#         message="whatever"
#     )

def send_job_mail(job):
    subject = "You just posted a job on bakujobs.az"
    template = loader.get_template("bakujobs/email.html")
    body = template.render({'job': job})
    to_email = [job.email]
    from_email = "jobsbaki@gmail.com"

    return send_mail(subject, body, from_email, to_email,
                     fail_silently=False, html_message=body)

def random_string_generator(size=2, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
