from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from hotels_api.domain.entities.hotel import Customer

class CustomerRepository(ABC):
    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        pass
