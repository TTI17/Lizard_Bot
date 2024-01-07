from dispatcher import *
from aiogram import executor
from content_types import *

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= False)