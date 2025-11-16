import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    CommonPasswordValidator,
)


# Write your validator here
class CustomPasswordValidator:
    def __init__(self):
        self.user_attribute_validator = UserAttributeSimilarityValidator()
        self.common_password_validator = CommonPasswordValidator()

    def validate(self, password, user=None):
        # Check user attribute similarity
        self.user_attribute_validator.validate(password, user)

        # Check common passwords
        self.common_password_validator.validate(password)

        # Min length
        if len(password) < 6:
            raise ValidationError(
                _("This password must be at least 6 characters long."),
                code="password_too_short",
            )
        # Uppercase letter
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter."),
                code="password_no_upper",
            )
        # Number
        if not re.search(r"[0-9]", password):
            raise ValidationError(
                _("This password must contain at least one number."),
                code="password_no_number",
            )
        # Special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(
                _(
                    "This password must contain at least one special "
                    "character."
                ),
                code="password_no_special",
            )

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
