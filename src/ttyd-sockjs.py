#import json
#import logging
import os

from aiohttp import web, WSMsgType
import sockjs


TOPPAGE_HTML = open(os.path.join(os.path.dirname(__file__), '../ttyd/ttyd-1.7.2/html/dist/inline.html'), 'rb').read()

NOPATCH_HTML = open(os.path.join(os.path.dirname(__file__), 'nopatch.html'), 'rb').read()

class TtydServer:
    def __init__(self, use_sockjs=True):
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
                     print('WSMsgType.BINARY: ', end='')
                     await self._chat(msg.data, ws.send_bytes, True);
                 case _:
                     print('unexpected msg.type: 0x%x (WSMsgTye)' % msg.type)

        await ws.close()
        print('WebSoocket: connection closed')
        return ws

    async def sockjs_handler(self, msg, session):
        if session.manager is None:
            return

        match msg.type:
            case sockjs.MSG_OPEN:
                print('SockJS: connection ready')
            case sockjs.MSG_MESSAGE:
                print('sockjs.MSG_MESSAGE: ', end='')
                await self._chat(msg.data, session.send, False)
            case sockjs.MSG_CLOSE:
                print('SockJS: connection closing')
            case sockjs.MSG_CLOSED:
                print('SockJS: connection closed')
            case _:
                 print('unexpected msg.type: %d (sockjs)' % msg.type)

    async def _chat_send(self, data, sendfunc, bin):
        if bin:
            await sendfunc(data.encode('ascii'))
        else:
            # XXX await XXX
            sendfunc(data)

    async def _chat(self, data, sendfunc, isBytes):
        if isBytes:
            data = data.decode()

        print(data)
        if data[0] == '{':
            await self._chat_send('1/bin/sh (ttyd-MIKADO)', sendfunc, isBytes)
            await self._chat_send('2{}', sendfunc, isBytes)
            await self._chat_send('0prompt$ ', sendfunc, isBytes)
        else:
            await self._chat_send('0{}'.format(data[1:]), sendfunc, isBytes)


if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    ttyd = TtydServer(True)
    app = web.Application()
    app.add_routes([web.get('/', ttyd.toppage_handler),
                    web.get('/token', ttyd.token_handler)])
    if ttyd.use_sockjs:
        sockjs.add_endpoint(app, ttyd.sockjs_handler, name='ttyd', prefix='/sockjs')
    else:
        app.add_routes([web.get('/ws', ttyd.websocket_handler)])

    web.run_app(app, host='localhost', port=8000)
    # https://docs.aiohttp.org/en/stable/web_reference.html#utilities
