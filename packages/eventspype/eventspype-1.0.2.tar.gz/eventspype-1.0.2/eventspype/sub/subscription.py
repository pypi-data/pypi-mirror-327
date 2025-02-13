from collections.abc import Callable
from enum import Enum
from functools import partial
from typing import Any, TypeVar

from eventspype.event import EventTag
from eventspype.pub.multipublisher import MultiPublisher
from eventspype.pub.publication import EventPublication
from eventspype.pub.publisher import EventPublisher
from eventspype.sub.functional import FunctionalEventCallback, FunctionalEventSubscriber

T = TypeVar("T")

SubscriberCompleteEventCallback = Callable[[Any, Any, EventTag, Any], Any]
SubscriberSimpleEventCallback = Callable[[Any, Any], Any]
EventSubscriptionCallback = (
    FunctionalEventCallback
    | SubscriberCompleteEventCallback
    | SubscriberSimpleEventCallback
)


class EventSubscription:
    def __init__(
        self,
        publisher_class: type[EventPublisher] | type[MultiPublisher],
        event_tag: EventTag | list[EventTag],
        callback: EventSubscriptionCallback,
        callback_with_subscriber: bool = True,
        callback_with_event_info: bool = True,
    ) -> None:
        if not issubclass(publisher_class, EventPublisher) and not issubclass(
            publisher_class, MultiPublisher
        ):
            raise ValueError(
                "Publisher class must be a subclass of EventPublisher or MultiPublisher"
            )

        self._publisher_class = publisher_class
        self._event_tag = event_tag
        self._callback = callback
        self._callback_with_subscriber = callback_with_subscriber
        self._callback_with_event_info = callback_with_event_info

    def __call__(
        self,
        publisher: EventPublisher,
        subscriber: Any | None = None,
    ) -> list[FunctionalEventSubscriber]:
        return self.subscribe(publisher, subscriber)

    def __hash__(self) -> int:
        return hash((self.publisher_class, self.event_tag_str, self.callback))

    # === Properties ===

    @property
    def publisher_class(self) -> Any:
        return self._publisher_class

    @property
    def event_tag(self) -> EventTag | list[EventTag]:
        return self._event_tag

    @property
    def callback(self) -> Callable[..., Any]:
        return self._callback

    @property
    def callback_with_subscriber(self) -> bool:
        return self._callback_with_subscriber

    @property
    def event_tag_str(self) -> str:
        tags = str(self.event_tag)
        if isinstance(self.event_tag, list):
            tags = ", ".join(sorted([str(tag) for tag in self.event_tag]))
            tags = f"[{tags}]"
        return tags

    # === Subscriptions ===

    def subscribe(
        self, publisher: EventPublisher | MultiPublisher, subscriber: Any
    ) -> list[FunctionalEventSubscriber]:
        subscribers = []
        tags = self._get_event_tags(self.event_tag)
        for event_tag in tags:
            subscribers.append(self._subscribe(publisher, event_tag, subscriber))
        return subscribers

    def unsubscribe(
        self,
        publisher: EventPublisher | MultiPublisher,
        subscriber: FunctionalEventSubscriber,
    ) -> None:
        tags = self._get_event_tags(self.event_tag)
        for event_tag in tags:
            self._unsubscribe(publisher, subscriber, event_tag)

    def _get_event_tags(self, event_tag: EventTag | list[EventTag]) -> list[EventTag]:
        tags = event_tag if isinstance(event_tag, list) else [event_tag]
        return [tag if isinstance(tag, Enum | int) else hash(self) for tag in tags]

    def _subscribe(
        self,
        publisher: EventPublisher | MultiPublisher,
        event_tag: EventTag,
        subscriber: Any | None = None,
    ) -> FunctionalEventSubscriber:
        if not isinstance(publisher, self.publisher_class):
            raise ValueError("Publisher type mismatch")

        callback = self.callback
        if self.callback_with_subscriber:
            if subscriber is None:
                raise ValueError("Subscriber is required for callback with subscriber")
            if hasattr(self.callback, "__name__"):
                callback = getattr(subscriber, self.callback.__name__)
            else:
                callback = self.callback
            callback = partial(callback, subscriber)

        subscriber = FunctionalEventSubscriber(
            callback, with_event_info=self._callback_with_event_info
        )
        if isinstance(publisher, MultiPublisher):
            publication = self._get_publication(publisher, event_tag)
            publisher.add_subscriber(publication, subscriber)
        else:
            publisher.add_subscriber(subscriber)
        return subscriber

    def _unsubscribe(
        self,
        publisher: EventPublisher | MultiPublisher,
        subscriber: FunctionalEventSubscriber,
        event_tag: EventTag,
    ) -> None:
        if not isinstance(publisher, self.publisher_class):
            raise ValueError("Publisher type mismatch")

        if isinstance(publisher, MultiPublisher):
            publication = self._get_publication(publisher, event_tag)
            publisher.remove_subscriber(publication, subscriber)
        else:
            publisher.remove_subscriber(subscriber)

    def _get_publication(
        self, publisher: MultiPublisher, event_tag: EventTag
    ) -> EventPublication:
        publication = publisher.get_event_definition_by_tag(event_tag)
        return publication


class PublicationSubscription(EventSubscription):
    def __init__(
        self,
        publisher_class: type[MultiPublisher],
        event_publication: EventPublication,
        callback: Callable[..., Any],
        callback_with_subscriber: bool = True,
        callback_with_event_info: bool = True,
    ) -> None:
        if not issubclass(publisher_class, MultiPublisher):
            raise ValueError("Publisher class must be a subclass of MultiPublisher")

        super().__init__(
            publisher_class,
            event_publication.event_tag,
            callback,
            callback_with_subscriber=callback_with_subscriber,
            callback_with_event_info=callback_with_event_info,
        )
        self._event_publication = event_publication

    def _get_publication(
        self, publisher: MultiPublisher, event_tag: EventTag
    ) -> EventPublication:
        return self._event_publication
