# Ticker

A REST service for finacial market data.

## Table of Contents
---
* [Configuring the Service](#configuring-the-service)
* [API Documentation](#api-documentation)

<br/>

### Configuring the Service

The ticker service is configured using a `.toml` file. The path to the configuration file needs to be defined using the `TICKER_CONFIG_FILE` environment variable.

#### TOML Configuration Parameters

```
alpha_vantage_url = "https://www.fakeapi.com"
alpha_vantage_api_key = "12345ABC"
flask_server_hostname = "127.0.0.1"
flask_server_port = "8000"
flask_server_ssl_cert = "fake_cert.pem"
flask_server_ssl_key = "fake_key.pem"
logging_config_file = "logging.cfg"
```

<br/>

### API Documentation

The ticker service utilizes a **REST** based interface to handle client requests.

#### Available Requests
#### Company Overview Information

`GET /company-overview/<company symbol>`

| **Parameter**    | **Type** | **Description**                                             | **Allowed Values**                                                  |
| ---------------- | -------- | ----------------------------------------------------------- | ------------------------------------------------------------------- |
| `company symbol` | `string` | **Required**. Ticker symbol of a company listed in a market | Any ticker symbol for a company currently listed on a stock market. |

#### Intraday Time Series Trading Data for the Previous Month

`GET /recent-trading-data/<company symbol>/<trading interval>/<time-span>`

| **Parameter**      | **Type** | **Description**                                                                                                                                                            | **Allowed Values**                                                  |
| ------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `company symbol`   | `string` | **Required**. Ticker symbol of a company listed in a market                                                                                                                | Any ticker symbol for a company currently listed on a stock market. |
| `trading interval` | `string` | **Required**. The trading data point frequency.                                                                                                                            | `1min`, `5min`, `15min`, `30min`, `60min`                           |
| `time-span`        | `string` | **Optional**. If provided, will return an extended set of data points, which roughly span the last month. If not provided, only the first 100 data points will be provided | `month`                                                             |


`<trading interval>` - a standard trading chart interval from the following list `5min`, `15min`, `30min`, `60min`

<br/>
