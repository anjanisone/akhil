from typing import List, Optional
from pydantic import BaseModel, Field, constr
from typing import Annotated


class SupportingService(BaseModel):
    code: Annotated[str, Field(..., json_schema_extra={"examples": ["99214"]}, min_length=1)]
    type: Annotated[str, Field(..., json_schema_extra={"examples": ["CPT4"]}, min_length=1)]


class Modifier(BaseModel):
    modifierCode: Annotated[str, Field(..., json_schema_extra={"examples": ["E1"]}, min_length=1)]


class PlaceOfService(BaseModel):
    code: Annotated[str, Field(..., json_schema_extra={"examples": ["11"]}, min_length=1)]


class Specialty(BaseModel):
    code: Annotated[str, Field(..., json_schema_extra={"examples": ["91017"]}, min_length=1)]


class ProviderNetworks(BaseModel):
    networkID: Annotated[str, Field(..., json_schema_extra={"examples": ["58921"]}, min_length=1)]


class NationalProviderIdentifier(BaseModel):
    nationalProviderId: Annotated[str, Field(..., json_schema_extra={"examples": ["1386660504"]}, min_length=1)]


class ProviderNetworkParticipation(BaseModel):
    providerTier: Annotated[str, Field(..., json_schema_extra={"examples": ["1"]}, min_length=1)]


class ProviderInfo(BaseModel):
    serviceLocation: Annotated[str, Field(..., json_schema_extra={"examples": ["000761071"]}, min_length=1)]
    providerType: Annotated[str, Field(..., json_schema_extra={"examples": ["HO"]}, min_length=1)]
    specialty: Specialty
    taxIdentificationNumber: Annotated[str, Field(..., json_schema_extra={"examples": ["0000431173518"]}, min_length=1)]
    taxIdQualifier: Annotated[str, Field(..., json_schema_extra={"examples": ["SN"]}, min_length=1)]
    providerNetworks: ProviderNetworks
    providerIdentificationNumber: Annotated[str, Field(..., json_schema_extra={"examples": ["0004000317"]}, min_length=1)]
    nationalProviderIdentifier: NationalProviderIdentifier
    providerNetworkParticipation: ProviderNetworkParticipation


class Service(BaseModel):
    code: Annotated[str, Field(..., json_schema_extra={"examples": ["99214"]}, min_length=1)]
    type: Annotated[str, Field(..., json_schema_extra={"examples": ["CPT4"]}, min_length=1)]
    description: Annotated[str, Field(..., json_schema_extra={"examples": ["Adult Office visit Age 30-39"]}, min_length=1)]
    supportingService: SupportingService
    modifier: Modifier
    diagnosisCode: Annotated[str, Field(..., json_schema_extra={"examples": ["F33 40"]}, min_length=1)]
    placeOfService: PlaceOfService


class CostEstimatorRequest(BaseModel):
    membershipId: Annotated[str, Field(..., json_schema_extra={"examples": ["5~186103331+10+7+20240101+793854+8A+829"]}, min_length=1)]
    zipCode: Annotated[str, Field(..., json_schema_extra={"examples": ["85305"]}, min_length=1)]
    benefitProductType: Annotated[str, Field(..., json_schema_extra={"examples": ["Medical"]}, min_length=1)]
    languageCode: str = Field(..., json_schema_extra={"examples": ["11"]})
    service: Service
    providerInfo: List[ProviderInfo]