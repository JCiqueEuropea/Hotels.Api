from dataclasses import dataclass, field
from uuid import UUID, uuid4
from hotels_api.domain.value_objects.common import Email, PhoneNumber

@dataclass
class Customer:
    id: UUID
    name: str
    email: Email
    phone: PhoneNumber

    @classmethod
    def create(cls, name: str, email: str, phone: str) -> 'Customer':
        return cls(
            id=uuid4(),
            name=name,
            email=Email(email),
            phone=PhoneNumber(phone)
        )

@dataclass
class Hotel:
    id: UUID
    name: str
    address: str

    @classmethod
    def create(cls, name: str, address: str) -> 'Hotel':
        return cls(
            id=uuid4(),
            name=name,
            address=address
        )
