import io

from aioboto3 import Session


class S3:
    _instance = None

    _bucket_name = None

    @classmethod
    async def connect(cls, access_key_id: str, secret_access_key: str, bucket_name: str, region: str):
        if cls._instance is None:
            session = Session(
                region_name=region,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
            )

            cls._instance = await session.client('s3').__aenter__()

            cls._bucket_name = bucket_name

        return cls._instance

    @classmethod
    async def upload_image(cls, user_id: str, image_name: str, image: io.BytesIO) -> str:
        image_path = '/'.join(['users', user_id, image_name])

        try:
            await cls._instance.upload_fileobj(image, cls._bucket_name, image_path)
        except Exception as e:
            raise e

        return f'/users/{user_id}/{image_name}'

    @classmethod
    async def disconnect(cls):
        if cls._instance is not None:
            await cls._instance.__aexit__(None, None, None)

            cls._instance = None
            cls._bucket_name = None
