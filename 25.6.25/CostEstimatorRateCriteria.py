from dataclasses import dataclass
from typing import Optional

@dataclass
class CostEstimatorRateCriteria:
    """
    A data class representing the criteria used for cost estimation calculations.

    Attributes:
        providerIdentificationNumber: Unique ID of the provider
        serviceLocationNumber: Location number where service is provided
        networkId: Network identifier
        serviceCode: The service code identifier
        serviceType: Type of service being provided
        placeOfServiceCode: Code representing the place of service
        zipCode: ZIP code of the service location
    """
    service_cd: str
    product_cd: str
    place_of_service_cd: str
    provider_business_group_nbr: Optional[str]
    geographic_area_cd: Optional[str]
    service_type_cd: Optional[str]
    provider_identification_nbr: Optional[str]
    network_id: Optional[str]
    service_location_nbr: Optional[str]
