import pathlib
import json
import ticker
import pytest
import requests
from flask import Flask

# REUSABLE TEST VALUES

TEST_TOML_CONFIG_FILE_NAME = "test_config.toml"
TEST_LOGGING_CONFIG_FILE_NAME = "test_logging.cfg"

asset_dict_list = [
    {"symbol": "ASSET1", "asset_name": "Asset 1"},
    {"symbol": "ASSET2", "asset_name": "Asset 2"},
    {"symbol": "ASSET3", "asset_name": "Asset 3"},
    {"symbol": "ASSET4", "asset_name": "Asset 4"},
]


class MockAlphaVantageService(ticker.AlphaVantageService):
    def get_intraday_trading_data(self, **kwargs):

        return f"intraday trading data for {kwargs.get('symbol')} at {kwargs.get('interval')}"

    def get_company_overview_information(self, **kwargs):

        return f"Overview information about company {kwargs.get('symbol')}"


class MockFlaskRestService(ticker.FlaskRestService):
    def start_rest_server(self):
        pass


class MockApplication(
    ticker.Application,
    MockAlphaVantageService,
    MockFlaskRestService,
):
    "Useful for testing Application interfaces"


@pytest.fixture
def mock_ticker_application_toml_config_file_path(
    tmp_path_factory,
    pytestconfig,
):

    test_dir_path = tmp_path_factory.mktemp("test")

    d = test_dir_path / "tests"
    d.mkdir()
    toml_app_config_file_path = d / TEST_TOML_CONFIG_FILE_NAME

    logging_config_file_path = d / TEST_LOGGING_CONFIG_FILE_NAME

    write_mock_app_toml_config_file(
        toml_app_config_file_path,
        logging_config_file_path,
        pytestconfig,
    )

    write_mock_logger_config_file(logging_config_file_path)

    return toml_app_config_file_path


def write_mock_app_toml_config_file(
    config_file,
    logging_config_file,
    pytestconfig,
):

    config_text = f"""alpha_vantage_url = "https://www.fakeapi.com"
alpha_vantage_api_key = "12345ABC"
flask_server_hostname = "127.0.0.1"
flask_server_port = "8000"
flask_server_ssl_cert = "fake_cert.pem"
flask_server_ssl_key = "fake_key.pem"
logging_config_file = "{logging_config_file}"
"""

    write_text_to_tmp_path_file(content=config_text, dest=config_file)


def write_mock_logger_config_file(config_file):

    config_text = f"""[loggers]
keys=root

[logger_root]
handlers=console
level=DEBUG

[formatters]
keys=console

[formatter_console]
format=[%(asctime)s] [%(process)s] [%(levelname)s] %(message)s
class=logging.Formatter
datefmt=%Y-%m-%d %H:%M:%S %z

[handlers]
keys=console

[handler_console]
class=StreamHandler
formatter=console
level=DEBUG
args=(sys.stdout,)
    """

    write_text_to_tmp_path_file(content=config_text, dest=config_file)


def write_text_to_tmp_path_file(content: str, dest: pathlib.Path):

    dest.write_text(content)


@pytest.fixture
def mock_app(mock_ticker_application_toml_config_file_path, tmp_path_factory):

    config_path = str(mock_ticker_application_toml_config_file_path)

    app = MockApplication(toml_app_config=config_path)

    return app


def test_ticker_application_interface_get_company_overview_information_for_asset(
    mock_app,
):

    company_data = mock_app.get_company_overview(symbol="TEST")

    assert company_data == "Overview information about company TEST"


def test_ticker_application_interface_get_detailed_recent_trading_data_for_asset(
    mock_app,
):

    trading_data = mock_app.get_detailed_recent_trading_data_for_asset(
        symbol="test", interval="time"
    )

    assert trading_data == "intraday trading data for test at time"


def test_ticker_application_interface_start_rest_service(mock_app):

    result_none = mock_app.start_rest_service()

    assert result_none is None


# ALPHA VANTAGE SERVICE TESTS


class MockRequestsResponse:
    def __init__(self, content):

        self.content = content


