from aiogram import Router

from . import callbacks, commands

def setup_router()->Router:
    router = Router()
    router.include_router(commands.router)
    router.include_router(callbacks.router)
    return router