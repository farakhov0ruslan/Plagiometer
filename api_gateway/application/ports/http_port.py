from abc import ABC, abstractmethod
from api_gateway.application.dtos import ProxyRequestDTO, ProxyResponseDTO


class HTTPClientPort(ABC):
    @abstractmethod
    def request(self, req: ProxyRequestDTO) -> ProxyResponseDTO:
        """Выполнить HTTP-запрос к downstream-сервису."""
        ...
