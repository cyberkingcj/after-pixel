import cv2
import os
from PIL import Image
from DenoiseImage import Denoise


class Process:

    def __init__(self, imagePath):

        self.__imageName = imagePath.split("/")[-1]
        
        self.imagePath = imagePath
    
        self.__denoise = Denoise()

    def startProcessing(self, usingCBD = True, choice = "real"):
        if usingCBD:
            processedImage = self.__denoise.CBDdenoise(self.imagePath, choice)
        else:
            processedImage = self.__denoise.UNetdenoise(self.imagePath)

        pathToSave = os.getcwd() + '/static/images/cleaned'+self.__imageName
        processedImage.save(pathToSave)

        print('DONE')
        return