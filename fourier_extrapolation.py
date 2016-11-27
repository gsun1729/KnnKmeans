import numpy as np
import matplotlib.pyplot as pl
import csv, time
from numpy import fft
# code modified from Artem Tartakynov
# https://gist.github.com/tartakynov/83f3cd8f44208a1856ce


def fourierExtrapolation(historical_data_array, n_predict,n_harmonics):
    n = historical_data_array.size
    n_harm = n_harmonics            # number of harmonics in model
    t = np.arange(0, n)
    p = np.polyfit(t, historical_data_array, 1)         # find linear trend in historical_data_array
    x_notrend = historical_data_array - p[0] * t        # detrended historical_data_array
    x_freqdom = fft.fft(x_notrend)  # detrended historical_data_array in frequency domain
    f = fft.fftfreq(n)              # frequencies
    indexes = range(n)
    # sort indexes by frequency, lower -> higher
    indexes.sort(key = lambda i: np.absolute(f[i]))
 
    t = np.arange(0, n + n_predict)
    restored_sig = np.zeros(t.size)
    for i in indexes[:1 + n_harm * 2]:
        ampli = np.absolute(x_freqdom[i]) / n   # amplitude
        phase = np.angle(x_freqdom[i])          # phase
        restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)
    return restored_sig + p[0] * t
    
def main():
    n_predict = 3
    n_harmonics = 14
    window = 14
    filename = 'export_w14_chx_0x513CA9F162_pathdist.csv'



    # read in target data
    f = open(filename, 'rb') 
    historical_data = []
    try:
        reader = csv.reader(f) 
        for row in reader: 
            historical_data.append(float(row[0]))
    finally:
        f.close()
    historical_data_array = np.array(historical_data)
    
    
    # historical h_extrapolation
    h_extrapolation = fourierExtrapolation(historical_data_array, n_predict,n_harmonics)
    pl.figure(0)
    pl.plot(np.arange(0, h_extrapolation.size), h_extrapolation, 'r', label = 'Extrapolation')
    pl.plot(np.arange(0, historical_data_array.size), historical_data_array, 'b', label = 'Actual Data', linewidth = 2)
    pl.ylabel('Minimum Cluster Path Distance')
    pl.xlabel('Day')
    pl.legend()
    pl.show()


    # moving window extrapolation
    window_SSE = []

    nScans = np.size(historical_data_array)-window+1
    for scan in range(nScans):
        # obtain local history and perform extrapolation on each window
        local_history = historical_data_array[scan:scan+window]
        
        l_extrapolation = fourierExtrapolation(local_history,n_predict,n_harmonics)

        # predictions with actual future data
        local_prediction_history = historical_data_array[scan+window:scan+window+n_predict]

        temp = np.flipud(l_extrapolation)
        l_extrapolation_prediction =np.flipud(temp[0:n_predict])

        if l_extrapolation_prediction.size == local_prediction_history.size:
            window_SSE.append(np.sum(np.square(np.subtract(local_prediction_history,l_extrapolation_prediction)))/local_prediction_history.size)

        pl.figure(scan+1)
        pl.plot(np.arange(0+scan, l_extrapolation.size+scan), l_extrapolation, 'r', label = 'Extrapolation')
        pl.plot(np.arange(0, historical_data_array.size), historical_data_array, 'b', label = 'Actual Data', linewidth = 2)
        pl.ylabel('Minimum Cluster Path Distance')
        pl.xlabel('Day')
        pl.legend()
        pl.show()
    window_SSE_np = np.array(window_SSE)
    average_SSE = np.mean(window_SSE_np)
    STD_SSE = np.std(window_SSE_np)

    print "> Average SSE:\t"+str(average_SSE)+"\n"
    print "> SSE Standard Dev:\t"+str(STD_SSE)+"\n"
    print "> SSE History:\n"
    print window_SSE




    time.sleep(5)
    print "> Continuous Historical Extrapolation Beginning"
    c_window_SSE = []
    for c_scan in range(nScans):
        # obtain local history and perform extrapolation on each window
        local_history = historical_data_array[0:c_scan+window]
        
        l_extrapolation = fourierExtrapolation(local_history,n_predict,n_harmonics)

        # predictions with actual future data
        local_prediction_history = historical_data_array[c_scan+window:c_scan+window+n_predict]

        temp = np.flipud(l_extrapolation)
        l_extrapolation_prediction =np.flipud(temp[0:n_predict])

        if l_extrapolation_prediction.size == local_prediction_history.size:
            c_window_SSE.append(np.sum(np.square(np.subtract(local_prediction_history,l_extrapolation_prediction)))/local_prediction_history.size)

        pl.figure(c_scan+1)
        pl.plot(np.arange(0, l_extrapolation.size), l_extrapolation, 'r', label = 'Extrapolation')
        pl.plot(np.arange(0, historical_data_array.size), historical_data_array, 'b', label = 'Actual Data', linewidth = 2)
        pl.ylabel('Minimum Cluster Path Distance')
        pl.xlabel('Day')
        pl.legend()
        pl.show()

    c_window_SSE_np = np.array(c_window_SSE)
    average_SSE = np.mean(c_window_SSE_np)
    STD_SSE = np.std(c_window_SSE_np)

    print "> Average SSE:\t"+str(average_SSE)+"\n"
    print "> SSE Standard Dev:\t"+str(STD_SSE)+"\n"
    print "> SSE History:\n"
    print c_window_SSE
if __name__ == "__main__":
    main()