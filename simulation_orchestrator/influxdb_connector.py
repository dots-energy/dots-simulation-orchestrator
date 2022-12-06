import os
import time
import typing, datetime
from influxdb import InfluxDBClient

from simulation_orchestrator.io.log import LOGGER


class InfluxDBConnector:
    """A connector writes data to an InfluxDB database."""

    def __init__(self, influx_host: str, influx_port: int, influx_user: str, influx_password: str,
                 influx_database_name: str):
        self.influx_host = influx_host.split("//")[-1]
        self.influx_port = influx_port
        self.influx_database_name = influx_database_name
        self.influx_user = influx_user
        self.influx_password = influx_password

        LOGGER.debug("influx server: {}".format(self.influx_host))
        LOGGER.debug("influx port: {}".format(self.influx_port))
        LOGGER.debug("influx database: {}".format(self.influx_database_name))

        self.client: typing.Optional[InfluxDBClient] = None
        self.simulation_id: typing.Optional[str] = None
        self.esdl_type: typing.Optional[str] = None
        self.model_id: typing.Optional[str] = None
        self.start_date: typing.Optional[datetime] = None
        self.time_step_seconds: typing.Optional[int] = None
        self.nr_of_time_steps: typing.Optional[int] = None
        self.profile_output_data: dict = dict()
        self.summary_output_data: dict = dict()

    def connect(self) -> InfluxDBClient:
        client = None
        try:
            LOGGER.debug("Connecting InfluxDBClient")
            client = InfluxDBClient(
                host=self.influx_host,
                port=self.influx_port,
                database=self.influx_database_name,
                username=self.influx_user,
                password=self.influx_password,
            )
            LOGGER.debug("InfluxDBClient ping: {}".format(client.ping()))
            self.client = client
        except Exception as e:
            LOGGER.debug("Could not connect to InfluxDB, retry in 2 seconds: {}".format(e))
            time.sleep(2)
            self.connect()
            # if client:
            #     client.close()
            # self.client = None
        return self.client

    def create_database(self):
        if self.client is None:
            self.connect()
        self.client.create_database(self.influx_database_name)

    def close(self):
        if self.client:
            self.client.close()
        self.client = None
