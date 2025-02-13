from collections.abc import Sequence
from typing import Generic, TypeVar

from ..models.content import Content
from ..models.messages import Message
from ..models.tools import ToolCall, ToolCallResult

BackendMessage = TypeVar("BackendMessage")


class MessageTransformer(Generic[BackendMessage]):
    """Transforms Pilgrim Message instances into backend-specific models."""

    def from_pilgrim(self, messages: Sequence[Message]) -> Sequence[BackendMessage]:
        return [self.transform_message_from_pilgrim(message) for message in messages]

    def from_backend(self, messages: Sequence[BackendMessage]) -> Sequence[Message]:
        return [self.transform_message_from_backend(message) for message in messages]

    def transform_message_from_pilgrim(self, message: Message) -> BackendMessage:
        raise NotImplementedError

    def transform_message_from_backend(self, message: BackendMessage) -> Message:
        raise NotImplementedError


BackendToolCall = TypeVar("BackendToolCall")


class ToolCallTransformer(Generic[BackendToolCall]):
    """Transforms Pilgrim ToolCall instances into backend-specific models."""

    def transform(self, tool_call: ToolCall) -> BackendToolCall:
        raise NotImplementedError


BackendToolCallResult = TypeVar("BackendToolCallResult")


class ToolCallResultTransformer(Generic[BackendToolCallResult]):
    """Transforms Pilgrim ToolCallResult instances into backend-specific models."""

    def transform(self, tool_call_result: ToolCallResult) -> BackendToolCallResult:
        raise NotImplementedError


BackendContent = TypeVar("BackendContent")


class ContentTransformer(Generic[BackendContent]):
    """Transforms Pilgrim Content instances into backend-specific models."""

    def from_pilgrim(self, content: Content) -> BackendContent:
        raise NotImplementedError

    def from_backend(self, content: BackendContent) -> Content:
        raise NotImplementedError
