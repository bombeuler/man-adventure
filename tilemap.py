from config import *
import csv


class TileMap:
    def __init__(self, mapName="background"):
        mapPath = f"{ASSETS_PATH}/{mapName}.csv"
        mapData = []
        with open(mapPath, "r") as f:
            while True:
                lines = f.readline()[0:-1]
                if lines:
                    mapData.append(lines.split(","))
                else:
                    break
        self.__data = mapData

    def get_map(self):
        return self.__data
