from ..Types import ReconstructionModuleIOType, ImageData
from . import ReconstructionModule, Register
import torch
import numpy as np
import mrftools.Utilities.torchkbnufft as tkbn


def PerformIFFTs(input, device): 
    """
    Perform inverse FFTs on input data.

    Args:
        input (torch.Tensor): Input data 
        device (torch.device): Device for computation.

    Returns:
        torch.Tensor: Inverse FFT results
    """
    sizes = np.shape(input)
    matrixSize=sizes[0:2]; numPartitions=sizes[2];numImages=sizes[3]; numCoils=sizes[4]; 
    images = torch.zeros((matrixSize[0], matrixSize[1], numPartitions, numImages, numCoils), dtype=input.dtype)
    for image in np.arange(0, numImages):
        image_device = input[:,:,:,image,:].to(device)
        images[:,:,:,image,:] = torch.fft.ifftshift(torch.fft.ifft(image_device, dim=2), dim=2)
        del image_device
    torch.cuda.empty_cache()
    return images
    

@Register
class IFFTModule(ReconstructionModule):
    """
    Inverse FFT module.

    Args:
        reconstructionParameters (dict): Parameters specific to the reconstruction module.
        inputType (ReconstructionModuleIOType, optional): Input data type. Defaults to ReconstructionModuleIOType.IMAGE.
        outputType (ReconstructionModuleIOType, optional): Output data type. Defaults to ReconstructionModuleIOType.IMAGE.
        device (torch.device, optional): Device for computation. Defaults to None.
    """
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, outputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, device=None):
        """
        Initialize the IFFTModule.

        Args:
            reconstructionParameters (dict): Parameters specific to the reconstruction module.
            inputType (ReconstructionModuleIOType, optional): Input data type. Defaults to ReconstructionModuleIOType.IMAGE.
            outputType (ReconstructionModuleIOType, optional): Output data type. Defaults to ReconstructionModuleIOType.IMAGE.
            device (torch.device, optional): Device for computation. Defaults to None.
        """
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
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
            "device": self.device.type,
        }
        return moduleDict

    def ProcessImageToImage(self, inputData):
        """
        Process data using inverse FFTs.

        Args:
            inputData (ImageData): Input image data.

        Returns:
            ImageData: Processed image data.
        """
        outputData = PerformIFFTs(inputData,self.device)
        return ImageData(outputData)

    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        """
        Create an instance of IFFTModule from JSON input.

        Args:
            jsonInput (dict): JSON input containing module details.
            reconstructionParameters (dict): Parameters specific to the reconstruction module.
            inputType (ReconstructionModuleIOType): Input data type.
            outputType (ReconstructionModuleIOType): Output data type.

        Returns:
            IFFTModule: Instance of IFFTModule.
        """
        device = jsonInput.get("device")
        if device != None:
            return IFFTModule(reconstructionParameters, inputType, outputType, torch.device(device))
        else:
            print("IFFTModule requires device")