from django.forms import ValidationError
from django.utils import timezone


# a validator for checking that the user inputted deadline is at least 72h into the future
def validate_deadline(deadline):
    delta_time = deadline - timezone.now()

    delta_hours = delta_time.total_seconds() // 3600
    if delta_hours < 72:
        raise ValidationError('Needs to be at least 72 hours! Now was {} hours.'.format(delta_hours))
