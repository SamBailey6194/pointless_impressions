import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    CommonPasswordValidator,
)


# Write your validator here
class CustomPasswordValidator:
    def __init__(self, min_length=6):
        self.min_length = min_length
        self.user_attribute_validator = UserAttributeSimilarityValidator()
        self.common_password_validator = CommonPasswordValidator()

    def validate(self, password, user=None):
        errors = []

        self.user_attribute_validator.validate(password, user)

        self.common_password_validator.validate(password)

        if len(password) < self.min_length:
            raise ValidationError(
                _("This password must be at least 6 characters long."),
                code="password_too_short",
            )
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter."),
                code="password_no_upper",
            )
        if not re.search(r"[0-9]", password):
            raise ValidationError(
                _("This password must contain at least one number."),
                code="password_no_number",
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(
                _(
                    "This password must contain at least one special "
                    "character."
                ),
                code="password_no_special",
            )
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            "Your password must include: \n"
            "- At least 6 characters long, \n"
            "- At least one uppercase letter, \n"
            "- At least one number, \n"
            "- At least one special character. \n"
            "\n"
            "It must not be too similar to your personal "
            "information and should avoid common passwords."
        )
