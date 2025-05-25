from api_gateway.application.ports.http_port import HTTPClientPort
from api_gateway.application.dtos import ProxyRequestDTO, ProxyResponseDTO

class ProxyRequest:
    def __init__(self, client: HTTPClientPort):
        self.client = client

    def execute(self, req: ProxyRequestDTO) -> ProxyResponseDTO:
        return self.client.request(req)
