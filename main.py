import asyncio

from aiohttp import web


def run_server(drop_tables=False, host='127.0.0.1', port=5000):
    """Prepares database and runs sever.

    See https://stackoverflow.com/a/51610341/27879617
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    import models
    loop.run_until_complete(models.prepare_database(drop=drop_tables))

    from app import app
    runner = web.AppRunner(app)

    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, host=host, port=port)
    loop.run_until_complete(site.start())

    loop.run_forever()


if __name__ == '__main__':
    from environs import env
    env.read_env()

    run_server(True)
