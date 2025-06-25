from dataclasses import dataclass

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
    providerIdentificationNumber: str
    serviceLocationNumber: str
    networkId: str
    serviceCode: str
    serviceType: str
    placeOfServiceCode: str
    zipCode: str
