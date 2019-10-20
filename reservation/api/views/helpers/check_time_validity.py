from django.utils import timezone


def check_time_validity(start_date, finish_date):
    now = str(timezone.now())
    if (
        start_date < now
        or finish_date < now
        or finish_date < start_date
    ):
        return False
    else:
        return True
