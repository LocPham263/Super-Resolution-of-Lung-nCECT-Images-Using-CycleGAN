import os
import shutil
import numpy as np
import SimpleITK as sitk
import scipy.ndimage as ndimage
from tqdm import tqdm
import matplotlib.pyplot as plt
import cv2
import h5py
import pandas as pd
from PIL import Image

from lung_seg import mask

BASE_DIR = '/home/avitech-pc4/RevGAN/datasets/'
data_folder = 'lung_COPD_3D/'
save_folder = 'lung_COPD/'
data_ls = sorted(os.listdir(BASE_DIR + data_folder))
save_ls = sorted(os.listdir(BASE_DIR + save_folder))

def CT2JPG(data_path, save_path, start, end):
    ct = sitk.GetArrayFromImage(sitk.ReadImage(data_path))
    ct[ct > 1024] = 1024
    ct[ct < -1024] = -1024
    for id in range (start, end):
        cv2.imwrite(save_path[:-7] + '_' + str(id) + '.tiff',ct[id])
        # sitk.WriteImage(sitk.GetImageFromArray(ct[id]), save_path[:-7] + '_' + str(id) + '.nii.gz')

# img = Image.open('/home/avitech-pc4/RevGAN/datasets/lung_COPD/trainA/p001_diag_30.tiff')

# # img = sitk.GetArrayFromImage(sitk.ReadImage('/home/avitech-pc4/RevGAN/datasets/lung_COPD/trainA/p001_diag_30.tiff'))
# print(img.size, type(img), img.format, type(img.getchannel(1).load()[1,1]))

# cv2.imwrite('/home/avitech-pc4/RevGAN/checkpoints/lung_COPD/web/images/p001_diag_30.tiff',np.array(img))
# im = Image.fromarray(image_numpy)
# im.save(img_path)

for __, folder in enumerate(data_ls):
    # for id, file in enumerate(sorted(os.listdir(BASE_DIR + data_folder + folder))):
    file_ls = sorted(os.listdir(BASE_DIR + data_folder + folder))
    for id in range(0,4,2):
        ct = sitk.GetArrayFromImage(sitk.ReadImage(BASE_DIR + data_folder + folder + '/' + file_ls[id]))
        seg = sitk.GetArrayFromImage(sitk.ReadImage(BASE_DIR + data_folder + folder + '/' + file_ls[id+1]))

        # Only keep slide with high portion of the lung
        if id == 0:
            for i in range (112):
                if 100*np.sum(seg[i])/(160*120) > 43:
                    CT2JPG(data_path=BASE_DIR + data_folder + folder + '/' + file_ls[id], 
                            save_path=BASE_DIR + save_folder + 'trainA/' + file_ls[id],
                            start = i, end = 103)
                    break
            CT2JPG(data_path=BASE_DIR + data_folder + folder + '/' + file_ls[id], 
                            save_path=BASE_DIR + save_folder + 'trainA/' + file_ls[id],
                            start = 35, end = 103)
                    
        elif id == 2:
            for i in range (112):
                if 100*np.sum(seg[i])/(160*120) > 35:
                    CT2JPG(data_path=BASE_DIR + data_folder + folder + '/' + file_ls[id], 
                        save_path=BASE_DIR + save_folder + 'trainB/' + file_ls[id],
                        start = i, end = 101)
                    break
            CT2JPG(data_path=BASE_DIR + data_folder + folder + '/' + file_ls[id], 
                        save_path=BASE_DIR + save_folder + 'trainB/' + file_ls[id],
                        start = 27, end = 101)    
            
        # # UNCOMMENT THIS CODE FOR LUNG AND LUNG LOBES SEGMENTATION
        # # Code for lung segmentation
        # ct_sitk = sitk.ReadImage(BASE_DIR + data_folder + folder + '/' + file)
        # model = mask.get_model('unet', 'LTRCLobes')
        # lung_pred = mask.apply(ct_sitk,model)
        # # lung_pred = mask.apply_fused(ct_sitk)
        # lung_pred[lung_pred > 0] = 1
        # src_lung_label = sitk.GetImageFromArray(lung_pred)
        # src_lung_label.CopyInformation(ct_sitk)
        # sitk.WriteImage(src_lung_label, BASE_DIR + data_folder + folder + '/' + file[:-7] + '_seg.nii.gz')













        # if file != 'CT_diag_final.nii.gz' and file != 'CT_spectct_final.nii.gz':
        #     os.remove(BASE_DIR + folder + '/' + file)
        # prefix = BASE_DIR + folder + '/'
        # if file == 'CT_diag_final.nii.gz':
        #     if idx+2 < 10:
        #         os.rename(prefix + file, prefix + 'p00'+str(idx+1)+'_diag.nii.gz')
        #     else:
        #         os.rename(prefix + file, prefix + 'p0'+str(idx+1)+'_diag.nii.gz')
        # else:
        #     if idx+2 < 10:
        #         os.rename(prefix + file, prefix + 'p00'+str(idx+1)+'_spectct.nii.gz')
        #     else:
        #         os.rename(prefix + file, prefix + 'p0'+str(idx+1)+'_spectct.nii.gz')

        # for i in range (112):
        #     if 100*np.sum(seg[i])/(160*120) > 43 and id == 0:
        #         print(file_ls[id], i)
        #         break
        #     elif 100*np.sum(seg[i])/(160*120) > 35 and id == 2:
        #         print(file_ls[id], i)
        #         break

# img = cv2.imread('/home/avitech-pc4/RevGAN/datasets/horse2zebra/trainA/n02381460_128.jpg')
# print(img.shape)