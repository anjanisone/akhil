# rate queries
RATE_QUERIES = {
    "get_standard_rate": """
        SELECT RATE, SERVICE_CD, PROVIDER_BUSINESS_GROUP_NBR,
               PLACE_OF_SERVICE_CD, PRODUCT_CD
        FROM cet_rates
        WHERE service_cd = :service_cd
          AND provider_business_group_nbr = :provider_business_group_nbr
          AND place_of_service_cd = :place_of_service_cd
          AND product_cd = :product_cd
    """,

    "get_standard_rate_without_pbg": """
        SELECT MAX(rate)
        FROM cet_rates
        WHERE service_cd = :service_cd
          AND service_type_cd = :service_type_cd
          AND rate_system_cd = 'REF'
          AND product_cd = :product_cd
          AND geographic_area_cd = :geographic_area_cd
          AND place_of_service_cd = :place_of_service_cd
          AND contract_type = 'S'
    """,

    "get_out_of_network_rate": """
        SELECT RATE, SERVICE_CD, PROVIDER_BUSINESS_GROUP_NBR,
               PLACE_OF_SERVICE_CD, PRODUCT_CD
        FROM cet_out_of_network_rates
        WHERE service_cd = :service_cd
          AND provider_business_group_nbr = :provider_business_group_nbr
          AND place_of_service_cd = :place_of_service_cd
          AND product_cd = :product_cd
    """,

    "get_claim_based_rate": """
        SELECT AVG(AMOUNT) AS RATE
        FROM claims
        WHERE service_cd = :service_cd
          AND provider_business_group_nbr = :provider_business_group_nbr
          AND date_of_service >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
        GROUP BY service_cd, provider_business_group_nbr
    """,

    "get_non_standard_rate": """
        SELECT RATE, SERVICE_CD, PROVIDER_BUSINESS_GROUP_NBR,
               PLACE_OF_SERVICE_CD, PRODUCT_CD
        FROM cet_rates
        WHERE service_cd = :service_cd
          AND provider_business_group_nbr = :provider_business_group_nbr
          AND place_of_service_cd = :place_of_service_cd
          AND product_cd = :product_cd
    """,

    "get_max_claim_rate": """
        SELECT 
            MAX(c.rate) AS RATE
        FROM 
            anbc-hcb-dev.prv_ps_ce_dec_hcb_dev.CET_CLAIM_BASED_AMOUNTS c
        WHERE 
            c.PROVIDER_IDENTIFICATION_NBR = :provider_identification_nbr
            AND c.NETWORK_ID = :network_id
            AND c.SERVICE_LOCATION_NBR = :service_location_nbr
            AND c.PLACE_OF_SERVICE_CD = :place_of_service_cd
            AND c.SERVICE_CD = :service_cd
            AND c.SERVICE_TYPE_CD = :service_type_cd
    """,

    "get_provider_info": """
        SELECT DISTINCT 
            PROVIDER_BUSINESS_GROUP_NBR,
            PRODUCT_CD,
            RATING_SYSTEM_CD,
            PROVIDER_BUSINESS_GROUP_NBR,
            EPDB_GEOGRAPHIC_AREA_CD
        FROM 
            anbc-hcb-dev.prv_ps_ce_dec_hcb_dev.CET_PROVIDERS p
        WHERE 
            p.PROVIDER_IDENTIFICATION_NBR = :provider_identification_nbr
            AND p.SERVICE_LOCATION_NBR = :service_location_nbr
            AND p.NETWORK_ID = :network_id
    """
}
