import requests
from api_gateway.application.ports.http_port import HTTPClientPort
from api_gateway.application.dtos import ProxyRequestDTO, ProxyResponseDTO
from api_gateway.infrastructure.config import settings

class HTTPClient(HTTPClientPort):
    def request(self, req: ProxyRequestDTO) -> ProxyResponseDTO:
        # Собираем URL
        url = settings.FILE_SERVICE_URL.rstrip("/") + "/" + req.path.lstrip("/")
        # Делаем запрос
        resp = requests.request(
            method=req.method,
            url=url,
            headers=req.headers,
            data=req.content
        )
        # Возвращаем DTO с результатом
        return ProxyResponseDTO(
            status_code=resp.status_code,
            headers=dict(resp.headers),
            content=resp.content
        )

