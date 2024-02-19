#import json
#import logging
import os

from aiohttp import web
import sockjs


CONSOLE_HTML = open(os.path.join(os.path.dirname(__file__), '../ttyd/ttyd-1.7.2/html/dist/inline.html'), 'rb').read()


async def token_handler(msg, session):
    if session.manager is None:
        return
    if msg.type == sockjs.MSG_OPEN:
        print("MSG_OPEN\n")
    elif msg.type == sockjs.MSG_MESSAGE:
        print("MSG_MESSAGE: %s\n" % msg.data)
    elif msg.type == sockjs.MSG_CLOSED:
        print("MSG_CLOSED\n")


def console(request):
    return web.Response(body=CONSOLE_HTML, content_type='text/html')


def token(request):
    return web.Response(body='{"token": "abc"}', content_type='application/json', charset='utf-8')


if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    app = web.Application()
    app.router.add_route('GET', '/', console)
    app.router.add_route('GET', '/token', token)
    sockjs.add_endpoint(app, token_handler, name='console', prefix='/sockjs/')

    web.run_app(app, host='localhost', port=8000)
    # https://docs.aiohttp.org/en/stable/web_reference.html#utilities
