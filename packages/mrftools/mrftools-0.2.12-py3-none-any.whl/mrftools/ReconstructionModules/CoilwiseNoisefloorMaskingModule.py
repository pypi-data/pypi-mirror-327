from ..Types import ReconstructionModuleIOType, KspaceData, ImageData
from . import ReconstructionModule, Register
from ..Utilities import dump_tensors
import torch
import gc
import numpy as np

@Register
class CoilwiseNoisefloorMaskingModule(ReconstructionModule):
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, noiseFactor=1.5, device=None):
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=inputType) 
        self.noiseFactor = noiseFactor
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device

    def __dict__(self):
        """
        Convert module attributes to a dictionary.

        Returns:
            dict: Dictionary containing module attributes.
        """
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "noiseFactor": self.noiseFactor
        }
        return moduleDict
    
    def GenerateHistogramNoisefloorMasks(self, data, noiseFactor):
        coil_masks = np.zeros(data.shape, dtype=bool)
        combined_binary_mask = np.zeros((data.shape[0], data.shape[1], data.shape[2], data.shape[3]), dtype=bool)
        for imSlice in range(data.shape[2]):
            for coil in range(data.shape[4]):
                coil_image = np.sum(np.abs(data[:, :, imSlice, :, coil]), axis=2)  # Sum over SVD components for each coil
                hist, bin_edges = np.histogram(coil_image[coil_image > 0], bins=100)  # Exclude zeros, make histogram
                noise_peak = np.argmax(hist)
                threshold = bin_edges[min(noise_peak + 1, len(bin_edges) - 1)] * noiseFactor
                mask_2d = coil_image > threshold
                mask_3d = np.repeat(mask_2d[:, :, np.newaxis], data.shape[3], axis=2)
                coil_masks[:, :, imSlice, :, coil] = mask_3d
                combined_binary_mask[:,:,imSlice, :] = combined_binary_mask[:,:,imSlice, :] | mask_3d
        return coil_masks, combined_binary_mask

    def ProcessImageToImage(self, inputData):
            self.coilMasks, self.combinedMask = self.GenerateHistogramNoisefloorMasks(inputData.numpy(), self.noiseFactor)
            outputData = inputData * self.coilMasks
            return ImageData(outputData)
    
    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        noiseFactor = jsonInput.get("noiseFactor")
        if noiseFactor != None:
            return CoilwiseNoisefloorMaskingModule(reconstructionParameters, inputType, noiseFactor)
        else:
            print("CoilwiseNoisefloorMaskingModule requires noiseFactor")
        