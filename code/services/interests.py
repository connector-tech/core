from code.models import Interest


async def get_interests():
    interests = await Interest.all()
    return [
        {
            'id': str(interest.id),
            'name': interest.name,
        }
        for interest in interests
    ]
