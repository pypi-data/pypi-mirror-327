from typing import Any

from .misc import Headers

from ..date import HttpDate
from ..enums import HttpMethod, HttpStatus
from ..misc import convert_to_bytes
from ..transport import AsyncTransport
from ..url import Url


class MessageBase:
	headers: Headers

	_transport: AsyncTransport
	_body: bytes


	def __getitem__(self, key: str) -> str:
		return self.headers.get_one(key)


	def __setitem__(self, key: str, value: str | int | HttpDate) -> None:
		if not isinstance(value, str):
			value = str(value)

		self.headers.set(key, value)


	def __delitem__(self, key: str) -> None:
		del self.headers[key]


	@property
	def accept(self) -> str:
		return self.headers.get_one("Accept", "")


	@accept.setter
	def accept(self, value: str) -> None:
		self.headers.set("Accept", value)


	@property
	def content_length(self) -> int:
		return int(self.headers.get_one("Content-Length", "0"))


	@content_length.setter
	def content_length(self, value: int) -> None:
		self.headers.set("Content-Length", str(value))


	@property
	def content_type(self) -> str:
		return self.headers.get_one("Content-Type", "")


	@content_type.setter
	def content_type(self, value: str) -> None:
		self.headers.set("Content-Type", value)


class Request(MessageBase):
	_transport: AsyncTransport
	_body: bytes


	def __init__(self,
				url: Url | str,
				method: HttpMethod | str = HttpMethod.GET,
				body: Any = None,
				headers: Headers | dict[str, str] | None = None) -> None:

		if isinstance(headers, dict):
			headers = Headers(headers)

		self.url: Url = Url.parse(url)
		self.method: HttpMethod = HttpMethod.parse(method)
		self.headers: Headers = headers or Headers()
		self.body = body

		self["Host"] = self.url.hostname
		self["Date"] = HttpDate.new_utc().to_string()


	@property
	def body(self) -> bytes:
		return self._body


	@body.setter
	def body(self, data: Any) -> None:
		self._body = convert_to_bytes(data)
		self.content_length = len(self.body)


class Response(MessageBase):
	_transport: AsyncTransport


	def __init__(self,
				body: bytes = b"",
				status: HttpStatus | int = HttpStatus.Ok,
				headers: Headers | dict[str, str] | None = None) -> None:

		if isinstance(headers, dict):
			headers = Headers(headers)

		self.status: HttpStatus = HttpStatus.parse(status)
		self.headers: Headers = headers or Headers()
		self.reason: str = ""
		self.body = body


	@property
	def body(self) -> bytes:
		return self._body


	@body.setter
	def body(self, data: Any) -> None:
		self._body = convert_to_bytes(data)
		self.content_length = len(self.body)


	async def read(self) -> bytes:
		print("content-length:", self.content_length)
		if not self.content_length:
			return b""

		if len(self.body) < self.content_length:
			self.body += await self._transport.read(self.content_length - len(self.body))

		return self.body
