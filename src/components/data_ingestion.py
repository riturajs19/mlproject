import os ## Handles files paths and directory management
import sys ## used for error handling in Custom Exception
from src.exception import CustomException # Imports cusotm error handling class
from src.logger import logging # import logger for debugging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass # A decorator used to store data
## it removes continuous use __init__, __repr__ and other dunder methods because it auto generates it

from src.components.data_tranformation import DataTransformation # Preprocess the data(handling missing values,scaling)
from src.components.data_tranformation import DataTransformationConfig # defines how data should be performed

from src.components.model_trainer import ModelTrainerConfig # Defines parameter to train ML Model
from src.components.model_trainer import ModelTrainer # Handles model training and evaluation
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")
## Artifacts- it refers to file or data produced at diffrent stages in ML Pipeline like model.pkl, logs.txt

class DataIngestion:# Reads the dataset, initiate process and split into train and test
    def __init__(self):
        self.ingestion_config=DataIngestionConfig() ## Calling the class

    def initiate_data_ingestion(self):# Reads the dataset, initiate process and split into train and test
        logging.info("Entered the data ingestion method or component") # Helps tracking the pipeline execution
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe') # If file is missing , then exception will be raised

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
        ## Creating the necessary folder and exist_ok = True provides no error is raised if directory exists
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
        ##Saves the raw dataset to self.ingestion_config.raw_data_path.
        ## index=False ensures the index column is not saved.
        ## header=True ensures column names are included.


            logging.info("Train test split initiated") # Tracks the step
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True) 
            ## train_set is saved at self.ingestion_config.train_data_path.
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            ##test_set is saved at self.ingestion_config.test_data_path.
             ## Helps in avoiding respitting
            logging.info("Inmgestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys) # If any error is occured then custom exception is raised
        
if __name__=="__main__": ## Script only runs when executed directly
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion() ## Reads and split data

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
     ## Prepares data for modelling
    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
    ## Trains and evaluates the model