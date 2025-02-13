from ..Types import ReconstructionModuleIOType, MapData, DictionaryEntry, Tissue
from . import ReconstructionModule, Register
import torch
import numpy as np
import os
import logging
from tqdm import tqdm
import scipy
import os
import numpy as np

b1Folder = ""

def LoadB1Map(matrixSize, b1Filename, resampleToMRFMatrixSize=True, deinterleave=True, deleteB1File=True):
    """
    Load and preprocess a B1 map.

    Args:
        matrixSize (tuple): Size of the target matrix.
        b1Filename (str): Filename of the B1 map.
        resampleToMRFMatrixSize (bool, optional): Whether to resample to MRF matrix size. Defaults to True.
        deinterleave (bool, optional): Whether to deinterleave. Defaults to True.
        deleteB1File (bool, optional): Whether to delete the B1 file after loading. Defaults to True.

    Returns:
        np.ndarray: Processed B1 map data.
    """
    # Using header, generate a unique b1 filename. This is temporary
    try:
        if(b1Folder != ""):
            b1Data = np.load(b1Folder + "/" + b1Filename +".npy")
        else:
            b1Data = np.load(b1Filename +".npy")
    except:
        logging.info("No B1 map found with requested filename. Trying fallback. ")
        try:
            b1Filename = f"B1Map_fallback"
            b1Data = np.load(b1Folder + "/" + b1Filename +".npy")
        except:
            logging.info("No B1 map found with fallback filename. Skipping B1 correction.")
            return np.array([])

    b1MapSize = np.array(np.shape(b1Data))
    logging.info(f"B1 Input Size: {b1MapSize}")
    if deinterleave:
        numSlices = b1MapSize[2]
        deinterleaved = np.zeros_like(b1Data)
        deinterleaved[:,:,np.arange(1,numSlices,2)] = b1Data[:,:,0:int(np.floor(numSlices/2))]
        deinterleaved[:,:,np.arange(0,numSlices-1,2)] = b1Data[:,:,int(np.floor(numSlices/2)):numSlices]
        b1Data = deinterleaved
    if resampleToMRFMatrixSize:
        b1Data = scipy.ndimage.zoom(b1Data, matrixSize/b1MapSize, order=5)
        b1Data = np.flip(b1Data, axis=2)
        b1Data = np.rot90(b1Data, axes=(0,1))
        b1Data = np.flip(b1Data, axis=0)
    logging.info(f"B1 Output Size: {np.shape(b1Data)}")
    if(deleteB1File):
        os.remove(b1Folder + "/" + b1Filename +".npy")     
        logging.info(f"Deleted B1 File: {b1Filename}")
    return b1Data
        
def performB1Binning(b1Data, b1Range, b1Stepsize, b1IdentityValue=800):
    """
    Perform B1 binning.

    Args:
        b1Data (np.ndarray): B1 map data.
        b1Range (tuple): B1 range for binning.
        b1Stepsize (float): B1 step size for binning.
        b1IdentityValue (int, optional): B1 identity value. Defaults to 800.

    Returns:
        np.ndarray: Binned B1 data.
    """
    b1Bins = np.arange(b1Range[0], b1Range[1], b1Stepsize)
    b1Clipped = np.clip(b1Data, np.min(b1Bins)*b1IdentityValue, np.max(b1Bins)*b1IdentityValue)
    b1Binned = b1Bins[np.digitize(b1Clipped, b1Bins*b1IdentityValue, right=True)]
    logging.info(f"Binned B1 Shape: {np.shape(b1Binned)}")
    return b1Binned

def vertex_of_parabola(points, clamp=False, min=None, max=None):
    """
    Calculate the vertex of a parabola given three points.

    Args:
        points (np.ndarray): Three points in the form [[x1, y1], [x2, y2], [x3, y3]].
        clamp (bool, optional): Whether to clamp the result. Defaults to False.
        min (float, optional): Minimum value to clamp to.
        max (float, optional): Maximum value to clamp to.

    Returns:
        tuple: Vertex coordinates (xv, yv) of the parabola.
    """
    x1 = points[:,0,0]
    y1 = points[:,0,1]
    x2 = points[:,1,0]
    y2 = points[:,1,1]
    x3 = points[:,2,0]
    y3 = points[:,2,1]
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom
    B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom
    C = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom
    xv = -B / (2*A)
    yv = C - B*B / (4*A)
    if clamp:
        torch.clamp(xv, min, max)
    return (xv, yv)

