from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_payload():
    return {
        "membershipId": "5~186103331+10+7+20240101+793854+8A+829",
        "zipCode": "85305",
        "benefitProductType": "Medical",
        "languageCode": "11",
        "service": {
            "code": "99214",
            "type": "CPT4",
            "description": "Adult Office visit Age 30-39",
            "supportingService": {"code": "470", "type": "DRG"},
            "modifier": {"modifierCode": "E1"},
            "diagnosisCode": "F33 40",
            "placeOfService": {"code": "11"}
        },
        "providerInfo": [
            {
                "serviceLocation": "000761071",
                "providerType": "HO",
                "specialty": {"code": "91017"},
                "taxIdentificationNumber": "0000431173518",
                "taxIdQualifier": "SN",
                "providerNetworks": {"networkID": "58921"},
                "providerIdentificationNumber": "0004000317",
                "nationalProviderIdentifier": {"nationalProviderId": "1386660504"},
                "providerNetworkParticipation": {"providerTier": "1"}
            }
        ]
    }


def test_estimate_cost_success():
    response = client.post("/estimate-cost", json=get_payload())
    assert response.status_code == 200
    assert "status" in response.json()


def test_estimate_cost_missing_field():
    bad_payload = get_payload()
    del bad_payload["zipCode"]

    response = client.post("/estimate-cost", json=bad_payload)
    assert response.status_code == 400  # because you implemented 400 on validation errors
    assert response.json()["errors"][0]["field"] == "zipCode"
