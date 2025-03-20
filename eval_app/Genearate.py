from rest_framework.views import APIView
from rest_framework.response import Response
from threading import Thread, Event
import random
import time
from .models import Business

# Sample data
names = ["Company A", "Company B", "Company C", "Company D", "Company E"]
countries = ["USA", "Canada", "Germany", "India", "Australia"]

# Global variables for controlling the script
data_injection_thread = None
stop_event = Event()

def generate_data():
    """Generate random company data."""
    data = []
    for i in range(5):
        name = names[i]
        revenue = round(random.uniform(1000, 10000), 2)
        profit = round(random.uniform(100, 5000), 2)
        employees = round(random.uniform(10, 500), 2)
        country = random.choice(countries)
        data.append((name, revenue, profit, employees, country))
    return data

def inject_data(stop_event):
    """
    Inject data into the database every 60 seconds until stopped.
    Args:
        stop_event: threading.Event object to signal when to stop.
    """
    while not stop_event.is_set():
        data = generate_data()  # Generate random data
        for row in data:
            Business.objects.create(
                name=row[0],
                revenue=row[1],
                profit=row[2],
                employees=row[3],
                country=row[4],
            )
        time.sleep(60)