transportation_emission_factors = {
    "Two-wheeler": 0.6,
    "Public Transport": 0.4,
    "Bicycle": 0.0,
    "Walking": 0.0,
    "Car": {
        "Petrol": {
            "Two-seater": 2.5,
            "Regular": 2.0,
            "SUV": 2.8,
            "Minivan": 2.4,
        },
        "Diesel": {
            "Two-seater": 2.0,
            "Regular": 1.6,
            "SUV": 2.2,
            "Minivan": 1.8,
        },
        "Electric": {
            "Two-seater": 0.0,
            "Regular": 0.0,
            "SUV": 0.0,
            "Minivan": 0.0,
        },
    }
}


electricity_emission_factors={
    "Less than average": 0.3,
    "Average": 0.5,
    "More than average": 0.7
}

diet_emission_factors = {
    "Rarely or Never": 0.1,
    "Occasionally": 0.3,
    "Regularly": 0.5,
    "Frequently": 0.7
}

clothing_emission_factors = {
    "fast_fashion": {
        "Yes": 1.0,  # Example emission factor for buying fast fashion items
        "No": 0.5,   # Example emission factor for not buying fast fashion items
    },
    "sustainability": 0.3,
    "budget": 0.7,
    "brand_reputation": 0.5,
    "material_quality": 0.4,
    "style": 0.6,
    "purchase_frequency": {
        "Rarely or Never": 0.2,
        "Occasionally": 0.4,
        "Regularly": 0.6,
        "Frequently": 0.8,
    }
}

# constants.py
housing_emission_factors = {
    "heating_source": {
        "Electricity": 0.5,
        "Natural Gas": 0.8,
        "Oil": 1.0,
        "Other": 0.7,
    },
    "heating_usage": {
        "Low": 0.3,
        "Moderate": 0.6,
        "High": 1.0,
    },
    "electrical_appliances_usage": {
        "Low": 0.5,
        "Moderate": 0.8,
        "High": 1.2,
    }
}

