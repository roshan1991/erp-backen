import requests
from typing import Dict, Any, List, Optional
from app.core.config import settings


class FacebookClient:
    """Client for Facebook and Instagram Graph API"""
    
    def __init__(self):
        self.access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
        self.page_id = settings.FACEBOOK_PAGE_ID
        self.instagram_account_id = settings.INSTAGRAM_ACCOUNT_ID
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to Facebook Graph API"""
        if params is None:
            params = {}
        
        params["access_token"] = self.access_token
        
        url = f"{self.base_url}/{endpoint}"
        
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, params=params, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    # Campaign APIs
    def get_campaigns(self, limit: int = 25) -> Dict[str, Any]:
        """Get ad campaigns"""
        return self._make_request(
            f"{self.page_id}/campaigns",
            params={"limit": limit, "fields": "id,name,status,objective,created_time"}
        )
    
    def get_campaign_insights(self, campaign_id: str, date_preset: str = "last_7d") -> Dict[str, Any]:
        """Get campaign insights/analytics"""
        return self._make_request(
            f"{campaign_id}/insights",
            params={
                "date_preset": date_preset,
                "fields": "impressions,reach,clicks,spend,cpc,cpm,ctr"
            }
        )
    
    # Facebook Messenger APIs
    def get_conversations(self, limit: int = 25) -> Dict[str, Any]:
        """Get page conversations"""
        return self._make_request(
            f"{self.page_id}/conversations",
            params={"limit": limit, "fields": "id,participants,updated_time,message_count"}
        )
    
    def get_conversation_messages(self, conversation_id: str, limit: int = 25) -> Dict[str, Any]:
        """Get messages in a conversation"""
        return self._make_request(
            f"{conversation_id}/messages",
            params={"limit": limit, "fields": "id,from,to,message,created_time"}
        )
    
    def send_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
        """Send message via Facebook Messenger"""
        return self._make_request(
            f"{self.page_id}/messages",
            method="POST",
            data={
                "recipient": {"id": recipient_id},
                "message": {"text": message_text}
            }
        )
    
    # Instagram APIs
    def get_instagram_messages(self, limit: int = 25) -> Dict[str, Any]:
        """Get Instagram direct messages"""
        return self._make_request(
            f"{self.instagram_account_id}/conversations",
            params={"limit": limit, "fields": "id,participants,updated_time,message_count"}
        )
    
    def get_instagram_conversation_messages(self, conversation_id: str, limit: int = 25) -> Dict[str, Any]:
        """Get messages in an Instagram conversation"""
        return self._make_request(
            f"{conversation_id}/messages",
            params={"limit": limit, "fields": "id,from,to,message,created_time"}
        )
    
    def send_instagram_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
        """Send Instagram direct message"""
        return self._make_request(
            f"{self.instagram_account_id}/messages",
            method="POST",
            data={
                "recipient": {"id": recipient_id},
                "message": {"text": message_text}
            }
        )
    
    # Analytics
    def get_page_insights(self, metrics: List[str], period: str = "day") -> Dict[str, Any]:
        """Get page insights"""
        return self._make_request(
            f"{self.page_id}/insights",
            params={
                "metric": ",".join(metrics),
                "period": period
            }
        )
