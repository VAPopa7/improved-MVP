import os
import pandas as pd

docs = os.listdir("assets")
monthly_updates = []

for year in range(2009,2025):
    for month in range(1,13):
        if month < 10:
            month = str(0) + str(month)
        date = "_" + str(year) + str(month)
        res = list(filter(lambda x: date in x, docs))
        if len(res) > 0:
            last_day = res[-1]
            monthly_updates.append(last_day)

for year in range(2009,2025):
    resnew = list(filter(lambda x: "_" + str(year) in x, monthly_updates))
    # if len(resnew) == 12: 
    #     # print(f"{year} is correct")
    # else:
    #     # print(f"{year} is incorrect: {len(resnew)}")
    #     # print(resnew)

delete_files = set(docs) - set(monthly_updates)

for file in delete_files:
    path = "assets\\" + file
    os.remove(path)