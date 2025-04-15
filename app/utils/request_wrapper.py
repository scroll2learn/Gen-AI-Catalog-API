import httpx
from app.exceptions import APIException

class RequestWrapper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def call_api(self, endpoint, method="get", data=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        headers = headers or self.headers
        print(url)
        if method.lower() == "get":
            response = await self.client.get(url, headers=headers)
        elif method.lower() == "post":
            response = await self.client.post(url, json=data, headers=headers)
        elif method.lower() == "put":
            response = await self.client.put(url, json=data, headers=headers)
        elif method.lower() == "delete":
            response = await self.client.delete(url, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method.")
        if response.status_code == 400:
            raise APIException(
                context={
                    "status_code": response.status_code,
                    "message": response.message,
                    "API_ERROR": response.error_code,
                }
            )
        if response.status_code != 200:
            raise Exception(f"API call failed with status code: {response.status_code}")
        return response.json()

    async def close(self):
        await self.client.aclose()
