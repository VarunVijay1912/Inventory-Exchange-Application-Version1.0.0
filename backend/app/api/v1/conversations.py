"""Enhanced conversations and messaging API"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.core.exceptions import NotFoundError, ForbiddenError
from app.schemas.conversation import Conversation, ConversationCreate, Message, MessageCreate
from app.services.conversation_service import ConversationService
from app.models.user import User
from app.core.logging import logger

router = APIRouter()


@router.post("/", response_model=Conversation, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_create: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Start a new conversation about a product
    
    **Requires:** Authenticated user
    **Note:** Returns existing conversation if already exists
    """
    try:
        conversation = ConversationService.create_conversation(
            db,
            conversation_create,
            current_user.id
        )
        
        if not conversation:
            raise NotFoundError("Product not found")
        
        logger.info(f"Conversation created/retrieved: {conversation.id}")
        return conversation
        
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Conversation creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation"
        )


@router.get("/", response_model=List[Conversation])
async def list_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all user's conversations
    
    **Requires:** Authenticated user
    **Returns:** Conversations where user is buyer or seller
    """
    try:
        conversations = ConversationService.get_user_conversations(db, current_user.id)
        logger.info(f"Retrieved {len(conversations)} conversations for user {current_user.id}")
        return conversations
        
    except Exception as e:
        logger.error(f"Conversations retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get conversation details with messages
    
    **Requires:** Participant in conversation
    **Note:** Marks messages as read automatically
    """
    try:
        conversation = ConversationService.get_conversation(db, conversation_id, current_user.id)
        
        if not conversation:
            raise NotFoundError("Conversation not found")
        
        # Mark messages as read
        ConversationService.mark_messages_as_read(db, conversation_id, current_user.id)
        
        logger.info(f"Conversation retrieved: {conversation_id}")
        return conversation
        
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Conversation retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation"
        )


@router.post("/{conversation_id}/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def send_message(
    conversation_id: UUID,
    message_create: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Send a message in conversation
    
    **Requires:** Participant in conversation
    **Supports:** text, contact_share, offer message types
    """
    try:
        message = ConversationService.send_message(
            db,
            conversation_id,
            current_user.id,
            message_create
        )
        
        if not message:
            raise ForbiddenError("Not authorized to send message in this conversation")
        
        logger.info(f"Message sent in conversation {conversation_id}")
        return message
        
    except ForbiddenError:
        raise
    except Exception as e:
        logger.error(f"Message sending error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
        )