from dotenv import load_dotenv,dotenv_values
import os
load_dotenv()
conf = dotenv_values()
print(conf)