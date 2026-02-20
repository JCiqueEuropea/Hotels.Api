from hotels_api.domain.entities.room import EventRoom
from hotels_api.domain.value_objects.common import Money
from hotels_api.infrastructure.persistence.models.event_room import EventRoomModel


def to_entity(model: EventRoomModel) -> EventRoom:
    return EventRoom(
        id=model.id,
        hotel_id=model.hotel_id,
        name=model.name,
        capacity=model.capacity,
        hourly_rate=Money(amount=model.hourly_rate_amount, currency=model.hourly_rate_currency),
        schedule=model.schedule or {},
    )


def to_model(entity: EventRoom) -> EventRoomModel:
    obj, _ = EventRoomModel.objects.get_or_create(id=entity.id)
    obj.hotel_id = entity.hotel_id
    obj.name = entity.name
    obj.capacity = entity.capacity
    obj.hourly_rate_amount = entity.hourly_rate.amount
    obj.hourly_rate_currency = entity.hourly_rate.currency
    obj.schedule = entity.schedule or {}
    return obj
