from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse
import jwt
from config import config
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/home")
async def home(request: Request):
    try:
        token = request.cookies.get("jwt_token")
        if not token:
            return RedirectResponse(url="/login")

        user_info = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])

        return templates.TemplateResponse("home.html", {"request": request, "user": user_info})

    except jwt.ExpiredSignatureError:
        return RedirectResponse(url="/login?error=expired")
    except jwt.InvalidTokenError:
        return RedirectResponse(url="/login?error=invalid")
    except Exception as e:
        print(f"Error loading home page: {e}")
        raise HTTPException(status_code=500, detail="Could not load home page")