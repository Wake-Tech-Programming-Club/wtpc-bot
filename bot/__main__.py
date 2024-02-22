import dotenv
import os
from . import bot


dotenv.load_dotenv()


bot.run(os.environ["API_KEY"])
