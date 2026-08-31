import pulumi
from pulumi.dynamic import ResourceProvider, Resource, CreateResult, UpdateResult
import requests

class NetBoxResourceProvider(ResourceProvider):
    def __init__(self, endpoint_path: str):
        self.endpoint_path = endpoint_path

    def _get_headers(self):
        config = pulumi.Config()
        token = config.get_secret("netbox_token") or config.get("netbox_token")
        return {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _get_url(self):
        config = pulumi.Config()
        base_url = config.get("netbox_url").rstrip("/")
        return f"{base_url}/api/{self.endpoint_path.strip('/')}/"

    def create(self, props):
        url = self._get_url()
        headers = self._get_headers()
        payload = {k: v for k, v in props.items() if not k.startswith("__")}
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code not in (200, 201):
            raise Exception(f"NetBox API Error [{response.status_code}]: {response.text}")
        
        data = response.json()
        return CreateResult(id_=str(data["id"]), outs={**props, "id": str(data["id"])})

    def delete(self, id_, props):
        url = f"{self._get_url()}{id_}/"
        headers = self._get_headers()
        requests.delete(url, headers=headers)

class NetBoxResource(Resource):
    def __init__(self, name: str, endpoint: str, props: dict, opts=None):
        super().__init__(NetBoxResourceProvider(endpoint), name, props, opts)