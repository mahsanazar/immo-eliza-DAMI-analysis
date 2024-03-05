# URL = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page=1"
URL = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false"
HEADERS = {
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    "user-agent": "Mozilla/5.0  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

ATTRIBUTES_MAP = {
    "id": ["id"],
    "region": ["property", "location", "region"],
    # "regionCode": ["property", "location", "regionCode"],
    "province": ["property", "location", "province"],
    "district": ["property", "location", "district"],
    "locality": ["property", "location", "locality"],
    "postalcode": ["property", "location", "postalCode"],
    "latitude": ["property", "location", "latitude"],
    "longitude": ["property", "location", "longitude"],
    # "street": ["property", "location", "street"],
    # "number": ["property", "location", "number"],
    "price_main": ["price", "mainValue"],
    "type": ["property", "type"],
    "subtype": ["property", "subtype"],
    "heatingType": ["property", "energy", "heatingType"],
    "cadastralIncome": ["transaction", "sale", "cadastralIncome"],
    # "typeSale": ["transaction", "type"],
    "epcScores": ["transaction", "certificates", "epcScore"],
    "primaryEnergyConsumption": [
        "transaction",
        "certificates",
        "primaryEnergyConsumptionPerSqm",
    ],
    "bedrooms": ["property", "bedroomCount"],
    # "livingRoom": ["property", "livingRoom"],
    "surface": ["property", "netHabitableSurface"],
    "surfaceGood": ["property", "land", "surface"],
    "hasGasWaterElectricityConnection": [
        "property",
        "land",
        "hasGasWaterElectricityConnection",
    ],
    "condition": ["property", "building", "condition"],
    "facadeCount": ["property", "building", "facadeCount"],
    "hasKitchenSetup": ["property", "kitchen", "type"],
    "isFurnished": ["transaction", "sale", "isFurnished"],
    "fireplaceExists": ["property", "fireplaceExists"],
    "hasSwimmingPool": ["property", "hasSwimmingPool"],
    "terraceSurface": ["property", "terraceSurface"],
    "floodZone": ["property", "constructionPermit", "floodZoneType"],
    "gardenSurface": ["property", "gardenSurface"],
    # "customerId": ["customers", "id"],
    # "customerType": ["customers", "type"],
    # "customerName": ["customers", "name"],
    "isNewRealEstateProject": ["flags", "isNewRealEstateProject"],
}
