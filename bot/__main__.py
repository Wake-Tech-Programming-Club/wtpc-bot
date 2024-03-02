import dotenv
import os
from . import client


dotenv.load_dotenv()


client.run(os.environ["API_KEY"])
