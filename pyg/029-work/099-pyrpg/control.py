
import pygame as pg
from pygame.locals import *
import codecs
import os
import random
import struct
import sys




class Method:

    def __init__(self):
        pass

    @staticmethod
    def load_image(dir, file, colorkey=None)->pg.image:
        file = os.path.join(dir, file)
        try:
            img = pg.image.load(file)
        except pg.error as message:
            print("Cannot load image:", file)
            raise SystemExit(message)

        img = img.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = img.get_at((0,0))
            img.set_colorkey(colorkey, RLEACCEL)

        return img

    @staticmethod
    def split_image(image)->None:
        """128x128のキャラクターイメージを32x32の16枚のイメージに分割
        分割したイメージを格納したリストを返す"""
        imageList = []
        for i in range(0, 128, GS):
            for j in range(0, 128, GS):
                surface = pg.Surface((GS,GS))
                surface.blit(image, (0,0), (j,i,GS,GS))
                surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
                surface.convert()
                imageList.append(surface)
        return imageList

    @staticmethod
    def load_sounds(dir, file)->None:
        """サウンドをロードしてsoundsに格納"""
        file = os.path.join(dir, file)
        fp = open(file, "r")
        for line in fp:
            line = line.rstrip()
            data = line.split(",")
            se_name = data[0]
            se_file = os.path.join("se", data[1])
            sounds[se_name] = pg.mixer.Sound(se_file)
        fp.close()

    @staticmethod
    def load_charachips(dir, file)->None:
        """キャラクターチップをロードしてCharacter.imagesに格納"""
        file = os.path.join(dir, file)
        fp = open(file, "r")
        for line in fp:
            line = line.rstrip()
            data = line.split(",")
            chara_id = int(data[0])
            chara_name = data[1]
            Character.images[chara_name] = split_image(load_image("charachip", "%s.png" % chara_name))
        fp.close()

    @staticmethod
    def load_mapchips(dir, file)->None:
        """マップチップをロードしてMap.imagesに格納"""
        file = os.path.join(dir, file)
        fp = open(file, "r")
        for line in fp:
            line = line.rstrip()
            data = line.split(",")
            mapchip_id = int(data[0])
            mapchip_name = data[1]
            movable = int(data[2])  # 移動可能か？
            transparent = int(data[3])  # 背景を透明にするか？
            if transparent == 0:
                Map.images.append(load_image("mapchip", "%s.png" % mapchip_name))
            else:
                Map.images.append(load_image("mapchip", "%s.png" % mapchip_name, TRANS_COLOR))
            Map.movable_type.append(movable)
        fp.close()

