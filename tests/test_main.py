import pytest
from fastapi.testclient import TestClient
from app.main import app  # Make sure 'main.py' has your app instance named `app`

client = TestClient(app)

# ✅ Valid input payload (update as per your model)
valid_payload = {
    "membershipId": "5~186103331+10+7+20240101+793854+8A+829",
    "zipCode": "85305",
    "benefitProductType": "Medical",
    "languageCode": "11",
    "service": {
        "code": "99214",
        "type": "CPT4",
        "description": "Adult Office visit Age 30-39",
        "supportingService": { "code": "470", "type": "DRG" },
        "modifier": { "modifierCode": "E1" },
        "diagnosisCode": "F33 40",
        "placeOfService": { "code": "11" }
    },
    "providerInfo": [
        {
            "serviceLocation": "000761071",
            "providerType": "HO",
            "specialty": { "code": "91017" },
            "taxIdentificationNumber": "0000431173518",
            "taxIdQualifier": "SN",
            "providerNetworks": { "networkID": "58921" },
            "providerIdentificationNumber": "0004000317",
            "nationalProviderIdentifier": { "nationalProviderId": "1386660504" },
            "providerNetworkParticipation": { "providerTier": "1" }
        }
    ]
}


def test_valid_payload_returns_success():
    response = client.post("/membercost/v1/estimate/search/retrieve", json=valid_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_missing_field_returns_400():
    invalid_payload = valid_payload.copy()
    del invalid_payload["membershipId"]

    response = client.post("/membercost/v1/estimate/search/retrieve", json=invalid_payload)

    assert response.status_code == 400
    assert "errors" in response.json()
    assert "membershipId" in response.json()["errors"]
    assert response.json()["errors"]["membershipId"] == "field required"


def test_empty_field_returns_400():
    invalid_payload = valid_payload.copy()
    invalid_payload["service"]["code"] = ""  # Empty string to trigger min_length error

    response = client.post("/membercost/v1/estimate/search/retrieve", json=invalid_payload)

    assert response.status_code == 400
    assert "service.code" in response.json()["errors"]
    assert "at least" in response.json()["errors"]["service.code"].lower()
