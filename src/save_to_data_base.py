
from supabase import create_client, Client,PostgrestAPIError
import os
from dotenv import load_dotenv
from datetime import date
import re
from src.validation import get_active_ingredients
load_dotenv()

def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase credentials not found in environment variables.")
    return create_client(url, key)

def active_ingredient_ids(name: str) -> list[str]:
    ing = get_active_ingredients(name)
    print(ing)
    supabase = get_supabase_client()

    try:
        result = supabase.table("active_ingredients") \
        .select("id") \
        .in_("name", [i.capitalize() for i in ing]) \
        .execute()

        if not result.data:
            print(f"No ingredients found for: {name}")
            return []

        return [row['id'] for row in result.data]

    except PostgrestAPIError as e:
        print(f"Database API error: {e.message}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def insert_medication(data: dict):
    supabase = get_supabase_client()
    ingredient_ids=active_ingredient_ids(data['name'])
    try:
        # Insert medication and grab the new ID
        response = supabase.table("medication").insert(data).execute()
        medication_id = response.data[0]['id']

        # Build junction rows
        junction_rows = [
            {"id": medication_id, "active_ingredient": ing_id}
            for ing_id in ingredient_ids
        ]

        #Insert into junction table
        response2 = supabase.table("medication_active").insert(junction_rows).execute()

        print("Data sent successfully.")
        return response

    except PostgrestAPIError as e:
        print(f"Database API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    