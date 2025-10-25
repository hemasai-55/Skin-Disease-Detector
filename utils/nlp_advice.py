care_tips = {
    "Acne": "Keep your skin clean, avoid oily cosmetics, and consult a dermatologist for medications.",
    "Eczema": "Use mild soaps, moisturize often, avoid scratching, and consult a doctor if it worsens.",
    "Psoriasis": "Use medicated creams, avoid triggers, and get regular dermatology check-ups.",
    "Rosacea": "Avoid spicy foods/alcohol, protect skin from sun, consult dermatologist for treatment.",
    "Normal": "Maintain a healthy skincare routine with cleansing and moisturizing."
}

def get_care_tip(condition):
    return care_tips.get(condition, "Consult a dermatologist for advice.")
