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
        # Try max claim-based rate first
        claim_result = await self._get_max_claim_based_rate(rate_criteria)
        if claim_result and len(claim_result) > 0 and claim_result[0].get("RATE") is not None:
            return float(claim_result[0]["RATE"])

        # Try non-standard rate
        provider_params = {
            "provider_identification_nbr": rate_criteria.providerIdentificationNumber,
            "service_location_nbr": rate_criteria.serviceLocationNumber,
            "network_id": rate_criteria.networkId
        }

        non_standard_result = await self._get_non_standard_rate(provider_params)
        if non_standard_result and len(non_standard_result) > 0 and non_standard_result[0].get("RATE") is not None:
            return float(non_standard_result[0]["RATE"])

        # Try standard rate with/without PBG
        if rate_criteria.providerBusinessGroupNumber:
            standard_result = await self._get_standard_rate_with_pbg(rate_criteria)
        else:
            standard_result = await self._get_standard_rate_without_pbg(rate_criteria)

        if standard_result and len(standard_result) > 0 and standard_result[0].get("RATE") is not None:
            return float(standard_result[0]["RATE"])

        # Default fallback
        return 100.0

    async def _get_max_claim_based_rate(self, criteria):
        query = RATE_QUERIES.get("get_max_claim_rate")
        params = {
            "provider_identification_nbr": criteria.providerIdentificationNumber,
            "network_id": criteria.networkId,
            "service_location_nbr": criteria.serviceLocationNumber,
            "place_of_service_cd": criteria.placeOfServiceCode,
            "service_cd": criteria.serviceCode,
            "service_type_cd": criteria.serviceType
        }
        return await self.db.execute_query(query, params)

    async def _get_non_standard_rate(self, params):
        query = RATE_QUERIES.get("get_non_standard_rate")
        return await self.db.execute_query(query, params)

    async def _get_standard_rate_with_pbg(self, criteria):
        query = RATE_QUERIES.get("get_standard_rate")
        params = {
            "service_cd": criteria.serviceCode,
            "provider_business_group_nbr": criteria.providerBusinessGroupNumber,
            "place_of_service_cd": criteria.placeOfServiceCode,
            "product_cd": criteria.productCode
        }
        return await self.db.execute_query(query, params)

    async def _get_standard_rate_without_pbg(self, criteria):
        query = RATE_QUERIES.get("get_standard_rate_without_pbg")
        params = {
            "service_cd": criteria.serviceCode,
            "service_type_cd": criteria.serviceType,
            "product_cd": criteria.productCode,
            "geographic_area_cd": criteria.geographicAreaCode,
            "place_of_service_cd": criteria.placeOfServiceCode
        }
        return await self.db.execute_query(query, params)

    async def get_provider_info(self, rate_criteria: CostEstimatorRateCriteria) -> dict:
        """
        Retrieve provider information based on the provided criteria.
        """
        params = {
            "provider_identification_nbr": rate_criteria.providerIdentificationNumber,
            "service_location_nbr": rate_criteria.serviceLocationNumber,
            "network_id": rate_criteria.networkId
        }

        query = RATE_QUERIES.get("get_provider_info")
        result = await self.db.execute_query(query, params)
        
        return result[0] if result and len(result) > 0 else {}
