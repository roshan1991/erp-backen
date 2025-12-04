import requests
from typing import Dict, Any, Optional
from app.core.config import settings


class WhatsAppClient:
    """Client for WhatsApp Business API"""
    
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.business_account_id = settings.WHATSAPP_BUSINESS_ACCOUNT_ID
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to WhatsApp Business API"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """Send text message"""
        return self._make_request(
            f"{self.phone_number_id}/messages",
            method="POST",
            data={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message}
            }
        )
    
    def send_template_message(self, to: str, template_name: str, language_code: str = "en") -> Dict[str, Any]:
        """Send template message"""
        return self._make_request(
            f"{self.phone_number_id}/messages",
            method="POST",
            data={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": language_code}
                }
            }
        )
    
    def send_media_message(self, to: str, media_type: str, media_id: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Send media message (image, video, document, audio)"""
        media_data = {"id": media_id}
        if caption:
            media_data["caption"] = caption
        
        return self._make_request(
            f"{self.phone_number_id}/messages",
            method="POST",
            data={
                "messaging_product": "whatsapp",
                "to": to,
                "type": media_type,
                media_type: media_data
            }
        )
    
    def mark_message_as_read(self, message_id: str) -> Dict[str, Any]:
        """Mark message as read"""
        return self._make_request(
            f"{self.phone_number_id}/messages",
            method="POST",
            data={
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": message_id
            }
        )
    
    def get_message_templates(self) -> Dict[str, Any]:
        """Get message templates"""
        return self._make_request(
            f"{self.business_account_id}/message_templates",
            params={"limit": 100}
        )
    
    def upload_media(self, file_path: str, media_type: str) -> Dict[str, Any]:
        """Upload media file"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = requests.post(
                f"{self.base_url}/{self.phone_number_id}/media",
                headers=headers,
                files=files,
                data={"messaging_product": "whatsapp", "type": media_type}
            )
            response.raise_for_status()
            return response.json()
