import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer # Allows to apply diffrent transformations to diffrent features
from sklearn.impute import SimpleImputer # Handle missing values
from sklearn.pipeline import Pipeline # helps creating sequence of transformations
from sklearn.preprocessing import OneHotEncoder,StandardScaler 

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object # Saves preprocessing pipeline for later use

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation: # Created to handle feature transformation
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self): # Creates a data preprocessing pipeline
        '''
        This function is responsible for data trnasformation
        
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(               # For numerical columns
                steps=[
                ("imputer",SimpleImputer(strategy="median")), #For numerical columns it will impute median for missing values
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(            # For categorical columns

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")), # Fills missing value with most frequent category
                ("one_hot_encoder",OneHotEncoder()), # Converts categorical into numerical
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1) # X.train
            target_feature_train_df=train_df[target_column_name]# Y.train

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1) # X.test
            target_feature_test_df=test_df[target_column_name] # Y.test

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df) # X_train_scaled
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)# Y_train_scaled

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ] # Concatenate it 
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj # Saves the preprocessing file

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)