import pandas as pd
import numpy as np
from PIL import Image
from scipy import stats
from multiprocessing import Pool
import os

"""
A script that segments a image into the different tram colors, where each
pixel will be categorised as it's most likely tram sign color. 
It runs in parallel to decrease the time it takes to segment every image.
"""

def get_mvn():
    mvn = []
    data = pd.read_csv("sign_colors_v1.csv")

    for sign in range(1,12):
        data_sign = data.loc[data.sign == sign,["R","G","B"]]
        sigma = np.cov(data_sign,rowvar=False)
        mu = np.mean(data_sign)
        dist = stats.multivariate_normal(mean=mu, cov=sigma)
        mvn.append(dist)
    return mvn

class ImageSegmenter:
    def __init__(self): 
        self.mvn = get_mvn()
        self.mu = [np.array([175., 187., 203.]),
                   np.array([214., 190.,  39.]),
                   np.array([ 44.,  99., 171.]),
                   np.array([ 64., 106.,  94.]),
                   np.array([185.,  54.,  75.]),
                   np.array([193., 118.,  81.]),
                   np.array([126.,  98.,  97.]),
                   np.array([126.,  77., 103.]),
                   np.array([ 88., 171., 208.]),
                   np.array([145., 185., 121.]),
                   np.array([71., 73., 76.])]

    def segment_image(self, mat):
        height, width = mat.shape[:2]
        seg_mat = np.zeros_like(mat)
        for m in range(height):
            for n in range(width):
                x = mat[m,n,:]
                highest_freq = 0
                sign = 1
                for it, dist in enumerate(self.mvn):
                    if dist.pdf(x) > highest_freq:
                        highest_freq = dist.pdf(x)
                        sign = it
                seg_mat[m,n,:] = self.mu[sign]
        return seg_mat

    def work_parallel(self, directories, workers):
        with Pool(processes = workers) as pool:
            pool.map(self.segment_directory, 
                [dir for dir in directories])

        
    def segment_directory(self, directory):
        for file in os.listdir(directory):
            im = Image.open(f"{directory}/{file}") 
            # if file.split(".")[-1] == "jpg":
            #     im = im.transpose(method=Image.ROTATE_270)
            mat = np.asarray(im)
            seg_mat = self.segment_image(mat)
            outdir = f"./model2_easy_xtra_seg/{directory.split('/')[-1]}/{file}"
            Image.fromarray(seg_mat).save(outdir)
            print(outdir)

    
def main():
    workers = 11
    directory = "./model2_easy_xtra"
    directories = []
    for dir in os.listdir(directory):
        directories.append(f"{directory}/{dir}")
    img_seg = ImageSegmenter()
    img_seg.work_parallel(directories, workers)



if __name__=="__main__":
    main()


    
        


