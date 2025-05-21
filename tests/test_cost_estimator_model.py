import pytest
from pydantic import ValidationError
from app.schemas.cost_estimator_request import CostEstimatorRequest


def get_valid_input():
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


def test_model_valid_input():
    data = get_valid_input()
    model = CostEstimatorRequest(**data)
    assert model.membershipId.startswith("5~")
    assert model.providerInfo[0].specialty.code == "91017"


def test_model_missing_required_field():
    data = get_valid_input()
    del data["membershipId"]

    with pytest.raises(ValidationError) as exc_info:
        CostEstimatorRequest(**data)
    assert "membershipId" in str(exc_info.value)


def test_model_invalid_nested_field_type():
    data = get_valid_input()
    data["service"]["supportingService"]["code"] = 470  # Should be str

    with pytest.raises(ValidationError) as exc_info:
        CostEstimatorRequest(**data)
    assert "supportingService.code" in str(exc_info.value)
