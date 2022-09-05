import json
import re


class JSONConvert:
    def __init__(self, sheetName):
        self.sheetPath = f'./assets/{sheetName}.json'
        self.__information = self.__convert()

    def __convert(self):
        with open(self.sheetPath, 'r') as f:
            basicSheetJson = json.load(f)

        nameRe = re.compile('.*?\((.*?)\).aseprite', re.S)
        information = {}
        for spriteSheet in basicSheetJson.get('frames'):
            name = re.match(nameRe, spriteSheet.get('filename')).group(1)
            frameInfor = spriteSheet.get('frame')
            x = frameInfor.get('x')
            y = frameInfor.get('y')
            num = int(frameInfor.get('w') / frameInfor.get('h'))
            rectList = []
            for i in range(num):
                rectList.append((x + i * 16, y, x + (i + 1) * 16, y + 16))
            information[name] = rectList
        return information

    def query(self, param):
        return self.__information.get(param)