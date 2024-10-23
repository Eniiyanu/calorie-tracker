import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class NutritionixService:
    def __init__(self):
        self.api_key = settings.NUTRITIONIX_API_KEY
        self.app_id = settings.NUTRITIONIX_APP_ID
        self.base_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    def get_calories(self, description: str) -> int:
        headers = {
            "x-app-id": self.app_id,
            "x-app-key": self.api_key,
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                self.base_url,
                json={"query": description},
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return int(data['foods'][0]['nf_calories'])
        except Exception as e:
            logger.error(f"Nutritionix API error: {str(e)}")
            return None