from app.repository.cost_estimator_repository import CostEstimatorRepositoryInterface
from app.database.spanner_client import SpannerClient
from app.config.database_config import spanner_config
from app.config.queries import RATE_QUERIES
from app.models.rate_criteria import CostEstimatorRateCriteria
from app.utils.logger import Logger

class CostEstimatorRepositoryImpl(CostEstimatorRepositoryInterface):
    def __init__(self):
        """Initialize repository with Spanner client."""
        if not spanner_config.is_valid():
            raise ValueError("Invalid Spanner configuration. Please check environment variables.")

        self.db = SpannerClient(
            project_id=spanner_config.project_id,
            instance_id=spanner_config.instance_id,
            database_id=spanner_config.database_id
        )

    async def get_rate(self, is_out_of_network: bool, rate_criteria: CostEstimatorRateCriteria, *args, **kwargs) -> float:
        """
        Retrieve the rate based on network status and criteria.
        """
        # Try claim-based rate first
        params = {
            "provider_identification_nbr": rate_criteria.providerIdentificationNumber,
            "service_location_nbr": rate_criteria.serviceLocationNumber,
            "network_id": rate_criteria.networkId,
            "place_of_service_cd": rate_criteria.placeOfServiceCode,
            "service_cd": rate_criteria.serviceCode,
            "service_type_cd": rate_criteria.serviceType
        }

        claim_result = await self._get_claim_based_rate(params)
        if claim_result and len(claim_result) > 0 and claim_result[0].get("RATE") is not None:
            return float(claim_result[0]["RATE"])

        # If not found, try non-standard rate (from provider)
        provider_params = {
            "provider_identification_nbr": rate_criteria.providerIdentificationNumber,
            "service_location_nbr": rate_criteria.serviceLocationNumber,
            "network_id": rate_criteria.networkId
        }

        non_standard_result = await self._get_non_standard_rate(provider_params)
        if non_standard_result and len(non_standard_result) > 0 and non_standard_result[0].get("RATE") is not None:
            return float(non_standard_result[0]["RATE"])

        # If still not found, try standard rate
        standard_result = await self._get_standard_rate(params)
        if standard_result and len(standard_result) > 0 and standard_result[0].get("RATE") is not None:
            return float(standard_result[0]["RATE"])

        # Default rate if all fails
        return 100.0

    async def _get_claim_based_rate(self, params):
        claim_query = RATE_QUERIES.get("get_claim_based_rate")
        return await self.db.execute_query(claim_query, params)

    async def _get_non_standard_rate(self, params):
        non_standard_query = RATE_QUERIES.get("get_non_standard_rate")
        return await self.db.execute_query(non_standard_query, params)

    async def _get_standard_rate(self, params):
        standard_query = RATE_QUERIES.get("get_standard_rate")
        return await self.db.execute_query(standard_query, params)
