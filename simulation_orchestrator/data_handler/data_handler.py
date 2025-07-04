from io import BytesIO
import pandas as pd
from dots_infrastructure.influxdb_connector import InfluxDBConnector
import zipfile


class DataHandler:
    def __init__(self, influxdb_connector: InfluxDBConnector):
        self.influxdb_connector = influxdb_connector

    def convert_points_to_df(self, points: dict) -> pd.DataFrame:
        df = pd.DataFrame(points)
        if not df.empty:
            df.drop(columns=["model_id", "simulation_id"], inplace=True)
        return df

    def get_simulation_results(
        self, measurement: str, simulation_id: str
    ) -> pd.DataFrame:
        query = (
            f"SELECT * FROM \"{measurement}\" WHERE simulation_id = '{simulation_id}'"
        )
        result_set = self.influxdb_connector.query(query)
        points = result_set.get_points(measurement=measurement)

        df = self.convert_points_to_df(points)
        return df

    def get_all_data_for_simulation_id(self, simulation_id: str) -> BytesIO:
        query = f'SHOW MEASUREMENTS ON "{self.influxdb_connector.influx_database_name}"'
        result_set = self.influxdb_connector.query(query)

        zip_buffer = BytesIO()
        has_data = False
        with zipfile.ZipFile(
            file=zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as zip_archive:
            for measurement in result_set.get_points():
                measurement_name = measurement["name"]
                measurement_dataframe = self.get_simulation_results(
                    measurement_name, simulation_id
                )
                if not measurement_dataframe.empty:
                    has_data = True
                    zip_archive.writestr(
                        zinfo_or_arcname=f"{simulation_id}_{measurement_name}.csv",
                        data=measurement_dataframe.to_csv(None),
                    )

        zip_buffer.seek(0)

        return zip_buffer if has_data else None
