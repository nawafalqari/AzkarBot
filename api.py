import requests
from datetime import datetime
from random import choice

def validateCountryCode(code: str):
   res = requests.get(f"https://api.worldbank.org/v2/country/{code}?format=json").json()
   if res[0].get("message", None) != None:
      return False, None

   return True, res[1][0].get("name")

def validateCity(country:str, city: str):
   return requests.get(f"https://api.aladhan.com/v1/timingsByCity?country={country}&city={city}&school=8").json().get("code", None) == 200

def getTime(country: str, city: str):
   timezone = requests.get(f"https://api.aladhan.com/v1/timingsByCity?country={country}&city={city}&school=8").json()["data"]["meta"]["timezone"]
   date = requests.get(f"https://api.aladhan.com/v1/currentDate?zone={timezone}").json()["data"]
   time = requests.get(f"https://api.aladhan.com/v1/currentTime?zone={timezone}").json()["data"]
   
   fullDate = f"{date} {time}"
   dt = extractDate(fullDate)

   return dt

def extractDate(string:str):
   date, time = string.split()

   day, month, year = date.split("-")
   day, month, year = int(day), int(month), int(year)

   hour, minute = time.split(":")
   hour, minute = int(hour), int(minute)

   return datetime(year, month, day, hour, minute)

def getLetterFromTime(time: datetime):
   if time.hour >= 5 and time.hour <= 12:
      return choice(['m', 't']) # morning, from 5AM - 12PM
      # choose random letter

   if time.hour >= 13 and time.hour <= 19:
      return choice(['e', 't']) # evening, from 1PM - 7PM

   if time.hour >= 20 and time.hour <= 24:
      return choice(['bs', 't']) # night, 8PM - 12AM
      # bs = before sleeping because people sleep at this time
   
   else:
      return 't'

def getZekrFromLetter(letter: str='t'):
   return requests.get(f"https://azkar-api.nawafhq.repl.co/zekr?{letter}&json").json()["content"]

def checkPrayerTime(time: datetime, country: str, city: str):
   api = requests.get(f"https://api.aladhan.com/v1/timingsByCity?country={country}&city={city}&school=8").json()
   
   # Fajr, Sunrise, Dhuhr, Asr, Sunset, Maghrib, Isha, Imsak, Midnight, Firstthird, Lastthird = api["data"]["timings"]
   timings = api["data"]["timings"]
   date = api["data"]["date"]["gregorian"]["date"]

   for prayer, timing in timings.items():
      fullDate = f"{date} {timing}"
      dt = extractDate(fullDate)

      if (time.hour == dt.hour) and time.minute == dt.minute:
         if prayer == "Fajr":
            return "حان الآن وقت صلاة الفجر"
         if prayer == "Dhuhr":
            return "حان الآن وقت صلاة الظهر"
         if prayer == "Asr":
            return "حان الآن وقت صلاة العصر"
         if prayer == "Maghrib":
            return "حان الآن وقت صلاة المغرب"
         if prayer == "Isha":
            return "حان الآن وقت صلاة العشاء"

def copyDatetime(datetime: datetime):
   return datetime.fromisoformat(datetime.isoformat())