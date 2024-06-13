'use strict';

const SockJS = require('sockjs-client');

function TtydSockJS(url, protocols) {
    this.textEncoder = new TextEncoder();
    this.textDecoder = new TextDecoder();

    this.onmessage_orig = function(event) {};
    this.onmessage_hook = function(event) {
        if (typeof(event.data) === 'string') {
            event.data = this.textEncoder.encode(event.data);
        } else {
            const fname = event.data.constructor.name;
            console.log('[ttyd-sockjs] onmessage(): unexpected object type: ' + fname);
        }
        return this.onmessage_orig(event);
    };
    Object.defineProperty(this, "onmessage", {
        get: function() {
            return this.onmessage_hook;
        },
        set: function(func) {
            this.onmessage_orig = func;
        }
    });

    const options = {};	// e.g. { transports: ["xhr-streaming", "xhr-polling"] }
    const pstr = JSON.stringify(protocols);
    const ostr = JSON.stringify(options);
    console.log(`[ttyd-sockjs] SockJS.call(this, ${url}, ${pstr}, ${ostr})`);
    SockJS.call(this, url, protocols, options);
}

TtydSockJS.prototype = Object.create(SockJS.prototype);
TtydSockJS.prototype.constructor = TtydSockJS;

TtydSockJS.CONNECTING = SockJS.CONNECTING;
TtydSockJS.OPEN = SockJS.OPEN;
TtydSockJS.CLOSING = SockJS.CLOSING;
TtydSockJS.CLOSED = SockJS.CLOSED;

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