def GenerateDictionaryLookupTables(dictionaryEntries):
    """
    Generate lookup tables for dictionary entries.

    Args:
        dictionaryEntries (np.ndarray): Dictionary entries.

    Returns:
        tuple: uniqueT1s, uniqueT2s, dictionary1DIndexLookupTable, dictionary2DIndexLookupTable.
    """
    uniqueT1s = np.unique(dictionaryEntries['T1'])
    uniqueT2s = np.unique(dictionaryEntries['T2'])

    dictionary2DIndexLookupTable = []
    dictionaryEntries2D = np.zeros((len(uniqueT1s), len(uniqueT2s)), dtype=DictionaryEntry)
    dictionary1DIndexLookupTable = np.zeros((len(uniqueT1s), len(uniqueT2s)), dtype=int)
    for dictionaryIndex in tqdm(range(len(dictionaryEntries))):
        entry = dictionaryEntries[dictionaryIndex]
        T1index = np.where(uniqueT1s == entry['T1'])[0]
        T2index = np.where(uniqueT2s == entry['T2'])[0]
        dictionaryEntries2D[T1index, T2index] = entry
        dictionary1DIndexLookupTable[T1index, T2index] = dictionaryIndex
        dictionary2DIndexLookupTable.append([T1index,T2index])
    dictionary2DIndexLookupTable = np.array(dictionary2DIndexLookupTable)
    return uniqueT1s, uniqueT2s, dictionary1DIndexLookupTable, dictionary2DIndexLookupTable


def BatchPatternMatchViaMaxInnerProduct(signalTimecourses, dictionaryEntries, dictionaryEntryTimecourses, voxelsPerBatch=500, device=None):
    if(device==None):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    with torch.no_grad():
        signalsTransposed = torch.t(signalTimecourses)
        signalNorm = torch.linalg.norm(signalsTransposed, axis=1)[:,None]
        normalizedSignals = signalsTransposed / signalNorm
        simulationResults = dictionaryEntryTimecourses.to(torch.complex64)
        simulationNorm = torch.linalg.norm(simulationResults, axis=0)
        normalizedSimulationResults = torch.t((simulationResults / simulationNorm)).to(device)

        numBatches = int(np.shape(normalizedSignals)[0]/voxelsPerBatch)
        patternMatches = np.empty((np.shape(normalizedSignals)[0]), dtype=Tissue)
        M0 = torch.zeros(np.shape(normalizedSignals)[0], dtype=torch.complex64)
        with tqdm(total=numBatches) as pbar:
            for i in range(numBatches):
                firstVoxel = i*voxelsPerBatch
                if i == (numBatches-1):
                    lastVoxel = np.shape(normalizedSignals)[0]
                else:
                    lastVoxel = firstVoxel+voxelsPerBatch
                batchSignals = normalizedSignals[firstVoxel:lastVoxel,:].to(device)
                innerProducts = torch.inner(batchSignals, normalizedSimulationResults)
                maxInnerProductIndices = torch.argmax(torch.abs(innerProducts), 1, keepdim=True)
                maxInnerProducts = torch.take_along_dim(innerProducts,maxInnerProductIndices,dim=1).squeeze()
                signalNorm_device = signalNorm[firstVoxel:lastVoxel].squeeze().to(device)
                simulationNorm_device = simulationNorm.to(device)[maxInnerProductIndices.squeeze().to(torch.long)]
                M0_device = signalNorm_device/simulationNorm_device
                M0[firstVoxel:lastVoxel] = M0_device.cpu()
                patternValues = dictionaryEntries[maxInnerProductIndices.squeeze().to(torch.long).cpu()].squeeze()
                patternMatches[firstVoxel:lastVoxel]['T1'] = patternValues['T1']
                patternMatches[firstVoxel:lastVoxel]['T2'] = patternValues['T2']
                patternMatches[firstVoxel:lastVoxel]['M0'] = M0[firstVoxel:lastVoxel]
                pbar.update(1)
                del batchSignals, M0_device, signalNorm_device, simulationNorm_device
        del normalizedSimulationResults, dictionaryEntryTimecourses, dictionaryEntries, signalsTransposed, signalNorm, normalizedSignals, simulationResults
        del simulationNorm
        return patternMatches, M0

