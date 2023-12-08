from datetime import datetime 
from typing import Any, Callable


__callbacks: dict[str, list[Callable[..., Any]]] = {}


class Event:
    def __init__(self):
        self.created: datetime
        self.event_type: str
        self.data: dict[str, Any]
        self.sender: object

    def __repr__(self) -> str:
        elements: list[str] = [repr(self.sender), ' -> ', self.event_type, ' @ ', str(self.created)]
        return ''.join(elements)
    

def event(sender: object, event_type: str, data: dict[str, Any]) -> Event:
    e = Event()
    e.sender = sender
    e.event_type = event_type
    e.data = data
    e.created = datetime.now()
    return e


def bind(event_type: str, callback: Callable[..., Any]) -> None:
    if event_type not in __callbacks:
        __callbacks.update({event_type: []})
    if callback not in __callbacks[event_type]:
        __callbacks[event_type].append(callback)


def unbind(event_type: str, callback: Callable[..., Any]) -> None:
    if event_type in __callbacks:
        __callbacks[event_type].remove(callback)


def publish_event(event: Event) -> None:
    if event.event_type in __callbacks:
        for callback in __callbacks[event.event_type]:
            callback(event)
