def check_previous_reserve(model: object, data: dict) -> None:
    previous_slot_reserve = model.objects.filter(
        parking_slot_id=data.get("parking_slot_id"),
        start_date=None,
        finish_date=None,
        exit_date__isnull=False,
    )
    if previous_slot_reserve:
        data["exit_date"] = None
        previous_slot_reserve.update(**data)
        return
    model(**data).save()
