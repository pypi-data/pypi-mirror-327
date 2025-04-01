import logging
from typing import Any, Iterator, NamedTuple, Optional, Protocol, Tuple

from opentelemetry import trace as trace_api
from opentelemetry.util.types import Attributes, AttributeValue

from fi.integrations.otel.frameworks.anthropic._with_span import _WithSpan
from fi.integrations.otel.instrumentation import safe_json_dumps
from fi.integrations.otel.types import FiMimeTypeValues, SpanAttributes

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class _ValueAndType(NamedTuple):
    value: str
    type: FiMimeTypeValues


class _HasAttributes(Protocol):
    def get_attributes(self) -> Iterator[Tuple[str, AttributeValue]]: ...

    def get_extra_attributes(self) -> Iterator[Tuple[str, AttributeValue]]: ...


def _finish_tracing(
    with_span: _WithSpan,
    has_attributes: _HasAttributes,
    status: Optional[trace_api.Status] = None,
) -> None:
    print(f"Starting _finish_tracing with status: {status}")
    try:
        print("Getting base attributes")
        attributes: Attributes = dict(has_attributes.get_attributes())
        print(f"Base attributes: {attributes}")
    except Exception as e:
        print(f"Failed to get attributes: {e}")
        logger.exception("Failed to get attributes")
        attributes = None

    try:
        print("Getting extra attributes")
        extra_attributes: Attributes = dict(has_attributes.get_extra_attributes())
        print(f"Extra attributes: {extra_attributes}")
    except Exception as e:
        print(f"Failed to get extra attributes: {e}")
        logger.exception("Failed to get extra attributes")
        extra_attributes = None

    try:
        print("Finishing tracing with collected attributes")
        with_span.finish_tracing(
            status=status,
            attributes=attributes,
            extra_attributes=extra_attributes,
        )
        print("Tracing finished successfully")
    except Exception as e:
        print(f"Failed to finish tracing: {e}")
        logger.exception("Failed to finish tracing")
        raise


def _io_value_and_type(obj: Any) -> _ValueAndType:
    print(f"Processing IO value and type for object of type: {type(obj)}")
    try:
        print("Attempting JSON serialization")
        json_value = safe_json_dumps(obj)
        print("JSON serialization successful")
        return _ValueAndType(json_value, FiMimeTypeValues.JSON)
    except Exception as e:
        print(f"Failed to serialize as JSON: {e}")
        logger.exception("Failed to get input attributes from request parameters.")

    print("Falling back to string representation")
    return _ValueAndType(str(obj), FiMimeTypeValues.TEXT)


def _as_input_attributes(
    value_and_type: Optional[_ValueAndType],
) -> Iterator[Tuple[str, AttributeValue]]:
    print(f"Processing input attributes for value_and_type: {value_and_type}")
    if not value_and_type:
        print("No value_and_type provided, returning empty iterator")
        return

    print(f"Yielding input value: {value_and_type.value[:100]}... (truncated)")
    yield SpanAttributes.INPUT_VALUE, value_and_type.value

    if value_and_type.type is not FiMimeTypeValues.TEXT:
        print(f"Yielding non-default mime type: {value_and_type.type}")
        yield SpanAttributes.INPUT_MIME_TYPE, value_and_type.type.value


def _as_output_attributes(
    value_and_type: Optional[_ValueAndType],
) -> Iterator[Tuple[str, AttributeValue]]:
    print(f"Processing output attributes for value_and_type: {value_and_type}")
    if not value_and_type:
        print("No value_and_type provided, returning empty iterator")
        return

    print(f"Yielding output value: {value_and_type.value[:100]}... (truncated)")
    yield SpanAttributes.OUTPUT_VALUE, value_and_type.value

    if value_and_type.type is not FiMimeTypeValues.TEXT:
        print(f"Yielding non-default mime type: {value_and_type.type}")
        yield SpanAttributes.OUTPUT_MIME_TYPE, value_and_type.type.value
