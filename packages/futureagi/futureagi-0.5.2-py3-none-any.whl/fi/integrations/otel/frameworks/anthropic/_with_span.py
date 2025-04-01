import logging
from typing import Any, Dict, Optional, Union

from opentelemetry import trace as trace_api
from opentelemetry.util.types import Attributes, AttributeValue

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class _WithSpan:
    __slots__ = (
        "_span",
        "_is_finished",
    )

    def __init__(
        self,
        span: trace_api.Span,
    ) -> None:
        print(f"Initializing _WithSpan with span: {span}")
        self._span = span
        try:
            self._is_finished = not self._span.is_recording()
            print(
                f"Span recording status: {'recording' if not self._is_finished else 'not recording'}"
            )
        except Exception:
            logger.exception("Failed to check if span is recording")
            print("Error checking span recording status, defaulting to finished")
            self._is_finished = True

    @property
    def is_finished(self) -> bool:
        return self._is_finished

    def set_attribute(self, key: str, value: Any) -> None:
        self._span.set_attribute(key, value)

    def set_attributes(self, attributes: Dict[str, AttributeValue]) -> None:
        print(f"Setting attributes: {attributes}")

        self._span.set_attributes(attributes)

    def record_exception(self, exception: Exception) -> None:
        if self._is_finished:
            print(f"Skipping exception recording - span is finished: {exception}")
            return
        try:
            print(f"Recording exception: {type(exception).__name__}: {exception}")
            self._span.record_exception(exception)
        except Exception:
            logger.exception("Failed to record exception on span")
            print("Error recording exception on span")

    def set_status(self, status: Union[trace_api.Status, trace_api.StatusCode]) -> None:
        if self._is_finished:
            print(f"Skipping status setting - span is finished: {status}")
            return
        try:
            print(f"Setting span status: {status}")
            self._span.set_status(status=status)
        except Exception:
            logger.exception("Failed to set status on span")
            print("Error setting status on span")

    def add_event(self, name: str) -> None:
        if self._is_finished:
            print(f"Skipping event addition - span is finished: {name}")
            return
        try:
            print(f"Adding event: {name}")
            self._span.add_event(name)
        except Exception:
            logger.exception("Failed to add event to span")
            print("Error adding event to span")

    def finish_tracing(
        self,
        status: Optional[trace_api.Status] = None,
        attributes: Attributes = None,
        extra_attributes: Attributes = None,
    ) -> None:
        if self._is_finished:
            print("Skipping finish_tracing - span is already finished")
            return

        print("Starting finish_tracing process")
        for mapping in (attributes, extra_attributes):
            if not mapping:
                continue
            print(f"Processing attributes mapping: {mapping}")
            for key, value in mapping.items():
                if value is None:
                    continue
                try:
                    print(f"Setting attribute: {key}={value}")
                    self._span.set_attribute(key, value)
                except Exception:
                    logger.exception("Failed to set attribute on span")
                    print(f"Error setting attribute: {key}")

        if status is not None:
            try:
                print(f"Setting final status: {status}")
                self._span.set_status(status=status)
            except Exception:
                logger.exception("Failed to set status code on span")
                print("Error setting final status")

        try:
            print("Ending span")
            self._span.end()
        except Exception:
            logger.exception("Failed to end span")
            print("Error ending span")

        self._is_finished = True
        print("Span finished successfully")
