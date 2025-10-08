import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def test_calculate_price():
    async with httpx.AsyncClient() as client:
        payload = {
            "material_type": "fragile",
            "urgency": "express",
            "weight": 5,
            "location_type": "urban",
            "origin": "New York, NY",
            "destination": "Los Angeles, CA"
        }
        response = await client.post(f"{BASE_URL}/calculate_price", json=payload)
        print("Calculate Price Response:", response.status_code, response.json())

async def test_create_user():
    async with httpx.AsyncClient() as client:
        params = {
            "name": "Test User",
            "email": "testuser@example.com",
            "phone": "+1234567890"
        }
        response = await client.post(f"{BASE_URL}/users", params=params)
        print("Create User Response:", response.status_code, response.json())

async def main():
    await test_create_user()
    await test_calculate_price()

if __name__ == "__main__":
    asyncio.run(main())
