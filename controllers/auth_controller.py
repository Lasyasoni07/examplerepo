from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse
from services.auth_service import oauth
from config import config
import jwt
import secrets

router = APIRouter()

@router.get("/login")
async def login(request: Request):
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state 
    request.session["debug_test"] = "Session is working!"  
    print(f"[LOGIN] Stored state in session: {state}")  

    return await oauth.google.authorize_redirect(request, config.REDIRECT_URI, state=state)


@router.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        session_state = request.session.get("oauth_state")
        request_state = request.query_params.get("state")
        debug_value = request.session.get("debug_test") 

        print(f"[CALLBACK] Session state before auth: {session_state}")  
        print(f"[CALLBACK] Request state from Google: {request_state}")  
        print(f"[CALLBACK] Debug Test Value: {debug_value}") 

        if not session_state or session_state != request_state:
            raise HTTPException(status_code=400, detail="CSRF Warning! OAuth state does not match.")

        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)

        print("[CALLBACK] OAuth2 Token:", token) 
        print("[CALLBACK] User Info:", user_info) 
        jwt_token = jwt.encode(user_info, config.JWT_SECRET, algorithm="HS256")

        response = RedirectResponse(url="/home")
        response.set_cookie(key="jwt_token", value=jwt_token, httponly=True, samesite="Lax")

        return response

    except Exception as e:
        print(f"[CALLBACK] Error during OAuth callback: {e}") 
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")