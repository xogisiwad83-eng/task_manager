from datetime import datetime
from observers.base import Observer


class NotificationObserver(Observer):

    def __init__(self):
        self._notifications = []
'''Принимает название события и данные.
Формирует структуру (словарь) с ключами: 
event, data, timestamp (время события).
Сохраняет уведомление в историю.
Выводит сообщение в консоль в формате:
� Notification: {event}.'''
    def update(self, event: str, data):
        notification = {
            "event": event,
            "data": data,
            "timestamp": datetime.now()
        }
        self._notifications.append(notification)
        print(f"🔔 Notification: {event}")
''' Возвращает список последних 
limitуведомлений.
'''
    def get_notifications(self, limit: int):
        return self._notifications[-limit:]
''' чистит историю'''
    def clear_notifications(self):
        self._notifications.clear()