def BatchPatternMatchViaMaxInnerProductWithInterpolation(signalTimecourses, dictionaryEntries, dictionaryEntryTimecourses, voxelsPerBatch=500, device=None, radius=1):
    """
    Perform batch pattern matching via max inner product with interpolation.

    Args:
        signalTimecourses (torch.Tensor): Signal timecourses.
        dictionaryEntries (np.ndarray): Dictionary entries.
        dictionaryEntryTimecourses (torch.Tensor): Dictionary entry timecourses.
        voxelsPerBatch (int, optional): Number of voxels per batch. Defaults to 500.
        device (torch.device, optional): Device for computation. Defaults to None.
        radius (int, optional): Radius for interpolation. Defaults to 1.

    Returns:
        tuple: patternMatches, interpolatedMatches, M0.
    """
    if(device==None):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")

    with torch.no_grad():

        uniqueT1s, uniqueT2s, dictionary1DIndexLookupTable, dictionary2DIndexLookupTable = GenerateDictionaryLookupTables(dictionaryEntries)

        signalsTransposed = torch.t(signalTimecourses)
        signalNorm = torch.linalg.norm(signalsTransposed, axis=1)[:,None]
        normalizedSignals = signalsTransposed / signalNorm
        simulationResults = dictionaryEntryTimecourses.to(torch.complex64)
        simulationNorm = torch.linalg.norm(simulationResults, axis=0)
        normalizedSimulationResults = torch.t((simulationResults / simulationNorm)).to(device)

        numBatches = int(np.shape(normalizedSignals)[0]/voxelsPerBatch)
        patternMatches = np.empty((np.shape(normalizedSignals)[0]), dtype=Tissue)
        interpolatedMatches = np.empty((np.shape(normalizedSignals)[0]), dtype=Tissue)

        offsets = np.mgrid[-1*radius:radius+1, -1*radius:radius+1]
        numNeighbors = np.shape(offsets)[1]*np.shape(offsets)[2]
        
        M0 = torch.zeros(np.shape(normalizedSignals)[0], dtype=torch.complex64)
        with tqdm(total=numBatches) as pbar:
            for i in range(numBatches):
                firstVoxel = i*voxelsPerBatch
                if i == (numBatches-1):
                    lastVoxel = np.shape(normalizedSignals)[0]
                else:
                    lastVoxel = firstVoxel+voxelsPerBatch
                batchSignals = normalizedSignals[firstVoxel:lastVoxel,:].to(device)
                innerProducts = torch.inner(batchSignals, normalizedSimulationResults)
                maxInnerProductIndices = torch.argmax(torch.abs(innerProducts), 1, keepdim=True)
                maxInnerProducts = torch.take_along_dim(innerProducts,maxInnerProductIndices,dim=1).squeeze()
                signalNorm_device = signalNorm[firstVoxel:lastVoxel].squeeze().to(device)
                simulationNorm_device = simulationNorm.to(device)[maxInnerProductIndices.squeeze().to(torch.long)]
                M0_device = signalNorm_device/simulationNorm_device
                M0[firstVoxel:lastVoxel] = M0_device.cpu()
                patternValues = dictionaryEntries[maxInnerProductIndices.squeeze().to(torch.long).cpu()].squeeze()
                patternMatches[firstVoxel:lastVoxel]['T1'] = patternValues['T1']
                patternMatches[firstVoxel:lastVoxel]['T2'] = patternValues['T2']
                patternMatches[firstVoxel:lastVoxel]['M0'] = M0[firstVoxel:lastVoxel]
            
                indices = dictionary2DIndexLookupTable[maxInnerProductIndices.squeeze().to(torch.long).cpu()].squeeze()

                numVoxels = len(maxInnerProductIndices)
                neighbor2DIndices = np.reshape(indices.repeat(numNeighbors,axis=1),(np.shape(indices)[0], np.shape(indices)[1],np.shape(offsets)[1], np.shape(offsets)[2])) + offsets
                neighbor2DIndices[:,0,:,:] = np.clip(neighbor2DIndices[:,0,:,:], 0, np.shape(dictionary1DIndexLookupTable)[0]-1)
                neighbor2DIndices[:,1,:,:] = np.clip(neighbor2DIndices[:,1,:,:], 0, np.shape(dictionary1DIndexLookupTable)[1]-1)

                neighborDictionaryIndices = torch.tensor(dictionary1DIndexLookupTable[neighbor2DIndices[:,0,:,:], neighbor2DIndices[:,1,:,:]].reshape(numVoxels, -1)).to(device)
                neighborInnerProducts = torch.take_along_dim(torch.abs(innerProducts),neighborDictionaryIndices.to(torch.long),dim=1).squeeze()
                neighborDictionaryEntries = dictionaryEntries[neighborDictionaryIndices.cpu()].squeeze()

                #Sum of inner products through T2 neighbors for each T1 neighbor
                T1InnerProductSums = torch.stack((torch.sum(neighborInnerProducts[:, [0,1,2]], axis=1), torch.sum(neighborInnerProducts[:, [3,4,5]], axis=1), torch.sum(neighborInnerProducts[:,[6,7,8]], axis=1))).t()
                T2InnerProductSums = torch.stack((torch.sum(neighborInnerProducts[:, [0,3,6]], axis=1), torch.sum(neighborInnerProducts[:,[1,4,7]], axis=1), torch.sum(neighborInnerProducts[:,[2,5,8]], axis=1))).t()

                T1s = torch.tensor(neighborDictionaryEntries['T1'][:, [0,3,6]]).to(device)
                stacked_T1 = torch.stack((T1s, T1InnerProductSums))
                stacked_T1 = torch.moveaxis(stacked_T1, 0,1)

                T2s = torch.tensor(neighborDictionaryEntries['T2'][:, [0,1,2]]).to(device)
                stacked_T2 = torch.stack((T2s, T2InnerProductSums))
                stacked_T2 = torch.moveaxis(stacked_T2, 0,1)

                interpolatedValues = np.zeros((numVoxels),dtype=Tissue)
                interpT1s, _ = vertex_of_parabola(torch.moveaxis(stacked_T1,1,2), clamp=True, min=0, max=np.max(uniqueT1s))
                interpT2s, _ = vertex_of_parabola(torch.moveaxis(stacked_T2,1,2), clamp=True, min=0, max=np.max(uniqueT2s))
                
                interpolatedValues['T1'] = interpT1s.cpu()
                interpolatedValues['T2'] = interpT2s.cpu()
                interpolatedValues['M0'] = np.nan_to_num(M0_device.cpu())
                
                # For "edge" voxels, replace the interpolated values with the original pattern matches
                edgeT1s = (indices[:,0] == (len(uniqueT1s)-1)) + (indices[:,0] == (0))
                interpolatedValues[edgeT1s] = patternValues[edgeT1s]
                
                # For "edge" voxels, replace the interpolated values with the original pattern matches
                edgeT2s = (indices[:,1] == (len(uniqueT2s)-1)) + (indices[:,1] == (0))
                interpolatedValues[edgeT2s] = patternValues[edgeT2s]
                
                # For "nan" voxels, replace the interpolated values with the original pattern matches
                nanT1s = np.isnan(interpolatedValues['T1'])
                interpolatedValues[nanT1s] = patternValues[nanT1s]

                # For "nan" voxels, replace the interpolated values with the original pattern matches
                nanT2s = np.isnan(interpolatedValues['T2'])
                interpolatedValues[nanT2s] = patternValues[nanT2s]
                
                interpolatedMatches[firstVoxel:lastVoxel] = interpolatedValues
                pbar.update(1)
                del batchSignals, M0_device, signalNorm_device, simulationNorm_device

        del normalizedSimulationResults, dictionaryEntryTimecourses, dictionaryEntries, signalsTransposed, signalNorm, normalizedSignals, simulationResults
        del simulationNorm
        return patternMatches,interpolatedMatches, M0

