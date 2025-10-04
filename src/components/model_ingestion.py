# okay so have to read data from a data source such as csv , mongoDb. split the data
# into train and test data into artifacts folder
#use this for ingetsion

#import the neccessary modules

#for os specific path
import os
import sys
from os.path import exists
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from src.components.model_transformation import Data_Transformation
from src.components.model_transformation import data_tranformation_config

from src.components.model_trainer import ModelTrainer


from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass


@dataclass
class data_config():
    train_data : str =os.path.join("artifacts", "train_data.csv")
    test_data : str =os.path.join("artifacts", "test_data.csv")
    raw_data : str =os.path.join("artifacts", "data.csv")


class data_ingestion():
    def __init__(self):

        self.ingestion_config=data_config()
        logging.info("ingestion started")

    def data_ingestion(self):

        try:
            df=pd.read_csv('notebook/data/stud 9.20.42 PM.csv')
            logging.info("Read csv data")
            #this created a folder of the train data csv and do the same for everything else
            os.makedirs(os.path.dirname(self.ingestion_config.train_data),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data,index=False,header=True)
            train_set,test_set=train_test_split(df,random_state=42,test_size=0.2)

            train_set.to_csv(self.ingestion_config.train_data,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data,index=False,header=True)

            logging.info("ingesrion complete")

            return (
                self.ingestion_config.train_data,
                self.ingestion_config.test_data
            )
        except Exception as e:
            logging.exception("error occured in ingestion")
            raise CustomException(e,sys)


if __name__=="__main__":
    obj=data_ingestion()
    train_data,test_data=obj.data_ingestion()

    dataTransformation=Data_Transformation()
    train_arr,test_arr,_=dataTransformation.initiate_data_transformation(train_data,test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))



