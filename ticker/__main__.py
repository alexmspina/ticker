import ticker

if __name__ == "__main__":

    app = ticker.create_app()

    app.start_rest_server()
