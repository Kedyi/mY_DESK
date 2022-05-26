import pandas as pd
from mY_DESK.settings import *


## update the login list along with the face-id and the username.
def call():
    a = pd.read_csv(str(BASE_DIR) +r"\Dashboard\Loginlist.csv")
    a.to_html(str(BASE_DIR) +r"\Dashboard\templates\output.html")

