from django.forms import ValidationError
from django.utils import timezone


def validate_deadline(deadline):
    delta_time = deadline - timezone.now()

    delta_hours = delta_time.total_seconds() // 3600
    if delta_hours < 72:
        raise ValidationError('Needs to be at least 72 hours! Now was {} hours.'.format(delta_hours))
