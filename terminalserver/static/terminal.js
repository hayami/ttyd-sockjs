window.addEventListener("load", function() {

  const clientOptions = {
    fontFamily: 'monospace',
    cursorBlink: true,
  }

  const command = {
    // from client to server
    AUTH: 'A',
    INPUT: 'I',

    // from server to client
    OUTPUT: 'O',
  }

  const textEncoder = new TextEncoder();

  const terminal = new Terminal(clientOptions);
  terminal.open(document.getElementById('terminal-container'));
  terminal.onData(onTerminalData);
  terminal.onBinary(onTerminalBinary);

  const fitAddon = new FitAddon.FitAddon();
  terminal.loadAddon(fitAddon);
  fitAddon.fit();

  terminal.write('Connecting to the terminal server');

  function onTerminalData(data) {
    if (!socket || socket.readyState !== socket.OPEN) return;
    if (typeof data !== 'string') {
      throw new Error(`onTerminalData: unexpected data type: ${typeof data}`);
    }
    socket.send(textEncoder.encode(command.INPUT + data));
  }

  function onTerminalBinary(data) {
    throw new Error('onTerminalBinary: unexpected call');
  }

  const socket = new WebSocket('ws');
  socket.binaryType = 'arraybuffer';
  socket.onerror = onSocketError;
  socket.onopen = onSocketOpen;
  socket.onclose = onSocketClose;
  socket.onmessage = onSocketMessage;

  function onSocketError(ev) {
    throw new Error(`onSocketError code=${ev.code}`);
  }

  function onSocketOpen(ev) {
    console.log('[terminalserver] socket connection opened');

    const msg = JSON.stringify({
      token: 'XXX TOKEN XXX',
      columns: terminal.cols,
      rows: terminal.rows
    });

    socket.send(textEncoder.encode(command.AUTH + msg));

    terminal.reset();
    /* 効果未確認 */ terminal.focus();
  }

  function onSocketClose(ev) {
    console.log(`[terminalserver] socket connection closed with code: ${ev.code}`);
  }

  function onSocketMessage(ev) {
    if (!(ev.data instanceof ArrayBuffer)) {
      throw new Error('ASSERTION FAILED: unexpected data type');
    }
    const buf = new Uint8Array(ev.data);
    const cmd = buf[0];
    const data = buf.slice(1);

    switch (String.fromCharCode(cmd)) {
    case command.OUTPUT:
      terminal.write(data);
      break;
    default:
      throw new Error('onSocketMessage: cmd=' + cmd);
    }
  }

});


/*
	ASSERTION FAILED: should not be reached here

	terminal.on*
	------------
	terminal.onBell
	terminal.onBinary
	terminal.onCursorMove
	terminal.onData
	terminal.onKey
	terminal.onLineFeed
	terminal.onRender
	terminal.onResize
	terminal.onScroll
	terminal.onSelectionChange
	terminal.onTitleChange
	terminal.onWriteParsed
*/
