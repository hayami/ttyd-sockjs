'use strict';

const SockJS = require('sockjs-client');

function TtydSockJS(url, protocols) {
    const options = {};	// e.g. { transports: ["xhr-streaming", "xhr-polling"] }
    const pstr = JSON.stringify(protocols);
    const ostr = JSON.stringify(options);
    console.log(`[ttyd-sockjs] SockJS.call(this, ${url}, ${pstr}, ${ostr})`);
    SockJS.call(this, url, protocols, options);
    this.textDecoder = new TextDecoder();
}

TtydSockJS.prototype = Object.create(SockJS.prototype);
TtydSockJS.prototype.constructor = TtydSockJS;

TtydSockJS.prototype.send = function(data) {
    if (data.constructor === Uint8Array) {
        data = this.textDecoder.decode(data);
    } else {
        const fname = data.constructor.name;
        console.log('[ttyd-sockjs] send(): unexpected object type: ' + fname);
    }
    SockJS.prototype.send.call(this, data);
};

module.exports = { TtydSockJS };
