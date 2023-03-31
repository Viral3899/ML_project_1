
import sys
import os

from housing.exception.exception import HousingException
from housing.logger.logger import logging
from housing.constant import *

from housing.util.util import read_yaml_file
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig,\
    ModelEvaluationConfig, ModelPusherConfig, ModelTrainerConfig, TrainingPipelineConfig


class Configuration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH,
                 current_time_stamp=get_current_time_stamp()) -> None:

        try:
            self.config_info = read_yaml_file(file_path=config_file_path)

            self.training_pipeline_config = self.get_training_pipeline_config()

            self.time_stamp = current_time_stamp

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:

        try:

            training_pipline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]

            artifact_dir = os.path.join(
                ROOT_DIR, training_pipline_config[TRAINING_PIPELINE_NAME_KEY],
                training_pipline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipline_config = TrainingPipelineConfig(
                artifact_dir=artifact_dir)

            logging.info(
                f"Training Pipeline Config: {training_pipline_config}")

            return training_pipline_config

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        try:
            data_ingestion_config_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_config_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            artifact_dir = self.training_pipeline_config.artifact_dir

            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR_NAME,
                self.time_stamp
            )

            raw_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_DIR_KEY]
            )

            tgz_download_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_config_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )

            ingested_train_dir = os.path.join(
                ingested_dir,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY]
            )

            ingested_test_dir = os.path.join(
                ingested_dir,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY]
            )

            data_ingestion_config = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                tgz_download_dir=tgz_download_dir,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )

            logging.info(f"Data Ingestion Config: {data_ingestion_config}")

            return data_ingestion_config

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            data_validation_config_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir = os.path.join(
                artifact_dir, DATA_VALIDATION_ARTIFACT_DIR_NAME,
                self.time_stamp
            )

            schema_file_path = os.path.join(
                ROOT_DIR,
                data_validation_config_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
                data_validation_config_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )

            report_file_path = os.path.join(
                data_validation_artifact_dir,
                data_validation_config_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )

            report_page_file_path = os.path.join(
                data_validation_artifact_dir,
                data_validation_config_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]
            )

            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path
            )

            return data_validation_config

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_data_transforamtion_config(self) -> DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_transformation_artifact_dir = os.path.join(
                artifact_dir,
                DATA_TRANSFORMATION_ARTIFACT_DIR_KEY,
                self.time_stamp
            )

            data_transformation_config_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            add_bedroom_per_room = data_transformation_config_info[
                DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY]

            preprocessed_object_file_path = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY]
            )

            transformed_train_dir = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY]
            )

            transformed_test_dir = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY]

            )

            data_transformation_config = DataTransformationConfig(
                add_bedroom_per_room=add_bedroom_per_room,
                preprocessed_object_file_path=preprocessed_object_file_path,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir
            )

            logging.info(
                f"Data transformation config: {data_transformation_config}")
            return data_transformation_config

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            model_trainer_artifact_dir = os.path.join(artifact_dir,
                                                      MODEL_TRAINER_ARTIFACT_DIR,
                                                      self.time_stamp
                                                      )

            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            trained_model_file_path = os.path.join(model_trainer_artifact_dir,
                                                   model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
                                                   model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY]
                                                   )

            model_config_file_path = os.path.join(model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
                                                  model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY]
                                                  )

            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_trainer_config = ModelTrainerConfig(trained_model_file_path=trained_model_file_path,
                                                      base_accuracy=base_accuracy,
                                                      model_config_file_path=model_config_file_path)

            logging.info(f"Model Trainer Config {model_trainer_config}")

            return model_trainer_config

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass
