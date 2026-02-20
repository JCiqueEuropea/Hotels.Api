from hotels_api.domain.entities.reservation import Reservation
from hotels_api.domain.value_objects.common import DateRange
from hotels_api.domain.value_objects.reservation_status import ReservationStatus
from hotels_api.infrastructure.persistence.models.reservation import ReservationModel


def to_entity(model: ReservationModel) -> Reservation:
    return Reservation(
        id=model.id,
        customer_id=model.customer_id,
        room_id=model.room_id,
        date_range=DateRange(start_date=model.start_date, end_date=model.end_date),
        status=ReservationStatus[model.status],
    )


def to_model(entity: Reservation) -> ReservationModel:
    obj, _ = ReservationModel.objects.get_or_create(id=entity.id)
    obj.customer_id = entity.customer_id
    obj.room_id = entity.room_id
    obj.start_date = entity.date_range.start_date
    obj.end_date = entity.date_range.end_date
    obj.status = entity.status.value
    return obj
