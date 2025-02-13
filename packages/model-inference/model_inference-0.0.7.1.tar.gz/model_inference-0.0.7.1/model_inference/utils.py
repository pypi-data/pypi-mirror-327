from identity_clustering.cluster import detect_faces, FaceCluster, cluster
from identity_clustering.utils import _get_crop
from .Inference import Inference
import numpy as np
import os
import tqdm
import cv2 as cv
def detect_probable_fakes(mask_frame, bbox, threshold = 0.50, use_get_crop_v2 : bool = False):
    global mask
    if use_get_crop_v2:
        mask = _get_crop_v2(mask_frame, bbox, pad_constant=4)
    else:
        mask = _get_crop(mask_frame,bbox, pad_constant=4)
    tot = mask.shape[0] * mask.shape[1]
    blob = np.sum(mask)
    if blob == 0.:
        return 1.
    
    fake_prob = blob/tot
    if fake_prob >= threshold:
        return 0.
    else:
        return 1.
def prepare_data(root_dir, save_dir, mask_dir, min_num_frames = 10):
    inf = Inference("cuda")
    clust = FaceCluster()
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    save_idx = 0

    for video_file in tqdm.tqdm(os.listdir(root_dir)):

        video_path = os.path.join(root_dir, video_file)
        mask_path = os.path.join(mask_dir, video_file[:-4] + "_mask.mp4")
        faces, fps = detect_faces(video_path,"cuda")
        clu = cluster(clust,video_path,faces,50)
        vid = cv.VideoCapture(mask_path)
        frames = []
        while True:
            success, frame = vid.read()
            if not success:
                break
            frames.append(cv.cvtColor(frame, cv.COLOR_BGR2GRAY))
        
        for key, value in clu.items():

            if len(value) < min_num_frames:
                continue

            label = None
            for i in value:
                frame_idx = i[0]
                curr_mask = frames[frame_idx]
                if label == None or label == 1:
                    label = detect_probable_fakes(curr_mask, i[2], 0.3)
            
            identity_tensor = inf.cvt_to_rgb(value)
            identity_tensor = identity_tensor.numpy()
            arr = np.array(identity_tensor)
            arr_label = np.array(label)
            np.save(os.path.join(save_dir, str(save_idx) + ".npy"),arr)
            np.save(os.path.join(save_dir,str(save_idx)+"_label.npy"),arr_label)
            save_idx += 1

def _get_crop_v2(frame, bbox, pad_constant : int | tuple = 3, multiplier: int = 1):
    '''
        This function takes a frame and a bbox and then outputs the region of the image given by the bounding box
        Args : 
        - frame : np.ndarray -> image frame containing the faces to be cropped.
        - bbox : list -> the bounding box associated with that frame.
        - pad_constant : int -> The constant to control the padding. Default is None.
        - use_pad_constant : bool -> If True, uses the pad_constant to control the padding. Default is False.
        - multiplier : int -> mulitplier to multiply bbox values (must be clearly defined later)
        Returns :

        - crop : np.ndarray -> the cropped output of the faces.
    '''
    xmin, ymin, xmax, ymax = [int(b*multiplier) for b in bbox]
    w = xmax - xmin
    h = ymax - ymin

    # Add some padding to catch background too
    '''
                          [[B,B,B,B,B,B],
    [[F,F,F,F],            [B,F,F,F,F,B],
     [F,F,F,F],    --->    [B,F,F,F,F,B],
     [F,F,F,F]]            [B,F,F,F,F,B],
                           [B,B,B,B,B,B]]

            F -> Represents pixels with the Face.
            B -> Represents the Background.
            padding allows us to include some background around the face.
            (padding constant 3 here causes some issue with some videos)
    '''
    p_w = 0
    p_h = 0
    if type(pad_constant) == int:
        p_h = h // pad_constant
        p_w = w // pad_constant
    elif type(pad_constant) == float:
        p_h = h // pad_constant[0]
        p_w = w // pad_constant[1]

    
    crop_h = (ymax + p_h) - max(ymin - p_h, 0)
    crop_w = (xmax + p_w) - max(xmin - p_w, 0)

    # Make the image square
    '''
    Makes the crop equal on all sides by adjusting the pad
    '''
    if crop_h > crop_w:
        p_h -= int(((crop_h - crop_w)/2))
    else:
        p_w -= int(((crop_w - crop_h)/2))

    # Extract the face from the frame
    crop = frame[max(ymin - p_h, 0):ymax + p_h, max(xmin - p_w, 0):xmax + p_w]
    
    # Check if out of bound and correct
    h, w = crop.shape[:2]
    if h > w:
        diff = int((h - w)/2)
        if diff > 0:         
            crop = crop[diff:-diff,:]
        else:
            crop = crop[1:,:]
    elif h < w:
        diff = int((w - h)/2)
        if diff > 0:
            crop = crop[:,diff:-diff]
        else:
            crop = crop[:,:-1]

    return crop