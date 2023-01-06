class ClientConfig:
    def __init__(self, base_url: str, timeout: int, api_key: str):
        self.base_url = base_url
        self.timeout = timeout
        self.api_key = api_key
