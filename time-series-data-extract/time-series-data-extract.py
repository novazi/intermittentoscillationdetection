## Authored by : Nova Zidane Ibrahim
## Created Date: 06/03/2023

import pandas as pd # data processing
import tsfel        # time series extraction
import warnings     # prevent warning
warnings.filterwarnings("ignore")
dataset = [] # list to collect the datasets to be extracted
labels  = [] # list to collect the labels from the dataset to be extracted
column  = [] # list to collect the XMEAS or XMV to be extracted
window  = [] # list to collect the window size to be extracted
stop1   = 0  # stop for file loop
stop2   = 0  # stop for XM loop
stop3   = 0  # stop for window loop
cgf     = tsfel.get_features_by_domain() 
try:
    # loop for input file name and label to be extracted
    while(stop1 != "No"):
        print("Enter the name of the TEP file to be extracted in csv format")
        file   = str(input('Write the file name along with ".csv":'))
        # loop for wrong format name
        while(file[-4:] != ".csv"):
            print("Sorry, the file format you entered is wrong")
            print("Please enter the name of the TEP file to be extracted in csv format")
            file   = str(input('Write the file name along with ".csv":'))
        print("Label description:")
        print('Write "0" for Normal data')
        print('Write "1" for data with disturbance 1')
        print('Write "2" for data with disturbance 2')
        print('Write "3" for data with distrubance 3')
        # you can add the description if you want and formatted as above 
        label = str(input('Label for the data that you want to extract:'))
        while(label != "0" and label != "1" and label != "2" and label != "3"):
            print("Sorry the label data you entered does not match")
            print("Please enter the label according to the label description")
            print("Label description:")
            print('Write "0" for Normal data')
            print('Write "1" for data with disturbance 1')
            print('Write "2" for data with disturbance 2')
            print('Write "3" for data with distrubance 3')
            label = str(input('Label for the data that you want to extract:'))
        labels.append(label)
        dataset.append(file)
        stop1 = str(input('Do you still want to enter more data? If not, type the word "No"!'))
    
    # loop for input XMEAS and XMV to be extracted
    print("------------------------------------------------------")
    while (stop2 != "No"):
        print("Select the desired XMEAS or XMV")
        print("For XMEAS, ranging from XMEAS 1 to XMEAS 41")
        print("For XMV, ranging from XMV 1 to XMV 12")
        print('Contoh penulisan: XMEAS 1, XMEAS 40, XMV 1, atau XMV 11')
        XM = str(input('Masukkan XMEAS atau XMV yang diinginkan:'))
        if ((XM[0:6] == "XMEAS ") and (1 <= int(XM[-2:]) <= 41) and (7 <= len(XM) <= 8)) or ((XM[0:4] == "XMV ") and (1 <= int(XM[-2:]) <= 12) and (5 <= len(XM) <= 6)):
            column.append(XM)
        else:
            print("Mohon maaf XMEAS atau XMV yang anda masukkan salah")
            print("Pilih XMEAS atau XMV yang diinginkan")
            print("Untuk XMEAS, mulai dari XMEAS 1 hingga XMEAS 41")
            print("Untuk XMEAS, mulai dari XMV 1 hingga XMV 11")
            print('Writing example: XMEAS 1, XMEAS 40, XMV 1, or XMV 11')
            XM = str(input('Enter the desired XMEAS or XMV:'))
        stop2 = str(input('Do you still want to enter more data? If not, type the word "No"!'))
    
    # loop for input window size to be extracted
    print("------------------------------------------------------")
    while (stop3 != "No"):
        print("Select the desired window size")
        print('Writing example: 100, 200, 300, or 500')
        size = input('Enter the desired window size:')
        while(size.isnumeric() != True):
            print("Sorry the window size you entered is wrong")
            print("Select the desired window size")
            print('Writing example: 100, 200, 300, or 500')
            size = int(input('Enter the desired window size:'))
        window.append(int(size))
        stop3 = str(input('Do you still want to enter more data? If not, type the word "No"!'))
    
    # result from the inputs
    print("------------------------------------------------------")
    print("Your Final Entry Results:")
    print("For files name to be extracted            :"+str(dataset))
    print("For labels to be extracted                :"+str(labels))
    print("For XMEAS or XMV to be extracted          :"+str(column))
    print("For the size of the window to be extracted:"+str(window))
    print("------------------------------------------------------")
    
    # extract the features from each datasets
    for k in range(len(window)):
        data    = pd.DataFrame()    
        for l in range(len(dataset)):
            df = pd.read_csv(dataset[k])
            for m in range(len(column)):
                result = tsfel.time_series_features_extractor(cgf, df[column[m]], window_size=window[k], verbose=0)
                result['Label'] = labels[l]
                data = pd.concat([data, result], axis=0, ignore_index=True)
        data.to_csv(r"Extraction Results for Window Size %.0d.csv" %(window[k]), index=False)
        print("Data Successfully Extracted and Merged for Window Size %.0d.csv" %(window[k]))
    print("All Data Extracted Successfully")
    print("------------------------------------------------------")
except:
    print("Sorry, you have entered the wrong data")