ibm_company_overview_information_json_content = json.dumps(
    {
        "Symbol": "IBM",
        "AssetType": "Common Stock",
        "Name": "International Business Machines Corporation",
        "Description": "International Business Machines Corporation provides integrated solutions and services worldwide. Its Cloud & Cognitive Software segment offers software for vertical and domain-specific solutions in health, financial services, supply chain, and asset management, weather, and security software and services application areas; and customer information control system and storage, and analytics and integration software solutions to support client mission critical on-premise workloads in banking, airline, and retail industries. It also offers middleware and data platform software, including Red Hat that enables the operation of clients' hybrid multi-cloud environments; and Cloud Paks, WebSphere distributed, and analytics platform software, such as DB2 distributed, information integration, and enterprise content management, as well as IoT, Blockchain and AI/Watson platforms. The company's Global Business Services segment offers business consulting services; system integration, application management, maintenance, and support services for packaged software; and finance, procurement, talent and engagement, and industry-specific business process outsourcing services. Its Global Technology Services segment provides IT infrastructure and platform services; and project, managed, outsourcing, and cloud-delivered services for enterprise IT infrastructure environments; and IT infrastructure support services. The company's Systems segment offers servers for businesses, cloud service providers, and scientific computing organizations; data storage products and solutions; and z/OS, an enterprise operating system, as well as Linux. Its Global Financing segment provides lease, installment payment, loan financing, short-term working capital financing, and remanufacturing and remarketing services. The company was formerly known as Computing-Tabulating-Recording Co. The company was incorporated in 1911 and is headquartered in Armonk, New York.",
        "CIK": "51143",
        "Exchange": "NYSE",
        "Currency": "USD",
        "Country": "USA",
        "Sector": "Technology",
        "Industry": "Information Technology Services",
        "Address": "One New Orchard Road, Armonk, NY, United States, 10504",
        "FullTimeEmployees": "345900",
        "FiscalYearEnd": "December",
        "LatestQuarter": "2021-03-31",
        "MarketCapitalization": "128435003392",
        "EBITDA": "15822000128",
        "PERatio": "24.0448",
        "PEGRatio": "1.5466",
        "BookValue": "23.938",
        "DividendPerShare": "6.52",
        "DividendYield": "0.0453",
        "EPS": "5.978",
        "RevenuePerShareTTM": "82.734",
        "ProfitMargin": "0.0728",
        "OperatingMarginTTM": "0.1232",
        "ReturnOnAssetsTTM": "0.0376",
        "ReturnOnEquityTTM": "0.2536",
        "RevenueTTM": "73779003392",
        "GrossProfitTTM": "35575000000",
        "DilutedEPSTTM": "5.978",
        "QuarterlyEarningsGrowthYOY": "-0.192",
        "QuarterlyRevenueGrowthYOY": "0.009",
        "AnalystTargetPrice": "143.82",
        "TrailingPE": "24.0448",
        "ForwardPE": "13.1579",
        "PriceToSalesRatioTTM": "1.75",
        "PriceToBookRatio": "6.0047",
        "EVToRevenue": "2.4183",
        "EVToEBITDA": "13.1523",
        "Beta": "1.2262",
        "52WeekHigh": "148.38",
        "52WeekLow": "101.8909",
        "50DayMovingAverage": "141.8923",
        "200DayMovingAverage": "129.3559",
        "SharesOutstanding": "893523008",
        "SharesFloat": "891968098",
        "SharesShort": "25132045",
        "SharesShortPriorMonth": "27652123",
        "ShortRatio": "3.97",
        "ShortPercentOutstanding": "0.03",
        "ShortPercentFloat": "0.0282",
        "PercentInsiders": "0.131",
        "PercentInstitutions": "57.739",
        "ForwardAnnualDividendRate": "6.56",
        "ForwardAnnualDividendYield": "0.0456",
        "PayoutRatio": "0.7593",
        "DividendDate": "2021-06-10",
        "ExDividendDate": "2021-05-07",
        "LastSplitFactor": "2:1",
        "LastSplitDate": "1999-05-27",
    }
)


def alpha_vantage_company_overview_information_json_response(request_url):

    json_content = ibm_company_overview_information_json_content

    return MockRequestsResponse(content=json_content)


@pytest.fixture
def alpha_vantage_service():

    alpha_vantage_service = ticker.AlphaVantageService()

    alpha_vantage_service.configure_external_market_api_service(
        alpha_vantage_url="https://www.faketesturl.com", alpha_vantage_api_key="12345"
    )

    yield alpha_vantage_service


