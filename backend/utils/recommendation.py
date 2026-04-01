def get_recommendation(skin_type):

    if skin_type == "Oily":
        return [
            "Use oil control face wash",
            "Apply gel-based moisturizer",
            "Use sunscreen SPF 50"
        ]

    elif skin_type == "Dry":
        return [
            "Use hydrating cleanser",
            "Apply heavy moisturizer",
            "Drink more water"
        ]

    elif skin_type == "Normal":
        return [
            "Maintain a balanced skincare routine",
            "Use mild face wash",
            "Apply sunscreen daily"
        ]

    else:
        return [
            "Consult dermatologist",
            "Use gentle skincare products"
        ]