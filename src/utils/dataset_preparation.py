"""
Script to programmatically split the AVA dataset into a train and a test set.
We are using a fixed seed value to make the procedure reproducible.
"""

import os
import random

import PIL.Image
import tqdm

DATASET_PATH = "datasets/ava/images"
OUTPUT_DIRECTORY_PATH = "datasets/ava"

SEED = 91
TRAIN_TEST_SPLIT = 0.8


def generate_train_test(dataset_path, output_path, train_test_split=TRAIN_TEST_SPLIT, seed=SEED):

    filenames = os.listdir(dataset_path)
    filenames = [os.path.join(dataset_path, f) for f in filenames if f.endswith('.jpg')]

    random.seed(seed)

    filenames.sort()
    random.shuffle(filenames)

    split = int(train_test_split * len(filenames))
    train_filenames = filenames[:split]
    test_filenames = filenames[split:]

    print("train_filenames: {}".format(len(train_filenames)))
    print("test_filenames: {}".format(len(test_filenames)))

    filenames = {
        'train': train_filenames,
        'test': test_filenames
    }

    for split in filenames.keys():

        output_dir_split = os.path.join(output_path, split)

        if not os.path.exists(output_dir_split):
            os.mkdir(output_dir_split)
        else:
            print("Warning: dir {} already exists.".format(output_dir_split))

        print("Processing {} data, saving preprocessed data to {}.".format(split, output_dir_split))

        for filename in tqdm.tqdm(filenames[split]):
            try:
                image = PIL.Image.open(filename)
                image.save(os.path.join(output_dir_split, filename.split('/')[-1]))
            except Exception as e:
                print("We'll make it I swear! {}".format(e))

    print("Done building dataset.")


if __name__ == "__main__":
    generate_train_test(DATASET_PATH, OUTPUT_DIRECTORY_PATH)