def PatternMatchingViaMaxInnerProduct(combined, dictionary, simulation, voxelsPerBatch=500, b1Binned=None, device=None,):
    if(device==None):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    sizes = np.shape(combined)
    numSVDComponents=sizes[0]; matrixSize=sizes[1:4]
    patternMatches = np.empty((matrixSize), dtype=Tissue)
    M0 = torch.zeros((matrixSize), dtype=torch.complex64)
    if b1Binned is not None:
        for uniqueB1 in np.unique(b1Binned):
            logging.info(f"Pattern Matching B1 Value: {uniqueB1}")
            if uniqueB1 == 0:
                patternMatches[b1Binned==uniqueB1] = 0
            else:
                signalTimecourses = combined[:,b1Binned == uniqueB1]
                simulationTimecourses = torch.t(torch.t(torch.tensor(simulation.truncatedResults))[(np.argwhere(dictionary.entries['B1'] == uniqueB1))].squeeze())
                dictionaryEntries = dictionary.entries[(np.argwhere(dictionary.entries['B1'] == uniqueB1))]
                signalTimecourses = combined[:,b1Binned == uniqueB1]
                patternMatches[b1Binned == uniqueB1], M0[b1Binned == uniqueB1] = BatchPatternMatchViaMaxInnerProduct(signalTimecourses,dictionaryEntries,simulationTimecourses, voxelsPerBatch=voxelsPerBatch, device=device)
    else:
        signalTimecourses = torch.reshape(combined, (numSVDComponents,-1))
        if(dictionary.entries['B1'][0]):
            simulationTimecourses = torch.t(torch.t(torch.tensor(simulation.truncatedResults))[(np.argwhere(dictionary.entries['B1'] == 1))].squeeze())
            dictionaryEntries = dictionary.entries[(np.argwhere(dictionary.entries['B1'] == 1))]
        else:   
            simulationTimecourses = torch.tensor(simulation.truncatedResults)
            dictionaryEntries = dictionary.entries
        patternMatches, M0 = BatchPatternMatchViaMaxInnerProduct(signalTimecourses, dictionaryEntries, simulationTimecourses, voxelsPerBatch=voxelsPerBatch, device=device)
    patternMatches = np.reshape(patternMatches, (matrixSize))
    M0 = np.reshape(M0, (matrixSize)).numpy()
    M0 = np.nan_to_num(M0)
    return patternMatches

