import numpy as np
import pandas as pd
import time
import argparse

from sklearn.linear_model import RidgeClassifierCV

from rocket import generate_kernels, apply_kernels

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--dataset_names", required = True)
parser.add_argument("-i", "--input_path", required = True)
parser.add_argument("-o", "--output_path", required = True)
parser.add_argument("-n", "--num_runs", type = int, default = 10)
parser.add_argument("-k", "--num_kernels", type = int, default = 10_000)
parser.add_argument("-m", "--kernels_model", type = str, default = "normal")

arguments = parser.parse_args()

dataset_names = np.loadtxt(arguments.dataset_names, "str")

results = pd.DataFrame(index = dataset_names,
                       columns = ["accuracy_mean",
                                  "accuracy_standard_deviation",
                                  "time_training_seconds",
                                  "time_test_seconds"],
                       data = 0)

results.index.name = "dataset"

print(f"START PROGRAMM".center(80, "="))

for dataset_name in dataset_names:

    print(f"{dataset_name}".center(80, "-"))

    print(f"Loading data")

    training_data = np.loadtxt(f"{arguments.input_path}/{dataset_name}/{dataset_name}_TRAIN.txt")
    X_training, Y_training = training_data[:, 1:], training_data[:, 0].astype(np.int32)
    X_training = np.nan_to_num(X_training, nan=0.0, posinf=0.0, neginf=0.0)

    test_data = np.loadtxt(f"{arguments.input_path}/{dataset_name}/{dataset_name}_TEST.txt")
    X_test, Y_test = test_data[:, 1:], test_data[:, 0].astype(np.int32)
    X_test = np.nan_to_num(X_test, nan=0.0, posinf=0.0, neginf=0.0)

    print("Train Test split is done")

    _results = np.zeros(arguments.num_runs)
    _timings = np.zeros([4, arguments.num_runs])

    for i in range(arguments.num_runs):

        input_length = X_training.shape[-1]
        kernels = generate_kernels(input_length, arguments.num_kernels, arguments.kernels_model)

        time_a = time.perf_counter()
        X_training_transform = apply_kernels(X_training, kernels)
        time_b = time.perf_counter()
        _timings[0, i] = time_b - time_a

        time_a = time.perf_counter()
        X_test_transform = apply_kernels(X_test, kernels)
        time_b = time.perf_counter()
        _timings[1, i] = time_b - time_a

        time_a = time.perf_counter()
        classifier = RidgeClassifierCV(alphas = np.logspace(-3, 3, 10))
        classifier.fit(X_training_transform, Y_training)
        time_b = time.perf_counter()
        _timings[2, i] = time_b - time_a

        time_a = time.perf_counter()
        _results[i] = classifier.score(X_test_transform, Y_test)
        time_b = time.perf_counter()
        _timings[3, i] = time_b - time_a

    print("Train Test split is done")

    results.loc[dataset_name, "accuracy_mean"] = _results.mean()
    results.loc[dataset_name, "accuracy_standard_deviation"] = _results.std()
    results.loc[dataset_name, "time_training_seconds"] = _timings.mean(1)[[0, 2]].sum()
    results.loc[dataset_name, "time_test_seconds"] = _timings.mean(1)[[1, 3]].sum()
    results.loc[dataset_name, "CI_0.05"] = _results.mean() -  (1.96 * _results.std()) / np.sqrt(len(_results))
    results.loc[dataset_name, "CI_0.95"] = _results.mean() +  (1.96 * _results.std()) / np.sqrt(len(_results))

print(f"END PROGRAMM".center(80, "="))

results.to_csv(f"{arguments.output_path}/results.csv")
