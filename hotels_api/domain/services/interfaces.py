from abc import ABC, abstractmethod
from hotels_api.domain.entities.hotel import Customer

# Servicio de dominio para notificaciones (implementación concreta en infraestructura)
class NotificationService(ABC):
    @abstractmethod
    def notify_reservation_approved(self, reservation: 'Reservation', customer: Customer) -> None:
        pass

    @abstractmethod
    def notify_reservation_rejected(self, reservation: 'Reservation', customer: Customer) -> None:
        pass
