import uuid


def get_uuid_str(data):
    try:
        uuid_obj = uuid.UUID(data)
    except:
        return None
    return uuid_obj