def test_alpha_vantage_service_get_company_overview_information(
    monkeypatch, alpha_vantage_service
):

    monkeypatch.setattr(
        requests, "get", alpha_vantage_company_overview_information_json_response
    )

    actual_company_overview = alpha_vantage_service.get_company_overview_information(
        symbol="IBM"
    )

    assert actual_company_overview == ibm_company_overview_information_json_content


def alpha_vantage_intraday_trading_json_response(request_url):

    if "full" in request_url:
        return MockRequestsResponse(content="month_testing")

    return MockRequestsResponse(content="testing")


def test_alpha_vantage_service_get_intraday_trading_data(
    monkeypatch, alpha_vantage_service
):

    monkeypatch.setattr(requests, "get", alpha_vantage_intraday_trading_json_response)

    actual_trading_data = alpha_vantage_service.get_intraday_trading_data(
        "TEST", "5min"
    )

    expected_trading_data = "testing"

    assert actual_trading_data == expected_trading_data


def test_alpha_vantage_service_get_intraday_trading_data_full_month(
    monkeypatch, alpha_vantage_service
):

    monkeypatch.setattr(requests, "get", alpha_vantage_intraday_trading_json_response)

    actual_trading_data = alpha_vantage_service.get_intraday_trading_data(
        "TEST", "5min", "month"
    )

    expected_trading_data = "month_testing"

    assert actual_trading_data == expected_trading_data


def test_alpha_vantage_service_prepare_request(alpha_vantage_service):

    actual_request_url = alpha_vantage_service._AlphaVantageService__prepare_request(
        function="TESTING", parameters={"key": "value"}
    )

    expected_request_url = (
        "https://www.faketesturl.com/query?function=TESTING&key=value&apikey=12345"
    )

    assert actual_request_url == expected_request_url


def test_alpha_vantage_service_prepare_parameters(alpha_vantage_service):

    actual_parameters_string = (
        alpha_vantage_service._AlphaVantageService__prepare_parameters(
            parameters={"key1": "value1", "key2": "value2", "key3": "value3"}
        )
    )

    expected_parameters_string = "&key1=value1&key2=value2&key3=value3"

    assert actual_parameters_string == expected_parameters_string


# FLASK REST SERVICE TESTS


@pytest.fixture
def environment_vars(monkeypatch, mock_ticker_application_toml_config_file_path):

    monkeypatch.setenv(
        "TICKER_CONFIG_FILE", str(mock_ticker_application_toml_config_file_path)
    )


@pytest.fixture
def app_with_configured_routes(environment_vars):

    app = ticker.create_app()

    return app


@pytest.fixture
def flask_rest_service_test_client(app_with_configured_routes):

    app_with_configured_routes.config["TESTING"] = True

    with app_with_configured_routes.test_client() as client:

        yield client


def test_flask_rest_service_get_company_overview(
    flask_rest_service_test_client, monkeypatch
):

    monkeypatch.setattr(
        requests, "get", alpha_vantage_company_overview_information_json_response
    )

    actual_company_overview = (
        flask_rest_service_test_client.get("/company-overview/IBM")
        .get_data()
        .decode("utf-8")
    )

    assert actual_company_overview == ibm_company_overview_information_json_content


def test_flask_rest_service_get_recent_trading_data_compact_route(
    flask_rest_service_test_client, monkeypatch
):

    monkeypatch.setattr(requests, "get", alpha_vantage_intraday_trading_json_response)

    actual_trading_data = (
        flask_rest_service_test_client.get("/recent-trading-data/TEST/5min")
        .get_data()
        .decode("utf-8")
    )

    assert actual_trading_data == "testing"


def test_flask_rest_service_get_recent_trading_data_full_route(
    flask_rest_service_test_client, monkeypatch
):

    monkeypatch.setattr(requests, "get", alpha_vantage_intraday_trading_json_response)

    actual_trading_data = (
        flask_rest_service_test_client.get("/recent-trading-data/TEST/5min/month")
        .get_data()
        .decode("utf-8")
    )

    assert actual_trading_data == "month_testing"


def test_create_app_returned_ticker_app(app_with_configured_routes):

    assert type(app_with_configured_routes) is ticker.Application


def test_ticker_application_is_subclass_of_flask():

    assert issubclass(ticker.Application, Flask)


def test_get_config_file_name(
    environment_vars, mock_ticker_application_toml_config_file_path
):

    actual_config_file = ticker.get_config_file_name()

    expected_config_file = str(mock_ticker_application_toml_config_file_path)

    assert actual_config_file == expected_config_file