#---------------------------------
def PatternMatchingViaMaxInnerProductCoilConfidence(acquisition_devices, dictionary, simulation, ratio, voxelsPerBatch=500, b1Binned=None, device=None):
    if(device==None):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    
    sizes = acquisition_devices.shape
    numSVDComponents = sizes[0]
    matrixSize = sizes[1:4]
    numDevices = sizes[4]
    patternMatches = np.empty(matrixSize, dtype=Tissue)
    dictionaryIndices = np.empty(matrixSize, dtype=np.int64)
    M0 = torch.zeros(matrixSize, dtype=torch.complex64)
    
    all_confidences = []
    all_matches = []
    all_indices = []
    
    for device_idx in range(numDevices):
        signalTimecourses = torch.reshape(acquisition_devices[:, :, :, :, device_idx], (numSVDComponents, -1))
        if dictionary.entries['B1'][0]:
            simulationTimecourses = torch.t(torch.t(torch.tensor(simulation.truncatedResults))[(np.argwhere(dictionary.entries['B1'] == 1))].squeeze())
            dictionaryEntries = dictionary.entries[(np.argwhere(dictionary.entries['B1'] == 1))]
        else:
            simulationTimecourses = torch.tensor(simulation.truncatedResults)
            dictionaryEntries = dictionary.entries

        matches, M0_device, confidences, dictionaryIndices = BatchPatternMatchViaMaxInnerProductCoilConfidence(
            signalTimecourses, dictionaryEntries, simulationTimecourses, voxelsPerBatch=voxelsPerBatch, device=device)
        
        all_matches.append(matches)
        all_confidences.append(confidences)
        all_indices.append(dictionaryIndices)
        
    all_matches = np.stack(all_matches, axis=0)
    all_confidences = np.stack(all_confidences, axis=0)
    all_indices = np.stack(all_indices, axis=0)
    # Aggregate pattern matches
    #patternMatches, confidences = AggregatePatternMatchesByVoting(all_indices, all_confidences, dictionary)
    patternMatches, confidences, coilCounts = AggregatePatternMatchesHighestConfidence(all_matches, all_confidences, ratio=ratio)
    patternMatches = np.reshape(patternMatches, (matrixSize))
    confidences = np.reshape(confidences, (matrixSize))
    coilCounts = np.reshape(coilCounts, (matrixSize))
    M0 = np.reshape(M0, (matrixSize)).numpy()
    M0 = np.nan_to_num(M0)
    return patternMatches, confidences, coilCounts


def BatchPatternMatchViaMaxInnerProductCoilConfidence(signalTimecourses, dictionaryEntries, dictionaryEntryTimecourses, voxelsPerBatch=500, device=None):
    if(device==None):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    
    with torch.no_grad():
        signalsTransposed = torch.t(signalTimecourses)
        signalNorm = torch.linalg.norm(signalsTransposed, axis=1)[:, None]
        normalizedSignals = signalsTransposed / signalNorm

        simulationResults = dictionaryEntryTimecourses.to(torch.complex64)
        simulationNorm = torch.linalg.norm(simulationResults, axis=0)
        normalizedSimulationResults = torch.t((simulationResults / simulationNorm)).to(device)
    
        numBatches = int(np.shape(normalizedSignals)[0] / voxelsPerBatch)
        patternMatches = np.empty((np.shape(normalizedSignals)[0]), dtype=Tissue)
        dictionaryIndices = np.empty((np.shape(normalizedSignals)[0]), dtype=np.int64)
        M0 = torch.zeros(np.shape(normalizedSignals)[0], dtype=torch.complex64)
        confidences = torch.zeros(np.shape(normalizedSignals)[0], dtype=torch.float32)

        with tqdm(total=numBatches) as pbar:
            for i in range(numBatches):
                firstVoxel = i * voxelsPerBatch
                if i == (numBatches - 1):
                    lastVoxel = np.shape(normalizedSignals)[0]
                else:
                    lastVoxel = firstVoxel + voxelsPerBatch
                
                batchSignals = normalizedSignals[firstVoxel:lastVoxel, :].to(device)
                innerProducts = torch.inner(batchSignals, normalizedSimulationResults)
                maxInnerProductIndices = torch.argmax(torch.abs(innerProducts), 1, keepdim=True)
                maxInnerProducts = torch.take_along_dim(torch.abs(innerProducts), maxInnerProductIndices, dim=1).squeeze()

                signalNorm_device = signalNorm[firstVoxel:lastVoxel].squeeze().to(device)
                simulationNorm_device = simulationNorm.to(device)[maxInnerProductIndices.squeeze().to(torch.long)]
                M0_device = signalNorm_device / simulationNorm_device
                M0[firstVoxel:lastVoxel] = M0_device.cpu()

                confidences[firstVoxel:lastVoxel] = maxInnerProducts.cpu()
                indices = maxInnerProductIndices.squeeze().to(torch.long).cpu()
                patternValues = dictionaryEntries[indices].squeeze()
                dictionaryIndices[firstVoxel:lastVoxel] = indices
                patternMatches[firstVoxel:lastVoxel]['T1'] = patternValues['T1']
                patternMatches[firstVoxel:lastVoxel]['T2'] = patternValues['T2']
                patternMatches[firstVoxel:lastVoxel]['M0'] = M0[firstVoxel:lastVoxel]

                pbar.update(1)
                del batchSignals, M0_device, signalNorm_device, simulationNorm_device

        return patternMatches, M0, confidences, dictionaryIndices
    
def AggregatePatternMatchesByVoting(all_indices, all_confidences, dictionary):
    num_patterns = len(dictionary.entries)
    num_devices = all_indices.shape[0]
    num_voxels = all_indices.shape[1]

    # Initialize the weighted votes array
    weighted_votes = np.zeros((num_voxels, num_patterns), dtype=np.float32)
    print("weighted_votes", weighted_votes.shape)
    
    for i in range(num_devices):
        indices = all_indices[i]
        confidences = all_confidences[i]
        # Use advanced indexing to accumulate confidence votes
        np.add.at(weighted_votes, (np.arange(num_voxels), indices), confidences)
    
    # Determine the final pattern matches by selecting the pattern with the highest vote count
    final_indices = np.argmax(weighted_votes, axis=-1)
    final_patternMatches = dictionary.entries[final_indices]
    
    # Create a confidence map based on the highest vote counts
    confidence_map = np.max(weighted_votes, axis=-1)
    return final_patternMatches, confidence_map
    
