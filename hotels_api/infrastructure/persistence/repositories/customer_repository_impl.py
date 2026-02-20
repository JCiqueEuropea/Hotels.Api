from typing import Optional
from uuid import UUID

from hotels_api.domain.entities.hotel import Customer
from hotels_api.domain.repositories.customer_repository import CustomerRepository
from hotels_api.infrastructure.persistence.mappers import customer_mapper
from hotels_api.infrastructure.persistence.models.customer import CustomerModel


class DjangoCustomerRepository(CustomerRepository):
    def save(self, customer: Customer) -> None:
        obj = customer_mapper.to_model(customer)
        obj.save()

    def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(id=customer_id)
            return customer_mapper.to_entity(model)
        except CustomerModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(email=email)
            return customer_mapper.to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
