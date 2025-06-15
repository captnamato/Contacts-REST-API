"""
Сервіс для роботи з Cloudinary
"""
import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


async def upload_avatar(file: UploadFile, user_id: int) -> str:
    """Завантаження аватара користувача"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Файл повинен бути зображенням")
    if file.size and file.size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Файл занадто великий (макс. 5MB)")
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder="contacts_api/avatars",
            public_id=f"user_{user_id}",
            overwrite=True,
            format="jpg",
            width=300,
            height=300,
            crop="fill"
        )
        return result.get('secure_url')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка завантаження: {str(e)}")


def delete_avatar(public_id: str):
    """Видалення аватара"""
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass
