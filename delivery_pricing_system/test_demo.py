import asyncio
from app.graph import compiled_graph

async def main():
    state = {
        "ticket_id": "D-101",
        "user_id": 1,
        "inputs": {
            "material_type": "fragile",
            "urgency": "express",
            "weight": 5,
            "location_type": "urban",
            "origin": "New York, NY",
            "destination": "Los Angeles, CA"
        },
        "price_attempts": 0,
        "action_log": []
    }
    result = await compiled_graph.ainvoke(state)
    print("Final State:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
