# Jacob Coomer
# This program queries open-notify for the current ISS location.
# After comparing to user data, the program sends an email to the user when the ISS
# is visible in the sky. 
import requests
import json
import sys
import os
from datetime import datetime
import smtplib
import time


def LocInfo():
    userLat = input("Enter your latitude: ")
    userLong = input("Enter your longitude: ")
    return [float(userLat), float(userLong)]


def ISSInfo():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    issLat = float(data["iss_position"]["latitude"])
    issLong = float(data["iss_position"]["longitude"])
    issCord = [issLat, issLong]
    return issCord


def Track(u, i):
    if (i[0] - 5 <= u[0] <= i[0] + 5) and (i[1] - 5 <= u[1] <= i[1] + 5):
        return True
    else:
        return False


def Night(u):
    parameters = {
        "lat": u[0],
        "lng": u[1],
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sunData = response.json()

    sunrise = int(sunData["results"]["sunrise".split("T")[1].split(":")[0]])
    sunset = int(sunData["results"]["sunset".split("T")[1].split(":")[0]])
    currentH = datetime.now().hour

    if currentH >= sunset or currentH <= sunrise:
        return True
    else:
        return False



if __name__ == '__main__':
    userCords = LocInfo()
    issCords = ISSInfo()

    with open(os.path.join(sys.path[0], "config.txt"), "r") as f:
        info = f.read()
        info = info.split(" ")


    MY_EMAIL = info[1]
    MY_PASSWORD = info[3]

    print(MY_EMAIL + MY_PASSWORD)

    recentMail = False
    while(True):

        print("Checking for ISS overhead -- " + str(datetime.now()))
        if Track(userCords, issCords) and Night(userCords):
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject: ISS Flyover\n\nThe ISS is above you in the sky."
            )
            recentMail = True
            print("ISS Overhead. Email sent.")
        else:
            print("No ISS Overhead. Current Pos:\nLat= " + str(issCords[0]) + " Long= " + str(issCords[1]))


        if (recentMail):
            time.sleep(21600)
            recentMail = False
        else:
            time.sleep(360)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
