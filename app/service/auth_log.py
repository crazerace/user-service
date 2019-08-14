# Standard library
from typing import Tuple

# 3rd party libraries
from crazerace.http.instrumentation import trace

# Internal modules
from app.models import AuthEvent
from app.models.dto import ClientInfo
from app.repository import auth_event_repo


@trace("auth_log")
def record_login(user_id: str, client: ClientInfo, success: bool=True) -> None:
    event = AuthEvent(
        user_id=user_id, 
        client_id = client.id, 
        ip_address=client.ip_address, 
        event_type="LOGIN", 
        succeeded=success
    )
    auth_event_repo.save(event)


@trace("auth_log")
def record_signup(user_id: str, client: ClientInfo) -> None:
    event = AuthEvent(
        user_id=user_id, 
        client_id = client.id, 
        ip_address=client.ip_address, 
        event_type="SIGN_UP"
    )
    auth_event_repo.save(event)