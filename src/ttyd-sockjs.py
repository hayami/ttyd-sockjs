#!/usr/bin/env python3.11
import argparse
#import json
#import logging
import os

from aiohttp import web, WSMsgType
import sockjs	# requires aio-libs/sockjs v0.13.0 (2024-06-13)


SOCKJS_HTML = open(os.path.join(os.path.dirname(__file__), 'html/ttyd-sockjs.html'), 'rb').read()
WEBSOCKET_HTML = open(os.path.join(os.path.dirname(__file__), 'html/ttyd-websocket.html'), 'rb').read()

class TtydServer:
    def __init__(self, once=False, use_sockjs=True):
        self.one_time_session = bool(once)
        self.use_sockjs = bool(use_sockjs)

    async def toppage_handler(self, request):
        if self.use_sockjs:
            return web.Response(body=SOCKJS_HTML, content_type='text/html')
        else:
            return web.Response(body=WEBSOCKET_HTML, content_type='text/html')

    async def token_handler(self, request):
        token = {'token': 'abc'}
        return web.json_response(token)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        print('WebSocket: connection ready')

        # TODO: self.one_time_session にまつわる実装

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

    async def sockjs_handler(self, manager, session, msg):
        if self.one_time_session:
            if self.one_time_session is True:
                self.one_time_session = session
            elif self.one_time_session is session:
                pass
            else:
                session.close()
                return

        match msg.type:
            case sockjs.MsgType.OPEN:
                print('SockJS: connection ready')

            case sockjs.MsgType.MESSAGE:
                print('sockjs.MsgType.MESSAGE: "%s"' % msg.data)
                ret = self._chat(msg.data)
                for data in ret:
                    if type(data) == str:
                        session.send(data)
                    else:
                        if data == 0:
                            session.close()

            case sockjs.MsgType.CLOSE:
                print('SockJS: connection closing')

            case sockjs.MsgType.CLOSED:
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
    #ttyd_formatter_class=lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=29)
    #parser = argparse.ArgumentParser(formatter_class=ttyd_formatter_class)

    parser = argparse.ArgumentParser()
    parser.add_argument('--host',       default='::1', dest='host',      action='store',      help='IP address or hostname to bind to (default: ::1)')
    parser.add_argument('-i',           default=None,  dest='sockpath',  action='store',      help='UNIX domain socket path', metavar='PATH')
    parser.add_argument('--interface',  default=None,  dest='sockpath',  action='store',      help='(same as above)', metavar='PATH')
    parser.add_argument('--no-sockjs',  default=False, dest='no_sockjs', action='store_true', help='Use WebSocket instead of SockJS')
    parser.add_argument('-o', '--once', default=False, dest='once',      action='store_true', help='Accept only one client and exit on disconnection')
    parser.add_argument('-p', '--port', default=7681,  dest='port',      action='store',      help='Port number or name to listen (default: 7681)')
    args = parser.parse_args();

    ttyd = TtydServer(once=args.once, use_sockjs=not(args.no_sockjs))
    app = web.Application()
    app.add_routes([web.get('/', ttyd.toppage_handler),
                    web.get('/token', ttyd.token_handler)])
    if args.no_sockjs:
        app.add_routes([web.get('/ws', ttyd.websocket_handler)])
    else:
        sockjs.add_endpoint(app, ttyd.sockjs_handler, name='ttyd', prefix='/sockjs')

    if args.sockpath:
        web.run_app(app, path=args.sockpath)
    else:
        web.run_app(app, host=args.host, port=args.port)

if __name__ == '__main__':
    main()
