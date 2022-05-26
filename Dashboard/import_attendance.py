import pandas as pd
from mY_DESK.settings import *

# export the attendance tracked during the login to the page

def create_attendance():
    a = pd.read_csv(str(BASE_DIR) + r"\Dashboard\PresentList.csv")
    a.to_html(str(BASE_DIR) + r"\Dashboard\templates\Attendance.html")

