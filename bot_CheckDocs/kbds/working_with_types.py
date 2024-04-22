from aiogram.types import CallbackQuery


def getting_the_message_object(request):
    return request.message if isinstance(request, CallbackQuery) else request
