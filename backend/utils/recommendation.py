# ======================================
# FACE RECOMMENDATION
# ======================================

def get_face_recommendation(issue, skin_type):

    rec = []

    # Issue-based
    if issue == "Acne":
        rec += [
            "Use salicylic acid face wash",
            "Avoid oily foods",
            "Do not touch your face"
        ]

    elif issue == "Pimple":
        rec += [
            "Apply benzoyl peroxide",
            "Keep skin clean",
            "Avoid popping pimples"
        ]

    elif issue == "Spots":
        rec += [
            "Use vitamin C serum",
            "Apply sunscreen daily"
        ]

    # Skin-type based
    if skin_type == "Oily":
        rec += ["Use oil-free moisturizer"]

    elif skin_type == "Dry":
        rec += [
            "Use hydrating cleanser",
            "Apply heavy moisturizer"
        ]

    elif skin_type == "Normal":
        rec += ["Maintain balanced skincare"]

    return rec


# ======================================
# HAIR RECOMMENDATION
# ======================================

def get_hair_recommendation(hair_type, frizz, damage, dandruff):

    rec = []

    if hair_type == "Oily":
        rec += ["Use mild shampoo regularly", "Avoid heavy oils"]

    elif hair_type == "Dry":
        rec += ["Use hydrating shampoo", "Apply hair oil weekly"]

    else:
        rec += ["Maintain regular hair care routine"]

    if frizz == "High":
        rec += ["Use anti-frizz serum", "Avoid heat styling"]

    if damage == "High":
        rec += ["Use protein hair mask", "Trim split ends"]

    if dandruff == "High":
        rec += ["Use anti-dandruff shampoo", "Keep scalp clean"]

    return rec


# ======================================
# SKIN (DISEASE) RECOMMENDATION
# ======================================

def get_skin_recommendation(condition):

    if condition == "Allergy":
        return ["Avoid allergens", "Use anti-allergic cream"]

    elif condition == "Infection":
        return ["Keep area clean", "Consult doctor if severe"]

    elif condition == "Normal":
        return ["Maintain hygiene", "Use moisturizer"]

    elif condition == "Rash":
        return ["Use soothing lotion", "Avoid heat exposure"]

    return ["Consult dermatologist"]