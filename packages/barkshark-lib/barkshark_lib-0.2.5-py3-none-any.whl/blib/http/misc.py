from __future__ import annotations

import enum

from asyncio import StreamReader
from collections.abc import Iterator, Mapping
from socket import socket
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
	try:
		from typing import Self

	except ImportError:
		from typing_extensions import Self


class HttpMessageType(enum.Enum):
	REQUEST = enum.auto()
	RESPONSE = enum.auto()


class ReadState(enum.Enum):
	START = enum.auto()
	HEADERS = enum.auto()
	BODY = enum.auto()


class Headers(dict[str, list[str]]):
	def __init__(self, data: Mapping[str, list[str] | str] | None = None) -> None:
		dict.__init__(self)

		if data:
			self.update(data)


	def __getitem__(self, key: str) -> list[str]:
		if not (value := dict.__getitem__(self, key.title())):
			dict.__delitem__(self, key.title())
			raise KeyError(key)

		return value


	def __setitem__(self, key: str, value: list[str] | str) -> None:
		key = key.title()

		if isinstance(value, list):
			dict.__setitem__(self, key, value)
			return

		dict.__setitem__(self, key, [value])


	def __delitem__(self, key: str) -> None:
		dict.__delitem__(self, key.title())


	def __contains__(self, key: str) -> bool: # type: ignore[override]
		# dafuq mypy!?
		return dict.__contains__(self, key.title()) # type: ignore[operator]


	def append(self, key: str, value: str) -> None:
		self[key] = value


	def copy(self) -> Headers:
		headers = Headers()

		for key, value in self.items():
			headers.append(key, value)

		return headers


	def get(self, key: str, default: list[str] | None) -> list[str]: # type: ignore[override]
		try:
			return self[key.title()]

		except KeyError:
			if default is None:
				raise

			return default


	def get_one(self, key: str, default: str | None = None) -> str:
		try:
			return self[key.title()][-1]

		except IndexError:
			del self[key.title()]

			if default is None:
				raise KeyError(key) from None

		except KeyError:
			if default is None:
				raise

		return default


	def items(self) -> Iterator[tuple[str, str]]: # type: ignore[override]
		for key in self:
			for value in self[key]:
				yield key, value


	def pop(self, key: str, default: list[str] | None = None) -> list[str]: # type: ignore[override]
		if default is None:
			return dict.pop(self, key.title())

		return dict.pop(self, key.title(), default)


	def pop_one(self, key: str, default: str | None = None) -> str:
		key = key.title()

		try:
			value = self[key].pop(-1)

			if len(self[key]) < 1:
				del self[key]

			return value

		except KeyError:
			if default is None:
				raise

		except IndexError:
			del self[key]

			if default is None:
				raise

		return default


	def remove(self, key: str) -> None:
		del self[key]


	def remove_one(self, key: str) -> None:
		items = self[key.title()]

		if len(items) <= 1:
			del self[key.title()]

		else:
			del items[-1]


	def set(self, key: str, value: str) -> None:
		self[key.title()] = [value]


	def update(self, data: Mapping[str, list[str] | str]) -> None: # type: ignore[override]
		for key, value in data.items():
			key = key.title()

			if isinstance(value, list):
				dict.__setitem__(self, key, self.get(key, []) + value)

			else:
				self[key] = value


	def values(self) -> Iterator[str]: # type: ignore[override]
		for key in self:
			for value in self[key]:
				yield value


class HttpParser:
	def __init__(self) -> None:
		self.message_type: HttpMessageType = HttpMessageType.REQUEST
		self.state: ReadState = ReadState.START
		self.start_line: str = ""
		self.method: str = ""
		self.path: str = ""
		self.version: str = ""
		self.status: int = 0
		self.reason: str = ""
		self.headers: Headers = Headers()
		self.body: bytes = b""


	def __repr__(self) -> str:
		items: dict[str, Any] = {}

		if self.message_type == HttpMessageType.REQUEST:
			items["method"] = self.method
			items["path"] = self.path
			items["version"] = self.version

		else:
			items["version"] = self.version
			items["status"] = self.status
			items["reason"] = self.reason

		items["headers"] = self.headers
		item_string = ", ".join(f"{key}={repr(value)}" for key, value in items.items())
		return f"HttpParser({self.message_type}, {item_string})"


	@classmethod
	async def from_reader(cls: type[Self], reader: StreamReader) -> Self:
		parser = cls()
		parser.feed((await reader.readuntil(b"\r\n\r\n")))
		return parser


	# broken on ssl sockets for some reason
	@classmethod
	def from_socket(cls: type[Self], sock: socket) -> Self:
		sockfile = sock.makefile("rb")
		parser = cls()

		try:
			while (parser.state != ReadState.BODY):
				parser.feed(sockfile.readline())

		finally:
			sockfile.close()

		return parser


	def feed(self, data: bytes) -> None:
		if self.state == ReadState.START:
			line_bytes, _, data = data.partition(b"\r\n")

			if (line := line_bytes.decode("ascii")).startswith("HTTP"):
				self.message_type = HttpMessageType.RESPONSE

				version, status, reason = line.split(" ", 2)

				self.status = int(status)
				self.reason = reason

			else:
				self.message_type = HttpMessageType.REQUEST

				method, path, version = line.split()

				self.method = method
				self.path = path

			self.version = version.split("/", 1)[1]
			self.start_line += line

			if data:
				self.state = ReadState.HEADERS
				self.feed(data)

		elif self.state == ReadState.HEADERS:
			lines = data.split(b"\r\n")

			for index, line_bytes in enumerate(lines):
				if not line_bytes:
					self.state = ReadState.BODY

					if index + 1 < len(lines):
						self.feed(b"\r\n".join(lines[index + 1:]))

					return

				key, value = line_bytes.decode("ascii").split(": ")
				self.headers.append(key, value)

		elif self.state == ReadState.BODY:
			self.body += data
