from django.db import models
from accounts.models import User
from accounts.others_models.model_profile import UserProfile
from helpers.utils import send_notification
from django.utils.translation import gettext_lazy as _

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Forncedores'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    # Send notification email
                    mail_subject = "Parabéns! Seu perfil foi aprovado na plataforma."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "Nos lamentamos! Você não é elegível para publicar seus produtos."
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)


