from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class WebhookPayload(BaseModel):
    # This structure depends on what Terra API sends.
    # We'll assume a generic structure for this example based on requirements.
    # "Health Data" payload.

    user_id: str # Terra User ID
    type: str # e.g. "HEART_RATE"
    data: List[dict] # The actual samples
    timestamp: datetime

    # Example generic structure to pass validation.
    # In a real scenario, this would be strictly typed against Terra's docs.

class HealthDataIngest(BaseModel):
    patient_id: int
    metric_type: str
    value: float
    timestamp: datetime
    source_device: str
