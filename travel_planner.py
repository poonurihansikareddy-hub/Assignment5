TOURIST_PLACES_KB = {

    "Paris": {
        "country": "France",
        "category": ["art", "history", "romance"],
        "attractions": [
            "Eiffel Tower",
            "Louvre Museum",
            "Notre Dame Cathedral",
            "Champs-Elysees",
            "Versailles"
        ],
        "best_season": "Spring"
    },

    "Kyoto": {
        "country": "Japan",
        "category": ["culture", "history", "nature"],
        "attractions": [
            "Fushimi Inari Shrine",
            "Arashiyama Bamboo Grove",
            "Kinkakuji Temple",
            "Gion District"
        ],
        "best_season": "Autumn"
    },

    "Goa": {
        "country": "India",
        "category": ["beach", "relaxation", "nightlife"],
        "attractions": [
            "Baga Beach",
            "Dudhsagar Falls",
            "Old Goa Churches",
            "Anjuna Market"
        ],
        "best_season": "Winter"
    },

    "Tuscany": {
        "country": "Italy",
        "category": ["wine", "art", "history"],
        "attractions": [
            "Florence",
            "Siena",
            "Chianti Wine Region",
            "Pisa"
        ],
        "best_season": "Spring"
    }
}


FOOD_KB = {

    "Paris": [
        "Croissants",
        "Macarons",
        "French Onion Soup"
    ],

    "Kyoto": [
        "Ramen",
        "Matcha Desserts",
        "Tofu Dishes"
    ],

    "Goa": [
        "Fish Curry Rice",
        "Prawn Balchao",
        "Bebinca"
    ],

    "Tuscany": [
        "Pasta",
        "Bistecca Fiorentina",
        "Pecorino Cheese"
    ]
}


WINE_KB = {

    "Paris": [
        "Champagne",
        "Bordeaux"
    ],

    "Kyoto": [
        "Sake"
    ],

    "Goa": [
        "Feni"
    ],

    "Tuscany": [
        "Chianti",
        "Brunello"
    ]
}


COST_KB = {

    "Paris": {
        "budget": 80,
        "mid": 180,
        "luxury": 400
    },

    "Kyoto": {
        "budget": 60,
        "mid": 130,
        "luxury": 350
    },

    "Goa": {
        "budget": 30,
        "mid": 70,
        "luxury": 200
    },

    "Tuscany": {
        "budget": 70,
        "mid": 150,
        "luxury": 380
    }
}


INTEREST_MATCH_KB = {

    "art": ["Paris", "Tuscany"],
    "history": ["Paris", "Kyoto", "Tuscany"],
    "nature": ["Kyoto", "Goa"],
    "beach": ["Goa"],
    "food": ["Kyoto", "Paris"],
    "wine": ["Tuscany", "Paris"],
    "culture": ["Kyoto", "Paris"],
    "relaxation": ["Goa"]
}


def recommend_destinations(interests):

    scores = {}

    for interest in interests:

        for dest in INTEREST_MATCH_KB.get(interest.lower(), []):

            scores[dest] = scores.get(dest, 0) + 1

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [dest for dest, _ in ranked]


def build_itinerary(destination, days):

    info = TOURIST_PLACES_KB.get(destination)

    if not info:
        return []

    attractions = info["attractions"]

    itinerary = []

    per_day = max(1, len(attractions) // days)

    for day in range(1, days + 1):

        start = (day - 1) * per_day

        end = start + per_day

        places = attractions[start:end]

        if not places:
            places = ["Free exploration"]

        itinerary.append((day, places))

    return itinerary


def estimate_cost(destination, days, budget_level="mid"):

    costs = COST_KB.get(destination, {})

    daily = costs.get(budget_level, 100)

    return daily * days


def generate_travel_plan(
    user_name,
    interests,
    destination,
    days,
    budget_level="mid"
):

    print("=" * 50)
    print(f"TRAVEL PLAN FOR {user_name.upper()}")
    print("=" * 50)

    recommended = recommend_destinations(interests)

    print("\nRecommended destinations:")
    print(", ".join(recommended[:3]))

    if destination not in TOURIST_PLACES_KB:

        print(f"\n{destination} not found.")
        print(f"Using {recommended[0]} instead.")

        destination = recommended[0]

    info = TOURIST_PLACES_KB[destination]

    print(f"\nDestination: {destination}")
    print(f"Country: {info['country']}")
    print(f"Best season: {info['best_season']}")

    print(f"\n--- {days}-Day Itinerary ---")

    itinerary = build_itinerary(destination, days)

    for day, places in itinerary:

        print(f"Day {day}: {', '.join(places)}")

    print("\n--- Foods ---")

    for food in FOOD_KB.get(destination, []):

        print(f"• {food}")

    print("\n--- Drinks ---")

    for wine in WINE_KB.get(destination, []):

        print(f"• {wine}")

    total_cost = estimate_cost(
        destination,
        days,
        budget_level
    )

    print(f"\nEstimated Cost: ${total_cost}")

    print("\nHave a wonderful trip!\n")

    return {
        "destination": destination,
        "days": days,
        "cost": total_cost
    }


def test_travel_planner():

    print("\n===== TEST 1 =====\n")

    plan = generate_travel_plan(
        user_name="Alice",
        interests=["art", "wine", "history"],
        destination="Tuscany",
        days=5,
        budget_level="mid"
    )

    assert plan["destination"] == "Tuscany"

    print("TEST 1 PASS\n")

    print("\n===== TEST 2 =====\n")

    plan = generate_travel_plan(
        user_name="Bob",
        interests=["beach", "relaxation"],
        destination="Goa",
        days=4,
        budget_level="budget"
    )

    assert plan["destination"] == "Goa"

    print("TEST 2 PASS\n")

    print("\n===== TEST 3 =====\n")

    plan = generate_travel_plan(
        user_name="Carol",
        interests=["culture", "history"],
        destination="Unknown",
        days=3,
        budget_level="luxury"
    )

    print("TEST 3 PASS\n")


if __name__ == "__main__":

    test_travel_planner()

    print("All Travel Planner tests passed!")