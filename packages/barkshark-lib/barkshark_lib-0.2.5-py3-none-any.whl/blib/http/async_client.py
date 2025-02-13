import ssl

from .message import Request, Response
from .misc import Headers, HttpParser

from .. import __version__
from ..enums import HttpMethod
from ..transport import AsyncTransport
from ..url import Url


class HttpClient:
	def __init__(self,
				agent: str = f"BarksharkLib/{__version__}",
				headers: dict[str, str] | None = None,
				timeout: int = 10) -> None:

		self.headers: Headers = Headers(headers or {})
		self.timeout: int = timeout
		self.user_agent = agent

		self.headers.set("Accept-Encoding", "identity")
		self._context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)


	@property
	def user_agent(self) -> str:
		return self.headers.get_one("User-Agent", "")


	@user_agent.setter
	def user_agent(self, value: str) -> None:
		self.headers.set("User-Agent", value)


	async def request(self, method: HttpMethod | str, url: Url | str) -> Response:
		request = Request(url, method)
		return await self.send(request)


	async def send(self, request: Request) -> Response:
		if not request.url.port:
			port = 443 if request.url.proto == "https" else 80

		else:
			port = request.url.port

		transport = await AsyncTransport.new_client(request.url.domain, port, ssl = self._context)
		await transport.write(f"{request.method.value.upper()} {request.url.path} HTTP/1.1\r\n")

		for key, value in [*self.headers.items(), *request.headers.items()]:
			await transport.write(f"{key}: {value}\r\n")

		await transport.write("\r\n")
		await transport.write(request.body)

		parser = await HttpParser.from_reader(transport.reader)

		response = Response(parser.body, parser.status)
		response._transport = transport
		response.reason = parser.reason

		for key, value in parser.headers.items():
			response.headers.append(key, value)

		return response
