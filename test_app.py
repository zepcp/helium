from typing import Dict

from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from database.database import Database
from apis.authentication import get_token


client = TestClient(app)
basic_threshold = 0.001
api_threshold = 1


@fixture(scope="session")
def headers() -> Dict[str, str]:
    user = Database().get_user("admin")
    token = get_token(user).get("access_token")
    return {"Authorization": "Bearer {}".format(token)}


def test_status():
    result = client.get("http://localhost:8000/status")
    assert result.status_code == 200
    assert result.json() == {"status": "OK"}
    assert float(result.headers.get('x-process-time')) < basic_threshold


def test_swagger():
    result = client.get("http://localhost:8000/docs")
    assert result.status_code == 200
    assert float(result.headers.get('x-process-time')) < basic_threshold


def test_unauthorized():
    for url in ["http://localhost:8000/coingecko/prices",
                "http://localhost:8000/helium/price",
                "http://localhost:8000/helium/balance/test",
                "http://localhost:8000/helium/reward/test"]:
        result = client.get(url)
        assert result.status_code == 401
        assert float(result.headers.get('x-process-time')) < api_threshold


def test_coingecko(headers: Dict[str, str]):
    result = client.get("http://localhost:8000/coingecko/prices", headers=headers)
    assert result.status_code == 200
    assert float(result.headers.get('x-process-time')) < api_threshold
    assert result.json().get("price")


def test_helium(headers: Dict[str, str]):
    result = client.get("http://localhost:8000/helium/price", headers=headers)
    assert result.status_code == 200
    assert float(result.headers.get('x-process-time')) < api_threshold
    assert result.json().get("price")

    result = client.get("http://localhost:8000/helium/balance/test", headers=headers)
    assert result.status_code == 200
    assert float(result.headers.get('x-process-time')) < api_threshold
    assert result.json().get("wallet").get("owner") == "test"
    assert result.json().get("wallet").get("address") is None
    assert result.json().get("balance") == 0

    result = client.get("http://localhost:8000/helium/reward/test",
                        params={"min_time": "2020-01-01", "max_time": "2020-01-02"}, headers=headers)
    assert result.status_code == 200
    assert float(result.headers.get('x-process-time')) < api_threshold
    assert result.json().get("hotspot").get("owner") == "test"
    assert result.json().get("hotspot").get("address") is None
    assert result.json().get("reward").get("total") == 0
    assert result.json().get("reward").get("referral") == 0
    assert result.json().get("reward").get("owner") == 0
