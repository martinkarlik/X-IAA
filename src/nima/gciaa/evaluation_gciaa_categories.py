"""
Evaluation of within-category trained GCIAA model.
Evaluated on 20 233 within-category generated pairs from AVA dataset.
Performance of the within-category trained GCIAA model is compared
with the baseline GCIAA model with the GIIAA model as the image encoder.

                Baseline    |   GCIAA Categories
Loss:           0.4274      |   0.3328
Accuracy:       0.6751      |   0.6852
"""

import pandas as pd
from keras.preprocessing.image import ImageDataGenerator

from src.nima.gciaa.base_module_gciaa import BaseModuleGCIAA
from src.utils.generators import *

GIIAA_MODEL = "../../models/giiaa-hist_204k_base-inceptionresnetv2_loss-0.078.hdf5"
GCIAA_CATEGORIES_MODEL = "../../models/gciaa-cat_81k_base-giiaa_accuracy-0.710.hdf5"

AVA_DATASET_TEST_PATH = "../../PhotoCulling/data/ava/dataset/test/"
AVA_DATAFRAME_TEST_PATH = "../../data/ava/gciaa_metadata/dataframe_AVA_gciaa-cat_test.csv"

BASE_MODEL_NAME = "InceptionResNetV2"
BATCH_SIZE = 64


if __name__ == "__main__":

    # model = keras.models.load_model(WEIGHTS_PATH, custom_objects={"earth_movers_distance": earth_movers_distance})
    base = BaseModuleGCIAA(custom_weights=GCIAA_CATEGORIES_MODEL)
    base.build()
    base.compile()

    dataframe = pd.read_csv(AVA_DATAFRAME_TEST_PATH, converters={'label': eval})

    data_generator = ImageDataGenerator(rescale=1.0 / 255)

    test_generator = SiameseGeneratorCategories(
        generator=data_generator,
        dataframe=dataframe
    )

    accuracy = base.siamese_model.evaluate_generator(
        generator=test_generator.get_pairwise_flow_from_dataframe(),
        steps=test_generator.samples_per_epoch / test_generator.batch_size,
        verbose=1
    )

