from fastapi import FastAPI, Request
from routers import auth_router, product_router, cart_router, order_router
from database.database import engine, Base
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(title="E-Commerce API")

# Set up session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Create database tables
Base.metadata.create_all(bind=engine)

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
