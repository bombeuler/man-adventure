import json
import re
from config import *


class JSONConvert:
    def __init__(self, sheetName):
        self.sheetPath = f"{ASSETS_PATH}/{sheetName}.json"
        self.__information = self.__convert()

    def __convert(self):
        with open(self.sheetPath, "r") as f:
            basicSheetJson = json.load(f)

        nameRe = re.compile(".*?\((.*?)\).aseprite", re.S)
        information = {}
        for spriteSheet in basicSheetJson.get("frames"):
            name = re.match(nameRe, spriteSheet.get("filename")).group(1)
            frameInfor = spriteSheet.get("frame")
            x = frameInfor.get("x")
            y = frameInfor.get("y")
            h = frameInfor.get("h")
            w = frameInfor.get("w")
            if h == 16:
                num = int(w / 16)
            else:
                num = 1
            rectList = []
            for i in range(num):
                rectList.append((x + i * w / num, y, w / num, h))
            information[name] = rectList
        return information

    def query(self, param):
        return self.__information.get(param)
