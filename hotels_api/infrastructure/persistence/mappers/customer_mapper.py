from hotels_api.domain.entities.hotel import Customer
from hotels_api.domain.value_objects.common import Email, PhoneNumber
from hotels_api.infrastructure.persistence.models.customer import CustomerModel


def to_entity(model: CustomerModel) -> Customer:
    return Customer(
        id=model.id,
        name=model.name,
        email=Email(model.email),
        phone=PhoneNumber(model.phone),
    )


def to_model(entity: Customer) -> CustomerModel:
    obj, _ = CustomerModel.objects.get_or_create(id=entity.id)
    obj.name = entity.name
    obj.email = entity.email.value
    obj.phone = entity.phone.value
    return obj
