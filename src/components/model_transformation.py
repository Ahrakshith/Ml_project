import os
import sys
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import numpy as np

from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.utils import save_object


from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass


@dataclass
class data_tranformation_config():
    preprocessor_obj_file=os.path.join('artifacts','prepocessor_obj.pkl')

#we create the pipeline here and then use another class to call that

class Data_Transformation():
    def __init__(self):
        self.data_transformation_config = data_tranformation_config()

    def preprocessing(self):
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('standardScaler',StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy="most_frequent")),
                    ('oneHotEncode',OneHotEncoder())
                ]
            )

            logging.info("pipeline created")

            preprocessor=ColumnTransformer([
                ('numericalColumns',num_pipeline,numerical_columns),
                ('categoricalCoulmns',cat_pipeline,categorical_columns)
            ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_data_path,test_data_path):
        try:
            preproceesing_obj=self.preprocessing()

            train_df=pd.read_csv(train_data_path)
            test_df=pd.read_csv(test_data_path)


            target_column="math_score"

            input_feature_train_df=train_df.drop(columns=[target_column],axis=1)
            target_feature_df=train_df[target_column]

            input_feature_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_df[target_column]


            input_feature_transform=preproceesing_obj.fit_transform(input_feature_train_df)
            input_feature_test_transform=preproceesing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_transform, np.array(target_feature_df)]
            test_arr = np.c_[input_feature_test_transform, np.array(target_feature_test_df)]

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file,
                obj=preproceesing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file,
            )

        except Exception as e:
            raise CustomException(e,sys)


