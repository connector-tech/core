import uuid

from fastapi import UploadFile

from code.clients.boto3 import S3
from code.models import User


class MediaService:
    @staticmethod
    async def upload_user_photos(user_id: str, files: list[UploadFile]):
        user_photos = []

        for file in files:
            file_format = file.filename.split('.')[-1]
            file_name = f'{uuid.uuid4()}.{file_format}'
            file_path = await S3.upload_image(user_id, file_name, file.file)

            user_photos.append(file_path)

        user = await User.filter(id=user_id).first()

        if user.photos is not None:
            user.photos.extend(user_photos)
        else:
            user.photos = user_photos

        await user.save(update_fields=['photos'])
        await user.refresh_from_db()

        return user.photos
