from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from app.core.firebase import get_db, get_current_user_id
from app.models.user_models import UserDB
from app.schemas.user import UserProfile
from typing import Optional, List

router = APIRouter(
    prefix="/users",
    tags=["사용자"],
    responses={404: {"description": "Not found"}},
)

# [프로필] 특정 사용자의 프로필 정보 조회
@router.get("/profile/{uid}", response_model=UserProfile, summary="사용자 프로필 조회")
async def get_user_profile(
    uid: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """특정 사용자의 프로필을 조회합니다."""
    user = db.query(UserDB).filter(UserDB.firebase_uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserProfile(
        uid=user.firebase_uid,
        nickname=user.name,
        bio=user.bio,
        profileImageUrl=user.profile_picture,
        likes=user.likes
    )

# [프로필] 프로필 정보 수정
@router.patch("/profile", response_model=UserProfile, summary="프로필 수정")
async def update_user_profile(
    update_data: dict = Body(...),
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """사용자의 bio 및 nickname 정보를 수정합니다."""
    user = db.query(UserDB).filter(UserDB.firebase_uid == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if "bio" in update_data:
        user.bio = update_data["bio"]
    if "nickname" in update_data:
        user.name = update_data["nickname"]

    db.commit()
    db.refresh(user)

    return UserProfile(
        uid=user.firebase_uid,
        nickname=user.name,
        bio=user.bio,
        profileImageUrl=user.profile_picture,
        likes=user.likes
    )

# [프로필] 전체 사용자 목록 조회
@router.get("/", response_model=List[UserProfile], summary="사용자 목록 조회")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """사용자 목록을 조회합니다."""
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return [
        UserProfile(
            uid=user.firebase_uid,
            nickname=user.name,
            bio=user.bio,
            profileImageUrl=user.profile_picture,
            likes=user.likes
        )
        for user in users
    ]