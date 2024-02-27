from src import create_app

app = create_app()


if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default= 2025, type= int, help = 'port to start')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port, debug=True)