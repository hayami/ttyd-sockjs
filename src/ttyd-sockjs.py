#!/usr/bin/env python3.11
import argparse
#import json
#import logging
import os

from aiohttp import web, WSMsgType
import sockjs


TOPPAGE_HTML = open(os.path.join(os.path.dirname(__file__), 'inline.html'), 'rb').read()

NOPATCH_HTML = open(os.path.join(os.path.dirname(__file__), 'nopatch.html'), 'rb').read()

class TtydServer:
    def __init__(self, once=False, use_sockjs=True):
        self.one_time_session = None if once else False
        self.use_sockjs = use_sockjs

    async def toppage_handler(self, request):
        if self.use_sockjs:
            return web.Response(body=TOPPAGE_HTML, content_type='text/html')
        else:
            return web.Response(body=NOPATCH_HTML, content_type='text/html')

    async def token_handler(self, request):
        token = {'token': 'abc'}
        return web.json_response(token)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        print('WebSocket: connection ready')

        async for msg in ws:
            match msg.type:
                 case WSMsgType.BINARY:
                     print('WSMsgType.BINARY: "%s"' % msg.data.decode())
                     ret = self._chat(msg.data.decode());
                     for data in ret:
                         if type(data) == str:
                             await ws.send_bytes(data.encode())
                         else:
                             if data == 0:
                                 await ws.close()
                 case _:
                     print('FIXME: WSMsgType: unexpected msg.type: 0x%x' % msg.type)

        await ws.close()
        print('WebSoocket: connection closed')
        return ws

    async def sockjs_handler(self, msg, session):
        if session.manager is None:
            return

        if self.one_time_session is not False:
            if self.one_time_session is None:
                self.one_time_session = session
            elif self.one_time_session is session:
                pass
            else:
                session.close()
                return

        match msg.type:
            case sockjs.MSG_OPEN:
                print('SockJS: connection ready')

            case sockjs.MSG_MESSAGE:
                print('sockjs.MSG_MESSAGE: "%s"' % msg.data)
                ret = self._chat(msg.data)
                for data in ret:
                    if type(data) == str:
                        session.send(data)
                    else:
                        if data == 0:
                            session.close()

            case sockjs.MSG_CLOSE:
                print('SockJS: connection closing')

            case sockjs.MSG_CLOSED:
                print('SockJS: connection closed')
                if self.one_time_session:
                    await session.manager.clear()
                    raise web.GracefulExit(0)	# TODO: スタックトレースが表示される

            case _:
                print('FIXME: SockJS: unknown msg.type: %d' % msg.type)

    def _chat(self, data):
        if data[0] == '{':
            return ['1/bin/sh (ttyd-MIKADO)',
                    '2{}',
                    '0prompt$ ']
        else:
            return ['0{}'.format(data[1:])]


def main():
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--once', help='accept only one client and exit on disconnection',
                        default=False, dest='once', action='store_true')
    parser.add_argument('--no-sockjs', help='use WebSocket instead of SockJS',
                        default=False, dest='no_sockjs', action='store_true')
    args = parser.parse_args();

    ttyd = TtydServer(once=args.once, use_sockjs=not(args.no_sockjs))
    app = web.Application()
    app.add_routes([web.get('/', ttyd.toppage_handler),
                    web.get('/token', ttyd.token_handler)])
    if ttyd.use_sockjs:
        sockjs.add_endpoint(app, ttyd.sockjs_handler, name='ttyd', prefix='/sockjs')
    else:
        app.add_routes([web.get('/ws', ttyd.websocket_handler)])

    web.run_app(app, host='localhost', port=8000)
    #web.run_app(app, path='/home/hayami/tmp/unix')
    # https://docs.aiohttp.org/en/stable/web_reference.html#utilities
    # https://stackoverflow.com/a/46377545
    #   unix:/var/sockets/$1.sock|http://%{HTTP_HOST}/
    #   あらかじめ umask 077 とかしておけば unix-soket の許可モードを制御できる


if __name__ == '__main__':
    main()
