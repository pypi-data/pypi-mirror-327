NetTracer3D is a python package developed for both 2D and 3D analysis of microscopic images in the .tif file format. It supports generation of 3D networks showing the relationships between objects (or nodes) in three dimensional space, either based on their own proximity or connectivity via connecting objects such as nerves or blood vessels. In addition to these functionalities are several advanced 3D data processing algorithms, such as labeling of branched structures or abstraction of branched structures into networks. Note that nettracer3d uses segmented data, which can be segmented from other softwares such as ImageJ and imported into NetTracer3D, although it does offer its own segmentation via intensity and volumetric thresholding, or random forest machine learning segmentation. NetTracer3D currently has a fully functional GUI. To use the GUI, after installing the nettracer3d package via pip, enter the command 'nettracer3d' in your command prompt:


This gui is built from the PyQt6 package and therefore may not function on dockers or virtual envs that are unable to support PyQt6 displays. More advanced documentation is coming down the line, but for now please see: https://www.youtube.com/watch?v=cRatn5VTWDY
for a video tutorial on using the GUI.

NetTracer3D is free to use/fork for academic/nonprofit use so long as citation is provided, and is available for commercial use at a fee (see license file for information).

NetTracer3D was developed by Liam McLaughlin while working under Dr. Sanjay Jain at Washington University School of Medicine.

-- Version 0.5.3 updates --

1. Improved calculate volumes method. Previous method used np.argwhere() to count voxels of labeled objects in parallel which was quite strenuous in large arrays with many objects. New method uses np.bincount() which uses optimized numpy C libraries to do the same.
2. scipy.ndimage.find_objects() method was replaced as the method to find bounding boxes for objects when searching for object neighborhoods for the morphological proximity network and the edge < > node interaction quantification. This new version should be substantially faster in big arrays with many labels. (Depending on how well this improves performance, I may reimplement the secondary network search algorithm, as a side-option, which uses the same parallel-search within subarray strategies, as opposed to the primary network search algorithm that uses distance transforms).
3. Image viewer window can now load in .nii format images, as well as .jpeg, .jpg, and .png. The nibabel library was added to the dependencies to enable .nii loading, although this is currently all it is used for (and the gui will still run without nibabel).
4. Fixed bug regarding deleting edge objects. 