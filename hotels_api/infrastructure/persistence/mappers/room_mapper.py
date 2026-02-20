from hotels_api.domain.entities.room import Room, RoomType
from hotels_api.domain.value_objects.common import Money
from hotels_api.infrastructure.persistence.models.room import RoomModel


def to_entity(model: RoomModel) -> Room:
    return Room(
        id=model.id,
        hotel_id=model.hotel_id,
        number=model.number,
        room_type=RoomType[model.room_type],
        price=Money(amount=model.price_amount, currency=model.price_currency),
        is_active=model.is_active,
    )


def to_model(entity: Room) -> RoomModel:
    obj, _ = RoomModel.objects.get_or_create(id=entity.id)
    obj.hotel_id = entity.hotel_id
    obj.number = entity.number
    obj.room_type = entity.room_type.name
    obj.price_amount = entity.price.amount
    obj.price_currency = entity.price.currency
    obj.is_active = entity.is_active
    return obj
