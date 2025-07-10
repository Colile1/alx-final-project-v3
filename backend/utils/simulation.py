# Simulated plant data generation
import random
from datetime import datetime

def generate_reading(garden_settings):
    # ...simulate moisture, temperature, light, etc...
    return {
        'moisture_level': random.uniform(30, 90),
        'temperature': random.uniform(18, 30),
        'light_intensity': random.uniform(200, 1000),
        'timestamp': datetime.utcnow().isoformat()
    }
