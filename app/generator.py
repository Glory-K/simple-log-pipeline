import random
import uuid
from datetime import datetime, timedelta

EVENT_TYPES = ["page_view", "purchase", "error"]
PAGE_URLS = ["/", "/products", "/cart", "/checkout", "/search", "/mypage"]
PRODUCT_IDS = ["P100", "P200", "P300", "P400", "P500"]
ERROR_CODES = ["E400", "E401", "E404", "E500"]

def generate_event() -> dict:
    event_type = random.choice(EVENT_TYPES)
    event_time = datetime.now()-timedelta(
        minutes=random.randint(0, 1440)
    )

    event = {
        "event_id":str(uuid.uuid4()),
        "user_id":random.randint(1,100),
        "event_type":event_type,
        "event_time":event_time,
        "page_url":random.choice(PAGE_URLS),
        "product_id":None,
        "amount":None,
        "error_code":None,
    }

    if event_type == "purchase":
        event["product_id"]= random.choice(PRODUCT_IDS)
        event["amount"]=round(random.uniform(10.0, 500.0), 2)
        
    if event_type == "error":
        event["error_code"] = random.choice(ERROR_CODES)

    return event

def generate_events(n: int = 1000) -> list[dict]:
    return [generate_event() for _ in range(n)]
