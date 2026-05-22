import logging
import requests

logger = logging.getLogger(__name__)

def validate(medication_data):
    medication_name = medication_data['name']
    
    params = {
        "search": f'openfda.brand_name:"{medication_name}"',
        "limit": 1
    }
    
    response = requests.get("https://api.fda.gov/drug/label.json", params=params, timeout=5)
    
    print(response.url)
    print(response.status_code)
    
    data = response.json()
    results = data.get("results", [])
    
    logger.debug("\t API query: %s", response.url)

    if response.status_code == 200 and len(results) != 0:
        medication_name_valid = True
    elif response.status_code == 404 and data.get("error", {}).get("code") == "NOT_FOUND":
        logger.warning("\t Medication name not found: %s", medication_name)
        medication_name_valid = False
    else:
        logger.warning("\t API request failed with status code: %d", response.status_code)
        medication_name_valid = False

    if medication_name_valid:
        need = results[0]
        #medication_data['active_ingredient'] = "Hydrochlorothiazide"
        medication_data['instructions_of_use'] = need.get('indications_and_usage', [None])[0]
        medication_data['warnings'] = need.get('warnings', [None])[0]
        medication_data['overdose'] = (
            need.get('overdosage', [None])[0] or
            need.get('overdose', [None])[0] or  
            None
        )

        print("valid med")
        return medication_data
    else:
        print("med doesn't exist")


import requests

import re
import urllib.request
import urllib.parse
import json

import re

def get_active_ingredients(drug_name: str) -> list[str]:
    try:
        # drugs.json
        res = requests.get("https://rxnav.nlm.nih.gov/REST/drugs.json", params={"name": drug_name})
        res.raise_for_status()
        data = res.json()

        rxcui = None
        first_name = None
        for group in data.get("drugGroup", {}).get("conceptGroup", []):
            props = group.get("conceptProperties", [])
            if props:
                rxcui = props[0]["rxcui"]
                first_name = props[0]["name"] 
                break

        if not rxcui:
            print(f"No RXCUI found for: {drug_name}")
            return []

        # Try allrelated.json with tty=IN
        ingredients_res = requests.get(f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/allrelated.json")
        ingredients_res.raise_for_status()
        ingredients_data = ingredients_res.json()

        concept_groups = ingredients_data.get("allRelatedGroup", {}).get("conceptGroup", [])
        ingredients = [
            prop["name"].lower()
            for group in concept_groups
            if group.get("tty") == "IN"
            for prop in group.get("conceptProperties", [])
        ]

        # parse ingredient names from the drug name string
        if not ingredients and first_name:
            raw = re.sub(r'\[.*?\]', '', first_name)
            raw = re.sub(r'\b\d+(\.\d+)?\s*(MG|ML|MCG|%)\b', '', raw, flags=re.IGNORECASE)
            raw = re.sub(r'\b(oral|tablet|capsule|solution|suspension|extended|release|chewable|powder)\b', '', raw, flags=re.IGNORECASE)
            parts = [p.strip().lower() for p in raw.split('/') if p.strip()]
            ingredients = [p for p in parts if p]

        if not ingredients:
            print(f"No ingredients found for: {drug_name}")
            return []

        return ingredients

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
    
# test_drugs = [
#     "tylenol",
#     "lisinopril",
#     "metformin",
#     "percocet",
#     "augmentin",
#     "zestoretic",
#     "panadol"

# ]

# for drug in test_drugs:
#     result = get_active_ingredients(drug)
#     print(f"{drug}: {result}")