import os
import ssl
import toml
import logging
import requests
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from logging.config import fileConfig as logging_file_config

ALPHA_VANTAGE_LISTING_STATUS_FUNCTION = "LISTING_STATUS"
ALPHA_VANTAGE_TIME_SERIES_INTRADAY = "TIME_SERIES_INTRADAY"


class AlphaVantageService:
    def configure_external_market_api_service(self, **app_config):

        self.alpha_vantage_url: str = app_config.get("alpha_vantage_url")
        self.alpha_vantage_api_key: str = app_config.get("alpha_vantage_api_key")

    def get_company_overview_information(self, symbol: str):

        request_url = self.__prepare_request(
            function="OVERVIEW", parameters={"symbol": symbol}
        )

        response = requests.get(request_url)

        return response.content

    def get_intraday_trading_data(self, symbol: str, interval: str, window: str = None):

        output_size = "compact"

        if window == "month":
            output_size = "full"

        request_url = self.__prepare_request(
            function="TIME_SERIES_INTRADAY",
            parameters={
                "interval": interval,
                "symbol": symbol,
                "outputsize": output_size,
            },
        )
        response = requests.get(request_url)

        return response.content

    def __prepare_request(self, function: str, parameters: dict = None):

        request_parameters = (
            f"{self.__prepare_parameters(parameters)}" if parameters else ""
        )

        request_url = f"{self.alpha_vantage_url}/query?function={function}{request_parameters}&apikey={self.alpha_vantage_api_key}"

        return request_url

    def __prepare_parameters(self, parameters: dict) -> str:

        parameters_list = []

        for key, value in parameters.items():
            parameter_string = f"{key}={value}"
            parameters_list.append(parameter_string)

        concatenated_parameters = "&".join(parameters_list)

        return f"&{concatenated_parameters}"


class FlaskRestService(Flask):
    def configure_rest_server(self, **app_config):

        super().__init__(__name__)

        self.flask_server_hostname: str = app_config.get("flask_server_hostname")
        self.flask_server_port: str = app_config.get("flask_server_port")
        self.flask_server_ssl_cert: str = app_config.get("flask_server_ssl_cert")
        self.flask_server_ssl_key: str = app_config.get("flask_server_ssl_key")

    def start_rest_server(self):

        ssl_context = None

        if self.flask_server_ssl_cert and self.flask_server_ssl_key:

            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

            ssl_context.load_cert_chain(
                self.flask_server_ssl_cert, self.flask_server_ssl_key
            )

        self.run(
            host=self.flask_server_hostname,
            port=self.flask_server_port,
            ssl_context=ssl_context,
        )


class LoggerService:
    def configure_logger(self, **app_config):

        logging_file_config(app_config.get("logging_config_file"))

        self.logger = logging.getLogger()


class AppTomlConfigParserService:
    def parse_app_config_file(self, **app_config):
        self.app_config = toml.load(app_config.get("toml_app_config"))


class Application(
    AppTomlConfigParserService,
    LoggerService,
    AlphaVantageService,
    FlaskRestService,
):
    def __init__(self, **kwargs):

        super().parse_app_config_file(**kwargs)

        super().configure_logger(**self.app_config)

        self.logger.debug("App config loaded; logger cofigured.")

        self.logger.debug("configuring assets database service")

        super().configure_external_market_api_service(**self.app_config)

        self.logger.debug("configuring flask rest service")

        super().configure_rest_server(**self.app_config)

    # retrieves general information about a given company in
    # a json byte object
    def get_company_overview(self, **kwargs):

        company_overview_json_bytes = super().get_company_overview_information(**kwargs)

        return company_overview_json_bytes

    # retrieves intraday trading data for the last 30 days at
    # a given interval
    def get_detailed_recent_trading_data_for_asset(self, **kwargs):

        trading_data_bytes = super().get_intraday_trading_data(**kwargs)

        return trading_data_bytes

    def start_rest_service(self):

        super().start_rest_server()


def get_config_file_name():

    return os.getenv("TICKER_CONFIG_FILE")


def create_app():
    logger = logging.getLogger()

    logger.debug("getting config file name")

    config_file = get_config_file_name()

    logger.debug(f"Config file name is {config_file}")

    app = Application(toml_app_config=config_file)

    CORS(app)

    cache = Cache(config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300})

    cache.init_app(app)

    app.logger.debug("configuring rest server endpoints")

    @app.route("/company-overview/<symbol>", methods=["GET"])
    @cache.cached(timeout=300)
    def get_company_overview(symbol: str):

        company_overview = app.get_company_overview(symbol=symbol)

        return company_overview

    @app.route("/recent-trading-data/<symbol>/<interval>", methods=["GET"])
    @app.route("/recent-trading-data/<symbol>/<interval>/<window>", methods=["GET"])
    @cache.cached(timeout=300)
    def get_recent_trading_data(symbol: str, interval: str, window: str = None):

        trading_data = app.get_detailed_recent_trading_data_for_asset(
            symbol=symbol, interval=interval, window=window
        )

        return trading_data

    return app


if __name__ == "__main__":

    app = create_app()

    app.start_rest_server()
