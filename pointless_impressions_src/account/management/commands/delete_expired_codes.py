from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now
from pointless_impressions_src.account.models import EmailVerificationCode


# Write your management command here.
class Command(BaseCommand):
    help = "Delete expired email verification codes"

    def handle(self, *args, **kwargs):
        expired_codes = EmailVerificationCode.objects.filter(
            created_at__lt=now() - timezone.timedelta(
                seconds=settings.VERIFICATION_TOKEN_EXPIRY
                )
        )
        count = expired_codes.delete()[0]
        self.stdout.write(f"Deleted {count} expired verification codes.")
