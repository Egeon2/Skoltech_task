from csv import Dialect
import numpy as np
from numba import njit, prange

# ------------------------------------------------------------------------ Создания ядер

@njit("Tuple((float64[:],int32[:],float64[:],int32[:],int32[:]))(int64,int64,unicode_type)")
def generate_kernels(input_length, num_kernels, kernel_model):

    candidate_lengths = np.array((7, 9, 11), dtype = np.int32)
    lengths = np.random.choice(candidate_lengths, num_kernels)

    weights = np.zeros(lengths.sum(), dtype = np.float64)
    biases = np.zeros(num_kernels, dtype = np.float64)
    dilations = np.zeros(num_kernels, dtype = np.int32)
    paddings = np.zeros(num_kernels, dtype = np.int32)

    a1 = 0

    for i in range(num_kernels):

        _length = lengths[i]

        # Реализация задания, выбор различных типов ядер

        # ----------------------------------------------

        if kernel_model == "normal":
            _weights = np.random.normal(0, 1, _length)

        elif kernel_model == "binary":
            binary_choices = np.array([-1.0, 1.0])
            _weights = np.random.choice(binary_choices, _length)

        elif kernel_model == "ternary":
            ternary_choices = np.array([-1.0, 0.0, 1.0])
            _weights = np.random.choice(ternary_choices, _length)

        else:
            raise ValueError("Unknown kernel_mode. Pick existing model: normal, binary, ternary")

        # ----------------------------------------------

        b1 = a1 + _length

        weights[a1:b1] = _weights - _weights.mean()

        biases[i] = np.random.uniform(-1, 1)

        dilation = 2**np.random.uniform(0, np.log2((input_length - 1) / (_length - 1)))
        dilation = np.int32(dilation)
        dilations[i] = dilation

        padding = ((_length - 1) * dilation) // 2 if np.random.randint(2) == 1 else 0
        paddings[i] = padding

        a1 = b1

    return weights, lengths, biases, dilations, paddings

# ------------------------------------------------------------------------ Расчет ppv, max на основе статьи

@njit(fastmath = True)
def apply_kernel(X, weights, length, bias, dilation, padding):

    input_length = len(X)

    output_length = (input_length + (padding * 2)) - ((length - 1) * dilation)

    ppv = 0
    _max = np.NINF

    end = (input_length + padding) - ((length - 1) * dilation)

    for i in range(-padding, end):

        sum = bias

        index = i

        for j in range(length):
            if index > -1 and index < input_length:
                sum = sum + weights[j] * X[index]
            index = index + dilation

        if sum > _max:
            _max = sum

        if sum > 0:
            ppv += 1

    return ppv / output_length, _max

# ------------------------------------------------------------------------ Применение к временным рядам

@njit("float64[:,:](float64[:,:],Tuple((float64[::1],int32[:],float64[:],int32[:],int32[:])))", parallel = True, fastmath = True)
def apply_kernels(X, kernels):

    weights, lengths, biases, dilations, paddings = kernels

    num_examples, _ = X.shape
    num_kernels = len(lengths)

    _X = np.zeros((num_examples, num_kernels * 2), dtype = np.float64)

    for i in prange(num_examples):

        a1 = 0
        a2 = 0

        for j in range(num_kernels):

            b1 = a1 + lengths[j]
            b2 = a2 + 2

            _X[i, a2:b2] = \
            apply_kernel(X[i], weights[a1:b1], lengths[j], biases[j], dilations[j], paddings[j])

            a1 = b1
            a2 = b2

    return _X
