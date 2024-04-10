import uuid

from fastapi import UploadFile

from code.models import User


class MediaService:
    @staticmethod
    async def upload_user_photos(user_id, files: list[UploadFile]):
        user_photos = []

        for file in files:
            file_format = file.filename.split('.')[-1]
            file_name = f'{uuid.uuid4()}.{file_format}'
            with open(f'./media/{file_name}', 'wb') as buffer:
                buffer.write(file.file.read())

            user_photos.append(file_name)

        user = await User.filter(id=user_id).first()

        if user.photos is not None:
            user.photos.extend(user_photos)
        else:
            user.photos = user_photos

        await user.save(update_fields=['photos'])
        await user.refresh_from_db()

        return user.photos