def AggregatePatternMatchesByIterativeOutlierRemoval(all_indices, all_confidences, dictionary, stddev_limit=4, stddev_threshold=0.5):
    num_patterns = len(dictionary.entries)
    num_devices = all_indices.shape[0]
    num_voxels = all_indices.shape[1]

    final_indices = np.zeros(num_voxels, dtype=int)
    confidence_map = np.zeros(num_voxels, dtype=np.float32)
    coilcount_map = np.zeros(num_voxels, dtype=np.float32)
    patternMatches = np.empty((num_voxels), dtype=Tissue)
    
    for voxel_idx in range(num_voxels):
        indices = all_indices[:, voxel_idx]
        confidences = all_confidences[:, voxel_idx]

        # Extract T1 and T2 values for the current voxel
        T1_values = np.array([dictionary.entries[idx]['T1'] for idx in indices])
        T2_values = np.array([dictionary.entries[idx]['T2'] for idx in indices])

        # Iteratively remove outliers
        while True:
            mean_T1 = np.mean(T1_values)
            stddev_T1 = np.std(T1_values)
            mean_T2 = np.mean(T2_values)
            stddev_T2 = np.std(T2_values)

            within_limit = (np.abs(T1_values - mean_T1) <= stddev_limit * stddev_T1) & (np.abs(T2_values - mean_T2) <= stddev_limit * stddev_T2)

            if np.all(within_limit):
                break

            T1_values = T1_values[within_limit]
            T2_values = T2_values[within_limit]
            indices = indices[within_limit]
            confidences = confidences[within_limit]

        # Check the standard deviation threshold
        if (stddev_T1 > stddev_threshold * mean_T1) or (stddev_T2 > stddev_threshold * mean_T2):
            patternMatches[voxel_idx]['T1'] = 0
            patternMatches[voxel_idx]['T2'] = 0
            patternMatches[voxel_idx]['M0'] = 0
            confidence_map[voxel_idx] = 0.0
        else:
            if len(indices) > 0:
                patternMatches[voxel_idx]['T1'] = np.mean(T1_values)
                patternMatches[voxel_idx]['T2'] = np.mean(T2_values)
                patternMatches[voxel_idx]['M0'] = 0
                confidence_map[voxel_idx] = np.mean(confidences)
                coilcount_map[voxel_idx] = len(indices)
            else:
                # If all entries were removed, assign a default value (e.g., the first index)
                patternMatches[voxel_idx]['T1'] = 0
                patternMatches[voxel_idx]['T2'] = 0
                patternMatches[voxel_idx]['M0'] = 0
                confidence_map[voxel_idx] = 0.0

    #final_patternMatches = dictionary.entries[final_indices]
    return patternMatches, confidence_map, coilcount_map

def closest_indices_to_median(values, ratio):
    """
    Find the indices of the values in a NumPy array that are closest to the median,
    sorted by their distance from the median.

    Parameters:
    values (numpy.ndarray): Input array of values.

    Returns:
    numpy.ndarray: The indices of the closest half of the values sorted by their distance from the median.
    """
    # Calculate the median
    median_value = np.median(values)

    # Compute the absolute differences from the median
    differences = np.abs(values - median_value)

    # Get the indices that would sort the array by distance from the median
    sorted_indices = np.argsort(differences)

    # Determine the number of closest values to select (half of the array length)
    num_closest = int(np.ceil(len(data) * (ratio)))

    # Select the indices of the closest half of the values
    closest_indices = sorted_indices[:num_closest]

    # Sort the closest indices by their distance from the median
    sorted_closest_indices = closest_indices[np.argsort(differences[closest_indices])]

    return sorted_closest_indices

def AggregatePatternMatches(all_indices, all_confidences, dictionary, ratio=0.10):
    num_patterns = len(dictionary.entries)
    num_devices = all_indices.shape[0]
    num_voxels = all_indices.shape[1]

    final_indices = np.zeros(num_voxels, dtype=int)
    confidence_map = np.zeros(num_voxels, dtype=np.float32)
    coilcount_map = np.zeros(num_voxels, dtype=np.float32)
    patternMatches = np.empty((num_voxels), dtype=Tissue)
    
    for voxel_idx in range(num_voxels):
        indices = all_indices[:, voxel_idx]
        confidences = all_confidences[:, voxel_idx]

        # Extract T1 and T2 values for the current voxel
        T1_values = np.array([dictionary.entries[idx]['T1'] for idx in indices])
        T2_values = np.array([dictionary.entries[idx]['T2'] for idx in indices])
        
        T1_indices = closest_indices_to_median(T1_values, ratio)
        T2_indices = closest_indices_to_median(T2_values, ratio)
        within_limit = (T1_indices & T2_indices)
        T1_values = T1_values[within_limit]
        T2_values = T2_values[within_limit]
        indices = indices[within_limit]
        confidences = confidences[within_limit]
        
        patternMatches[voxel_idx]['T1'] = np.mean(T1_values)
        patternMatches[voxel_idx]['T2'] = np.mean(T2_values)
        patternMatches[voxel_idx]['M0'] = 0
        confidence_map[voxel_idx] = np.mean(confidences)
        coilcount_map[voxel_idx] = len(indices)

    return patternMatches, confidence_map, coilcount_map

