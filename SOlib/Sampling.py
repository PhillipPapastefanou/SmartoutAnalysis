from SOlib.Scaling import  ScalerListToArray
from SOlib.outputfile import  OutputFile
from SOlib.outputfile import  TimeDomain
import numpy as np
from enum import Enum


class Scenario(Enum):
    Control = 1
    Drought = 2

class StratifiedSample:

    def __init__(self, path):
        self.path = path
        file = OutputFile(self.path)
        self.lons = file.nc.variables['Longitude'][:]
        self.lats = file.nc.variables['Latitude'][:]
        file.Close()

    def PftNames(self):
        file = OutputFile(self.path)
        names = file.PFTVarNames
        file.Close()
        return names;

    def PatchNames(self):
        file = OutputFile(self.path)
        names = file.PatchVarNames
        file.Close()
        return names;

    def Get(self, var, year, gridcell):
        file = OutputFile(self.path)
        data = file._GetPFT(var, 0, file.insFileDim.size, pftID_begin=0, pftID_end=0, yearBeginOfInterest=year, yearEndOfInterest= year, gridcellBegin=gridcell, gridcellEnd=gridcell)
        file.Close()
        return data


    def GetSelection(self, var, yearBegin, yearEnd, gridcell, insfileBegin, insfileEnd):
        file = OutputFile(self.path)
        data = file._GetPFT(var, insfileBegin, insfileEnd, pftID_begin=0, pftID_end=0, yearBeginOfInterest=yearBegin, yearEndOfInterest= yearEnd, gridcellBegin=gridcell, gridcellEnd=gridcell)
        file.Close()
        return data


    def GetAllGridcells(self, var, yearBegin,yearEnd, insfileBegin, insfileEnd):
        file = OutputFile(self.path)
        data = file._GetPFT(var, insfileBegin, insfileEnd, pftID_begin=0, pftID_end=0, yearBeginOfInterest=yearBegin, yearEndOfInterest= yearEnd, gridcellBegin=0, gridcellEnd=file.gridcellDim.size)
        file.Close()
        return data

    def GetAllGridcellsPatch(self, var, yearBegin,yearEnd, insfileBegin, insfileEnd):
        file = OutputFile(self.path)
        data = file._GetPatch(var, insfileBegin, insfileEnd, yearBeginOfInterest=yearBegin, yearEndOfInterest= yearEnd,gridcellBegin=0, gridcellEnd=file.gridcellDim.size)
        file.Close()
        return data

    def CreateImage(self, res, biomasses):

        lonScaler = ScalerListToArray(self.lons, res, False)
        latScaler = ScalerListToArray(self.lats, res, False)
        lonIndexes = lonScaler.Indexes
        latIndexes = latScaler.Indexes
        xlen = lonScaler.len
        ylen = latScaler.len
        self.IMG_extent = [lonScaler.min, lonScaler.max, latScaler.min, latScaler.max ]

        image = np.empty((ylen + 1, xlen + 1,)) * np.nan
        for i in range(len(self.lons)):
            image[latIndexes[i], lonIndexes[i]] = biomasses[i]

        return image



