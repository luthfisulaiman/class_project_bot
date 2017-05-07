import requests
import os
from random import randint


class FileHandler:

    def __init__(self):
        self.fname = os.path.abspath(os.path.join(os.path.dirname(__file__), "id_list.csv"))

    def openfile(self):
        self._file = open(self.fname, "r")

    def readfile(self):
        return self._file.read().split("\n")

    def closefile(self):
        self._file.close()


class MemeGenerator:

    def __init__(self):
        self.dank = Meme()
        self.requester = MemeRequester()
        self.items = {}
        self.fHandler = FileHandler()
        self.fHandler.openfile()
        self._memelist = self.fHandler.readfile()
        self.fHandler.closefile()

    def createid(self):
        self.items['id'] = self._memelist[randint(0, len(self._memelist) - 1)]

    def createbottom(self, caption):
        if(len(caption) >= 100):
            raise ValueError
        self.items['bottom'] = caption

    def createtop(self, caption):
        if(len(caption) >= 100):
            raise ValueError
        self.items['top'] = caption

    def generatememe(self):
        self.dank.set(self.items['id'], self.items['bottom'], self.items['top'])
        self.items['image'] = self.requester.makerequest(self.dank)['data']['url']
        self.dank.setimage(self.items['image'])
        return self.dank


class Meme:

    def __init__(self):
        self._id = ""
        self._bottomCaption = ""
        self._topCaption = ""
        self._image = ""

    def getid(self):
        return self._id

    def getbottom(self):
        return self._bottomCaption

    def gettop(self):
        return self._topCaption

    def set(self, id, bottom, top):
        self._id = id
        self._bottomCaption = bottom
        self._topCaption = top

    def setimage(self, imageurl):
        self._image = imageurl

    def getimage(self):
        return self._image


class MemeRequester:

    def __init__(self):
        self.url = "https://api.imgflip.com/caption_image"

    def makerequest(self, meme):
        mid = meme.getid()
        top = meme.gettop()
        btm = meme.getbottom()
        ur = "imgflip_hubot"
        task = {"template_id": mid, "username": ur, "password": ur, "text0": top, "text1": btm}
        req = requests.post(self.url, params=task)
        return req.json()
