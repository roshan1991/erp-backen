from fastapi import APIRouter, HTTPException, Depends, Query, Request, Response
from typing import Optional, List
from datetime import datetime, timedelta
from app.integrations.facebook_client import FacebookClient
from app.integrations.whatsapp_client import WhatsAppClient
from app.api import deps
from app.core.config import settings

router = APIRouter()

def get_facebook_client():
    """Dependency to get Facebook API client"""
    return FacebookClient()

def get_whatsapp_client():
    """Dependency to get WhatsApp API client"""
    return WhatsAppClient()

# Campaign Endpoints
@router.get("/campaigns")
def get_campaigns(
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get Facebook/Instagram ad campaigns"""
    try:
        return client.get_campaigns(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaigns/{campaign_id}/insights")
def get_campaign_insights(
    campaign_id: str,
    date_preset: str = Query("last_7d", description="Date preset: today, yesterday, last_7d, last_30d"),
    client: FacebookClient = Depends(get_facebook_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get campaign insights/analytics"""
    try:
        return client.get_campaign_insights(campaign_id=campaign_id, date_preset=date_preset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Unified Inbox - Messages Endpoints
@router.get("/messages")
def get_all_messages(
    platform: Optional[str] = Query(None, description="Filter by platform: facebook, instagram, whatsapp"),
    limit: int = Query(25, ge=1, le=100),
    fb_client: FacebookClient = Depends(get_facebook_client),
    wa_client: WhatsAppClient = Depends(get_whatsapp_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get unified inbox messages from all platforms"""
    try:
        messages = []
        
        if platform is None or platform == "facebook":
            fb_conversations = fb_client.get_conversations(limit=limit)
            for conv in fb_conversations.get("data", []):
                conv["platform"] = "facebook"
                messages.append(conv)
        
        if platform is None or platform == "instagram":
            ig_conversations = fb_client.get_instagram_messages(limit=limit)
            for conv in ig_conversations.get("data", []):
                conv["platform"] = "instagram"
                messages.append(conv)
        
        # WhatsApp messages come via webhook, stored locally
        # For now, return empty list for WhatsApp
        if platform is None or platform == "whatsapp":
            # TODO: Implement local storage for WhatsApp messages
            pass
        
        # Sort by updated_time
        messages.sort(key=lambda x: x.get("updated_time", ""), reverse=True)
        
        return {"data": messages[:limit]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messages/{conversation_id}")
def get_conversation_messages(
    conversation_id: str,
    platform: str = Query(..., description="Platform: facebook, instagram, whatsapp"),
    limit: int = Query(25, ge=1, le=100),
    fb_client: FacebookClient = Depends(get_facebook_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get messages in a specific conversation"""
    try:
        if platform == "facebook":
            return fb_client.get_conversation_messages(conversation_id=conversation_id, limit=limit)
        elif platform == "instagram":
            return fb_client.get_instagram_conversation_messages(conversation_id=conversation_id, limit=limit)
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/messages/send")
def send_message(
    platform: str,
    recipient_id: str,
    message: str,
    fb_client: FacebookClient = Depends(get_facebook_client),
    wa_client: WhatsAppClient = Depends(get_whatsapp_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Send message to a recipient"""
    try:
        if platform == "facebook":
            return fb_client.send_message(recipient_id=recipient_id, message_text=message)
        elif platform == "instagram":
            return fb_client.send_instagram_message(recipient_id=recipient_id, message_text=message)
        elif platform == "whatsapp":
            return wa_client.send_text_message(to=recipient_id, message=message)
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WhatsApp Specific Endpoints
@router.get("/whatsapp/templates")
def get_whatsapp_templates(
    client: WhatsAppClient = Depends(get_whatsapp_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get WhatsApp message templates"""
    try:
        return client.get_message_templates()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/whatsapp/send-template")
def send_whatsapp_template(
    to: str,
    template_name: str,
    language_code: str = "en",
    client: WhatsAppClient = Depends(get_whatsapp_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Send WhatsApp template message"""
    try:
        return client.send_template_message(to=to, template_name=template_name, language_code=language_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Webhook Endpoints (for local development)
@router.get("/webhooks/facebook")
async def facebook_webhook_verify(request: Request):
    """Facebook webhook verification (GET)"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    else:
        raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/webhooks/facebook")
async def facebook_webhook_receive(request: Request):
    """Facebook webhook to receive messages (POST)"""
    try:
        body = await request.json()
        
        # Process webhook payload
        # Store messages in local database or cache
        # For now, just log it
        print("Facebook webhook received:", body)
        
        return {"status": "ok"}
    except Exception as e:
        print(f"Error processing Facebook webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/webhooks/whatsapp")
async def whatsapp_webhook_verify(request: Request):
    """WhatsApp webhook verification (GET)"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    else:
        raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/webhooks/whatsapp")
async def whatsapp_webhook_receive(request: Request):
    """WhatsApp webhook to receive messages (POST)"""
    try:
        body = await request.json()
        
        # Process webhook payload
        # Extract messages and store them
        # For now, just log it
        print("WhatsApp webhook received:", body)
        
        return {"status": "ok"}
    except Exception as e:
        print(f"Error processing WhatsApp webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Analytics Endpoints
@router.get("/analytics/overview")
def get_analytics_overview(
    client: FacebookClient = Depends(get_facebook_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get social media analytics overview"""
    try:
        metrics = ["page_impressions", "page_engaged_users", "page_post_engagements"]
        return client.get_page_insights(metrics=metrics, period="day")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
