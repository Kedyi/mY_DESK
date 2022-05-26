
from datetime import datetime
from mY_DESK import settings

# get the attendance of the employee using their face_id

def markAttendance(name):
      with open(str(settings.BASE_DIR) + r'\Dashboard\PresentList.csv','r+') as f:
          myDataList = f.readlines()
          nameList = []
          for line in myDataList:
              entry = line.split(',')
              nameList.append(entry[0])

          if name not in nameList:
              now = datetime.now()
              dtstring = now.strftime('%H:%M:%S')
              f.writelines(f'\n{name},{dtstring}')

# get the face_id and the username during login process

def login_list(name,face_id):
    with open(str(settings.BASE_DIR) + r'\Dashboard\Loginlist.csv', 'r+') as f1:
        myDataList = f1.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f1.writelines(f'\n{name},{face_id},{dtstring}')






