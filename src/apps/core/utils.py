import random
import string
from datetime import datetime
from os.path import splitext

from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _


def random_num(size=10, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def get_time(frmt: str = "%Y-%m-%d %H:%M"):
    time = timezone.now()
    if frmt is not None:
        time = time.strftime(frmt)

    return time


def upload_file_src(instance, path):
    now = get_time("%Y-%m-%d")
    return f"files/{now}/{path}"


def get_file_extension(file_name):
    if not file_name or not hasattr(file_name, "file") or not file_name.file.name:
        return None
    name, extension = splitext(file_name.file.name)
    return extension


def validate_form(request, form):
    if form.is_valid():
        return True

    errors = form.errors.items()

    if not errors:
        messages.error(request, _("Entered data is not correct."))
        return False

    for _field, message in errors:
        for error in message:
            messages.error(request, error)

    return False


def toast_form_errors(request, form):
    errors = form.errors.items()
    if not errors:
        messages.error(request, _("Entered data is not correct."))
        return False

    for _field, message in errors:
        for error in message:
            messages.error(request, error)


def get_user_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]

    return request.META.get("REMOTE_ADDR")


def convert_str_to_bool(str_vlue):
    if str_vlue == "true":
        return True
    return False