def highest_indices(data, ratio):
    data = np.array(data)
    non_zero_indices = np.where(data != 0)[0]
    non_zero_data = data[non_zero_indices]
    
    num_elements = int(np.ceil(len(non_zero_data) * ratio))
    indices = np.argpartition(non_zero_data, -num_elements)[-num_elements:]
    sorted_indices = non_zero_indices[indices[np.argsort(non_zero_data[indices])[::-1]]]
    
    return sorted_indices

def weighted_mean_by_confidence(values, confidences):
    weighted_sum = sum(v * c for v, c in zip(values, confidences))
    sum_of_confidences = sum(confidences)
    if sum_of_confidences > 0:
        return weighted_sum / sum_of_confidences
    else:
        return 0
        
def AggregatePatternMatchesHighestConfidence(all_matches, all_confidences, ratio):
    num_devices = all_matches.shape[0]
    num_voxels = all_matches.shape[1]
    confidence_map = np.zeros(num_voxels, dtype=np.float32)
    coilcount_map = np.zeros(num_voxels, dtype=np.float32)
    patternMatches = np.empty((num_voxels), dtype=Tissue)
    
    for voxel_idx in range(num_voxels):
        matches = all_matches[:, voxel_idx]
        confidences = np.nan_to_num(all_confidences[:, voxel_idx])

        # Extract T1 and T2 values for the current voxel
        within_limit = highest_indices(confidences, ratio)
        T1_values = matches['T1'][within_limit]
        T2_values = matches['T2'][within_limit]
        M0_values = matches['M0'][within_limit]
        confidences = confidences[within_limit]
        
        patternMatches[voxel_idx]['T1'] = weighted_mean_by_confidence(T1_values,confidences)
        patternMatches[voxel_idx]['T2'] = weighted_mean_by_confidence(T2_values,confidences)
        patternMatches[voxel_idx]['M0'] = weighted_mean_by_confidence(M0_values,confidences)
        confidence_map[voxel_idx] = weighted_mean_by_confidence(confidences, confidences)
        #confidence_map[voxel_idx] = np.mean(confidences)
        coilcount_map[voxel_idx] = len(confidences)

    return patternMatches, confidence_map, coilcount_map


#---------------------------------

def PatternMatchingViaMaxInnerProductWithInterpolation(combined, dictionary, simulation, voxelsPerBatch=500, b1Binned=None, device=None,):
    """
    Perform pattern matching via max inner product with interpolation.

    Args:
        combined (torch.Tensor): Combined data.
        dictionary (Dictionary): Dictionary.
        simulation (Simulation): Simulation.
        voxelsPerBatch (int, optional): Number of voxels per batch. Defaults to 500.
        b1Binned (np.ndarray, optional): Binned B1 data. Defaults to None.
        device (torch.device, optional): Device for computation. Defaults to None.

    Returns:
        np.ndarray: Interpolated matches.
    """
    if(device==None):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    sizes = np.shape(combined)
    numSVDComponents=sizes[0]; matrixSize=sizes[1:4]
    patternMatches = np.empty((matrixSize), dtype=Tissue)
    interpolatedMatches = np.empty((matrixSize), dtype=Tissue)
    M0 = torch.zeros((matrixSize), dtype=torch.complex64)
    if b1Binned is not None:
        for uniqueB1 in np.unique(b1Binned):
            logging.info(f"Pattern Matching B1 Value: {uniqueB1}")
            if uniqueB1 == 0:
                patternMatches[b1Binned==uniqueB1] = 0
            else:
                signalTimecourses = combined[:,b1Binned == uniqueB1]
                simulationTimecourses = torch.t(torch.t(torch.tensor(simulation.truncatedResults))[(np.argwhere(dictionary.entries['B1'] == uniqueB1))].squeeze())
                dictionaryEntries = dictionary.entries[(np.argwhere(dictionary.entries['B1'] == uniqueB1))]
                signalTimecourses = combined[:,b1Binned == uniqueB1]
                patternMatches[b1Binned == uniqueB1], interpolatedMatches[b1Binned == uniqueB1], M0[b1Binned == uniqueB1] = BatchPatternMatchViaMaxInnerProductWithInterpolation(signalTimecourses,dictionaryEntries,simulationTimecourses, voxelsPerBatch=voxelsPerBatch, device=device)
    else:
        signalTimecourses = torch.reshape(combined, (numSVDComponents,-1))
        if(dictionary.entries['B1'][0]):
            simulationTimecourses = torch.t(torch.t(torch.tensor(simulation.truncatedResults))[(np.argwhere(dictionary.entries['B1'] == 1))].squeeze())
            dictionaryEntries = dictionary.entries[(np.argwhere(dictionary.entries['B1'] == 1))]
        else:   
            simulationTimecourses = torch.tensor(simulation.truncatedResults)
            dictionaryEntries = dictionary.entries
        patternMatches, interpolatedMatches, M0 = BatchPatternMatchViaMaxInnerProductWithInterpolation(signalTimecourses, dictionaryEntries, simulationTimecourses, voxelsPerBatch=voxelsPerBatch, device=device)
    patternMatches = np.reshape(patternMatches, (matrixSize))
    interpolatedMatches = np.reshape(interpolatedMatches, (matrixSize))
    M0 = np.reshape(M0, (matrixSize)).numpy()
    M0 = np.nan_to_num(M0)
    return patternMatches, interpolatedMatches

