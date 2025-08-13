from main import run_server

if __name__ == '__main__':
    from environs import env
    env.read_env()

    run_server(True)
