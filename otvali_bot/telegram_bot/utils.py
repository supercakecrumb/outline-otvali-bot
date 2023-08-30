from models.client import get_client_by_tg_id


def admin_only(func):
    def wrapper(message):
        client = get_client_by_tg_id(message.from_user.id)
        if client is None or (not client.is_admin):
            return
        return func(message)

    return wrapper