@Register
class PatternMatchingModule(ReconstructionModule):
    """
    Pattern matching module.

    Args:
        reconstructionParameters (dict): Parameters specific to the reconstruction module.
        inputType (ReconstructionModuleIOType, optional): Input data type. Defaults to ReconstructionModuleIOType.IMAGE.
        outputType (ReconstructionModuleIOType, optional): Output data type. Defaults to ReconstructionModuleIOType.MAP.
        mode (str, optional): Mode of operation. Defaults to "interpolated".
        voxelsPerBatch (int, optional): Number of voxels per batch. Defaults to 1000.
        device (torch.device, optional): Device for computation. Defaults to None.
    """

    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, outputType:ReconstructionModuleIOType=ReconstructionModuleIOType.MAP, mode="interpolated", voxelsPerBatch=1000, ratio=None, device=None):
        """
        Initialize the PatternMatchingModule.

        Args:
            reconstructionParameters (ReconstructionParameters): Parameters for the reconstruction.
            inputType (ReconstructionModuleIOType): Input data type.
            outputType (ReconstructionModuleIOType): Output data type.
            mode (str): Mode for pattern matching (e.g., "interpolated").
            voxelsPerBatch (int): Number of voxels per batch.
            device (torch.device): Device to use for computation.
        """
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
        self.mode = mode
        self.voxelsPerBatch = voxelsPerBatch
        self.ratio = ratio
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device
    def __dict__(self):
        """
        Convert the module's attributes to a dictionary.

        Returns:
            dict: Dictionary representation of the module.
        """
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "mode": self.mode,
            "voxelsPerBatch": self.voxelsPerBatch,
            "ratio": self.ratio, 
            "device": self.device.type,
        }
        return moduleDict

    def ProcessImageToMap(self, inputData):
        """
        Process image data to map data using pattern matching.

        Args:
            inputData (ImageData): Input image data with shape [svdComponents, xMat, yMat, zMat]

        Returns:
            MapData: Output map data.
        """
        if(self.mode == "interpolated"):
            combined = inputData.squeeze() # Put into format [svdComponent, x,y,z]
            _, outputData = PatternMatchingViaMaxInnerProductWithInterpolation(combined, self.reconstructionParameters.simulation.dictionaryParameters, self.reconstructionParameters.simulation, self.voxelsPerBatch, None, self.device)
        elif((self.mode == "direct")):
            combined = inputData.squeeze() # Put into format [svdComponent, x,y,z]
            outputData = PatternMatchingViaMaxInnerProduct(combined, self.reconstructionParameters.simulation.dictionaryParameters, self.reconstructionParameters.simulation, self.voxelsPerBatch, None, self.device)
        elif((self.mode == "coil-confidence")):
            combined = inputData.squeeze().moveaxis(-2,0) # Put into format [svdComponent, x,y,z, coil]
            outputData, self.confidenceMap, self.coilCounts = PatternMatchingViaMaxInnerProductCoilConfidence(combined, self.reconstructionParameters.simulation.dictionaryParameters, self.reconstructionParameters.simulation, self.ratio, self.voxelsPerBatch, None, self.device)
        else:
            return None
        return MapData(outputData)

    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        """
        Create an instance of the PatternMatchingModule from JSON input.

        Args:
            jsonInput (dict): JSON input data.
            reconstructionParameters (dict): Parameters specific to the reconstruction module.
            inputType (ReconstructionModuleIOType): Input data type.
            outputType (ReconstructionModuleIOType): Output data type.

        Returns:
            PatternMatchingModule: Instance of the PatternMatchingModule.
        """
        mode = jsonInput.get("mode")
        voxelsPerBatch = jsonInput.get("voxelsPerBatch")
        ratio = jsonInput.get("ratio")
        device = jsonInput.get("device")
        if mode != None and voxelsPerBatch != None and device != None:
            return PatternMatchingModule(reconstructionParameters, inputType, outputType, mode, voxelsPerBatch, ratio, torch.device(device))
        else:
            print("NUFFTModule requires mode, voxelsPerBatch, and device")
    