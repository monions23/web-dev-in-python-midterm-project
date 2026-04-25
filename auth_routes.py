from typing import Annotated

from fastapi import APIRouter, HTTPException, logger, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.authenticate import authenticate
from users import User
from auth.hash_password import verify_password
from auth.jwt_handler import TokenData, create_access_token, verify_access_token

from auth.hash_password import hash_password, verify_password
from database import Database
from users import User, TokenResponse


auth_router = APIRouter()

user_database = Database(User)


@auth_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    db_user = await User.find_one(User.email == user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already.",
        )
    hashed_password = hash_password(user.password)
    user.password = str(hashed_password, "utf-8")
    await user_database.save(user)
    return {"message": "User created successfully"}


@auth_router.post("/sign-in", response_model=TokenResponse)
async def sign_in(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:

    db_user = await User.find_one(User.email == user.username)

    if not db_user or not db_user.active:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, expiry = create_access_token(
        {"username": db_user.email}
    )

    return TokenResponse(
        username=db_user.email,
        access_token=access_token,
        expiry=expiry,
    )

@auth_router.get("/me")
async def get_me(
    current_user: Annotated[TokenData, Depends(authenticate)],
) -> TokenData:
    return current_user
