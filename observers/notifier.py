from datetime import datetime
from observers.base import Observer


class NotificationObserver(Observer):

    def __init__(self):
        self._notifications = []

    def update(self, event: str, data):
        notification = {
            "event": event,
            "data": data,
            "timestamp": datetime.now()
        }
        self._notifications.append(notification)
        print(f"🔔 Notification: {event}")

    def get_notifications(self, limit: int):
        return self._notifications[-limit:]

    def clear_notifications(self):
        self._notifications.clear()
