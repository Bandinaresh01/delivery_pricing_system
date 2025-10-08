import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def test_missing_fields():
    async with httpx.AsyncClient() as client:
        payload = {
            # Missing material_type
            "urgency": "express",
            "weight": 5,
            "location_type": "urban",
            "origin": "New York, NY",
            "destination": "Los Angeles, CA"
        }
        response = await client.post(f"{BASE_URL}/calculate_price", json=payload)
        print("Missing Fields Response:", response.status_code, response.json())

async def test_invalid_urgency():
    async with httpx.AsyncClient() as client:
        payload = {
            "material_type": "fragile",
            "urgency": "invalid-urgency",
            "weight": 5,
            "location_type": "urban",
            "origin": "New York, NY",
            "destination": "Los Angeles, CA"
        }
        response = await client.post(f"{BASE_URL}/calculate_price", json=payload)
        print("Invalid Urgency Response:", response.status_code, response.json())

async def test_escalation_trigger():
    async with httpx.AsyncClient() as client:
        # Provide invalid origin to trigger distance calculation failure
        payload = {
            "material_type": "fragile",
            "urgency": "express",
            "weight": 5,
            "location_type": "urban",
            "origin": "Invalid Origin",
            "destination": "Los Angeles, CA"
        }
        response = await client.post(f"{BASE_URL}/calculate_price", json=payload)
        print("Escalation Trigger Response:", response.status_code, response.json())

async def main():
    await test_missing_fields()
    await test_invalid_urgency()
    await test_escalation_trigger()

if __name__ == "__main__":
    asyncio.run(main())
