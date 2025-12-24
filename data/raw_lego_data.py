# Simulating the structured data an employee would "select"
def get_selected_trip_data():
    return {
        "meta": {
            "client_name": "The Anderson Family",
            "destination": "Amalfi Coast, Italy",
            "vibe": "Luxury & Relaxation",  # The AI uses this for tone
            "start_date": "2024-06-10"
        },
        "itinerary": [
            {
                "day": 1,
                "focus": "Arrival",
                # The "Lego Brick" for Hotel
                "stay": {
                    "name": "Le Sirenuse",
                    "stars": 5,
                    "amenities": ["Infinity Pool", "Michelin Dining", "Sea View"],
                    "location": "Positano"
                },
                # The "Lego Brick" for Transport
                "transfer": "Private Mercedes S-Class from Naples Airport"
            },
            {
                "day": 2,
                "focus": "Culture",
                # The "Lego Brick" for Activity
                "activities": [
                    {
                        "name": "Private Boat Tour to Capri",
                        "duration": "6 Hours",
                        "notes": "Includes Blue Grotto swim stop"
                    }
                ],
                 "stay": {
                    "name": "Le Sirenuse",
                    "location": "Positano"
                }
            }
        ]
    }
