from django.core.exceptions import ObjectDoesNotExist


def check_previous_reserve(model: object, data: dict) -> None:
    try:
        previous_slot_reserve = model.objects.get(
            parking_slot_id=data.get("parking_slot_id"),
            start_date=None,
            finish_date=None,
            exit_date__isnull=False,
        )
        previous_slot_reserve.start_date = data.get("start_date")
        previous_slot_reserve.finish_date = data.get("finish_date")
        previous_slot_reserve.exit_date = None
        previous_slot_reserve.save()
        return
    except ObjectDoesNotExist:
        pass
    model(**data).save()
