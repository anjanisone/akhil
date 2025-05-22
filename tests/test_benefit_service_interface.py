import pytest
from unittest.mock import create_autospec, MagicMock
from app.services.benefit_service import (
    BenefitRequest,
    BenefitResponse,
    BenefitServiceInterface
)

# Abstract Behavior


def test_interface_is_abstract():
    with pytest.raises(TypeError):
        BenefitServiceInterface()


def test_subclass_without_implementation_fails():
    class IncompleteService(BenefitServiceInterface):
        pass

    with pytest.raises(TypeError):
        IncompleteService()


def test_subclass_with_implementation_succeeds():
    class ConcreteBenefitService(BenefitServiceInterface):
        def get_benefit(self, request: BenefitRequest) -> BenefitResponse:
            return BenefitResponse()

    service = ConcreteBenefitService()
    result = service.get_benefit(BenefitRequest())
    assert isinstance(result, BenefitResponse)


# Mock-Based Testing


def test_mocked_interface_behavior():
    mock_service = create_autospec(BenefitServiceInterface, instance=True)
    mock_response = BenefitResponse()
    mock_service.get_benefit.return_value = mock_response

    request = BenefitRequest()
    response = mock_service.get_benefit(request)

    mock_service.get_benefit.assert_called_once_with(request)
    assert isinstance(response, BenefitResponse)


def test_mock_used_in_application_logic():
    def app_logic(service: BenefitServiceInterface, request: BenefitRequest) -> BenefitResponse:
        return service.get_benefit(request)

    mock_service = MagicMock(spec=BenefitServiceInterface)
    mock_service.get_benefit.return_value = BenefitResponse()

    req = BenefitRequest()
    res = app_logic(mock_service, req)

    mock_service.get_benefit.assert_called_once()
    assert isinstance(res, BenefitResponse)
