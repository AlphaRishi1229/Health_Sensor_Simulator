"""The processor file."""
from typing import Dict, List
import logging

import pandas as pd
import ujson

from constants import (
    HOURLY_SECONDS,
    SEGMENTED_SECONDS,
    SENSOR_DATA_CSV_FILE,
    SENSOR_DATA_HOURLY_FILE,
    SENSOR_DATA_JSON_FILE
)


logger = logging.getLogger("PROCESSOR")


class Processor:
    def __init__(self, start_time: int) -> None:
        """The main processor class which will be processing the received sensor data and generate reports.

        Args:
            start_time (int): The current starting time of the processor.
        """
        self.start_timeframe: int = start_time
        self.end_timeframe: int = self.start_timeframe + SEGMENTED_SECONDS
        # Data required to generate reports.
        self.min_heart_rate: int = float("inf")
        self.max_heart_rate: int = float("-inf")
        self.sum_heart_rate: int = 0
        self.sum_resp_rate: int = 0
        self.timeframe_count: int = 0
        # Initialise the dataframe and the file to be written to.
        self.records_dataframe = pd.DataFrame()
        self.log_file = open(SENSOR_DATA_JSON_FILE, "w")

    def init_and_update(self, dataframe_data: List) -> None:
        """Reinitialises and updates properties of this processor class.

        Args:
            dataframe_data (List): The row of dataframe to be updated.
        """
        # Update new segment timeframe data.
        self.start_timeframe = self.end_timeframe
        self.end_timeframe = self.start_timeframe + SEGMENTED_SECONDS
        # Re initialise all data for this segment.
        self.min_heart_rate: int = float("inf")
        self.max_heart_rate: int = float("-inf")
        self.sum_heart_rate: int = 0
        self.sum_resp_rate: int = 0
        self.timeframe_count: int = 0
        # Update dataframe with new rows.
        self.records_dataframe = self.records_dataframe.append(dataframe_data, ignore_index=True)

    def transform_update_data(self, sensor_data: Dict) -> None:
        """The function transforms and adds the received sensor data and current data to a dataframe.

        Args:
            sensor_data (Dict): The data received by the sensor.
        """
        logger.info({
            "module": "Processor.transform_update_data",
            "msg": "ADDING_DATA_TO_DATAFRAME",
            "data": sensor_data
        })
        dataframe_data = [{
            "user_id": sensor_data["user_id"],
            "seg_start": self.start_timeframe,
            "seg_end": self.end_timeframe - 1,
            "avg_hr": self.sum_heart_rate // self.timeframe_count,
            "min_hr": self.min_heart_rate,
            "max_hr": self.max_heart_rate,
            "avg_rr": self.sum_resp_rate // self.timeframe_count
        }]
        self.init_and_update(dataframe_data)

    def process_sensor_data(self, sensor_data: Dict) -> None:
        """The main function which receives the recorded data from sensor and updates the current recorded data.

        Args:
            sensor_data (Dict): Data recorded and sent by the sensor.
        """
        logger.info({
            "module": "Processor.process_sensor_data",
            "msg": "PROCESSING_RECEIVED_DATA",
        })
        self.min_heart_rate = min(self.min_heart_rate, sensor_data["heart_rate"])
        self.max_heart_rate = max(self.max_heart_rate, sensor_data["heart_rate"])
        self.sum_heart_rate += sensor_data["heart_rate"]
        self.sum_resp_rate += sensor_data["respiration_rate"]
        self.timeframe_count += 1
        self.log_file.write(ujson.dumps(sensor_data) + "\n")

        if sensor_data["timestamp"] >= self.end_timeframe - 1:
            self.transform_update_data(sensor_data)

    def post_processor(self) -> None:
        """The post processor function which will be called after simulation ends.

        Here the files that we opened for writing is closed and the dataframe is converted to a csv.
        """
        logger.info({
            "module": "Processor.post_processor",
            "msg": "CLOSING_JSON_FILE_AND_CREATING_CSV_FILE",
        })
        self.log_file.close()
        self.records_dataframe.to_csv(SENSOR_DATA_CSV_FILE)
        print("GENERATED A 15 MINS SEGMENTED CSV")

    def generate_hourly_report(self, started_on: int, ended_on: int, user: str) -> None:
        """Generates a hourly report from the dataframe that we created above.

        Args:
            started_on (int): The timestamp when simulation started.
            ended_on (int): The timestamp of when simulation ended.
            user (str): The name of the user.
        """
        logger.info({
            "module": "Processor.post_processor",
            "msg": "CREATING_HOURLY_REPORT",
        })

        temp_dataframe = pd.DataFrame()
        while started_on <= ended_on - HOURLY_SECONDS:
            filter1 = self.records_dataframe["seg_start"] >= started_on
            filter2 = self.records_dataframe["seg_end"] <= started_on + HOURLY_SECONDS
            result_df = self.records_dataframe.loc[filter1 & filter2]

            dataframe_data = [{
                "user_id": user,
                "seg_start": started_on,
                "seg_end": started_on + (HOURLY_SECONDS - 1),
                "avg_hr": int(result_df["avg_hr"].mean()),
                "min_hr": int(result_df["min_hr"].min()),
                "max_hr": int(result_df["max_hr"].max()),
                "avg_rr": int(result_df["avg_rr"].mean())
            }]
            temp_dataframe = temp_dataframe.append(dataframe_data, ignore_index=True)

            started_on += HOURLY_SECONDS

        temp_dataframe.to_csv(SENSOR_DATA_HOURLY_FILE)

        print("GENERATED A HOURLY REPORT CSV")
