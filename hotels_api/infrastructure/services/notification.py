import logging
from hotels_api.domain.services.interfaces import NotificationService
from hotels_api.domain.entities.hotel import Customer

logger = logging.getLogger(__name__)


class LoggingNotificationService(NotificationService):
    def notify_reservation_approved(self, reservation, customer: Customer) -> None:
        logger.info(
            "notification=reservation_approved reservation_id=%s customer_email=%s",
            str(reservation.id),
            customer.email.value,
        )

    def notify_reservation_rejected(self, reservation, customer: Customer) -> None:
        logger.info(
            "notification=reservation_rejected reservation_id=%s customer_email=%s",
            str(reservation.id),
            customer.email.value,
        )
