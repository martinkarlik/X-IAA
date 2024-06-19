"""
Using distribution-based GIIAA to make inference on a few random samples from the subset of images.
"""

import os
import random

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

from src.nima.giiaa.base_module_giiaa import BaseModuleGIIAA

GIIAA_WEIGHTS = "models/giiaa-hist_200k_base-inceptionresnetv2_loss-0.078.hdf5"
AVA_DATASET_TEST_PATH = "../../PhotoCulling/data/ava/dataset/test/"
AVA_DATAFRAME_TEST_PATH = "../../data/ava/giiaa_metadata/dataframe_AVA_giiaa-hist_test.csv"


def get_weighted_mean(distribution):
    mean = 0.0
    for i in range(0, len(distribution)):
        mean += distribution[i] * (i + 1)
    return mean


if __name__ == "__main__":

    nima = BaseModuleGIIAA(custom_weights=GIIAA_WEIGHTS)
    nima.build()
    nima.compile()

    dataframe = pd.read_csv(AVA_DATAFRAME_TEST_PATH, converters={'label': eval})

    count_all = 10
    count_correct = 0
    eval_matrix = np.ndarray([count_all, 2])

    for i in tqdm(range(count_all)):

        predictions = []
        gts = []

        for ii in range(2):

            random_file = os.path.join(AVA_DATASET_TEST_PATH, random.choice(os.listdir(AVA_DATASET_TEST_PATH)))
            image = cv2.resize(cv2.imread(random_file), (224, 224)) / 255.0
            image = np.asarray(image)[np.newaxis, ...]

            gt = dataframe[dataframe["id"] == random_file].iloc[0]['label']
            prediction = nima.nima_model.predict(image)[0]

            # prediction_histogram = nima.predict(image)[0]

            predictions.append(get_weighted_mean(prediction))
            gts.append(get_weighted_mean(gt))

        eval_matrix[i, 0] = int(predictions[0] < predictions[1])
        eval_matrix[i, 1] = int(gts[0] < gts[1])

        if eval_matrix[i, 0] == eval_matrix[i, 1]:
            count_correct += 1

    print(eval_matrix)
    print("Correct {} out of {}.".format(count_correct, count_all))



