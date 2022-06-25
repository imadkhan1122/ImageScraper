#-----------------------IMPORT Python PACKAGES--------------------------------#

import pandas as pd
import os
import urllib.request as urllib
import shutil
from tqdm import tqdm
import csv

#------------------------Class IMAGE_SCRAPER----------------------------------#
class IMAGE_SCRAPER:
    # constructor dunction
    def __init__(self):
        # takes csv file as input from user
        self.PTH = str(input('Enter path to the input csv file: '))
        # path to output images files folder
        self.Opth = 'Images/'
        # check if the path to images is not exist 
        if not os.path.exists(self.Opth):
            # make folder is not made
            os.mkdir(self.Opth)
        # tegger main function
        self.main()
    #--------------------- READING DATA FROM INPUT CSV FILE-------------------#
    def Read_Data(self, pth):
        # empty data list for latter use
        DATA = []
        # read data from csv and save as pandas dataframe
        df = pd.read_csv(pth)
        
        # iterate over dataframe rows
        for index, row in df.iterrows():
            # save first column data to variable
            SaleChan = row[0]
            # alocate third column data to variable
            SKU      = row[2]
            # alocated sixth column data + QTY string to variable
            QTY      = 'QTY'+str(row[5])
            # alocated second column data to variable
            ORDER_ID = row[1]
            # building image names from multiple variables
            ImageName = str(SaleChan)+'-'+str(SKU)+'-'+str(QTY)+'-'+str(ORDER_ID)
            # making dictionay of all existing columns with additional two columns data
            # one for image name and second for image url
            DIC = {'Sales Channal':row[0], 'Order ID':row[1], 'Item Code/SKU':row[2],
                   'Print SKU':row[3], 'Print Url':row[4], 'Quantity':row[5], 
                   'Image Name':ImageName}
            
            # appending DIC to DATA list
            DATA.append(DIC)
        # returning DATA list as function output
        return DATA
    #-------------------------FUNCTION DOWNLOADING FILES----------------------#
    def Download_Files(self, pth, ImageName, ImageURL):
        # split image name into two parts
        ImgName = ImageURL.split('/')
        # split last part of image name by . to get image extension
        ImageEXT   = ImgName[-1].split('.')
        # make complete path where image will be downloaded
        ImagePth   = pth+'/'+ImageName+'.'+ImageEXT[1]
        # check if image is not already exists in folder
        if not os.path.exists(ImagePth):
        # download image file to images folder
          try:
              request = urllib.Request(ImageURL, headers={'User-Agent': 'Mozilla/5.0'})
              with urllib.urlopen(request) as response, open(ImagePth, 'wb') as out_file:
                  shutil.copyfileobj(response, out_file)
                  return str('Yes')
          except:
              return str('No')
        elif os.path.exists(ImagePth):
          return str('Yes')
    #-----------------------------------Main function-------------------------#
    def main(self):
        
        # save path to the pth variable
        pth = self.PTH
        if not os.path.exists(pth):
            print('file not exists')
        Opth = self.Opth
        # trigger Read_data function and save output as data variable
        data = self.Read_Data(pth)
        header = ['Sales Channal', 'Order ID', 'Item Code/SKU', 'Print SKU',
                  'Print Url', 'Quantity', 'Image Name', 'Image_Status']
        # open Output.csv file with new data points
        with open('Ouptput_With_Image_Status.csv', 'w', newline = '') as output_csv:
            # initialize rows writer
            csv_writer = csv.writer(output_csv)
            # write headers to the file
            csv_writer.writerow(header)
            # iterate over data
            for d in tqdm(data):
                # save image name to the variable
                ImageName  = d['Image Name']
                # save image url to variable
                ImageURL   = d['Print Url']
                # call Download files
                
                status = self.Download_Files(Opth, ImageName, ImageURL)
                if status == 'Yes':
                    d['Image_Status'] = 'Yes'
                #   # # write rows to csv file
                    csv_writer.writerow(d.values())
                elif status == 'No':
                    d['Image_Status'] = 'No'
                    # write rows to csv file
                    csv_writer.writerow(d.values())     
            # Display process completed message
            print('\n\n', '[INFO] PROCESS COMPLETED')
        
        return        

