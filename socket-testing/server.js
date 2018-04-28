#!/bin/env node

const fs  = require('fs');
const net = require('net');

const path= './test.sock';

if (fs.existsSync(path))
  fs.unlinkSync(path);
let s = net.createServer((c) => {
  console.log('client connected');

  c.on('data', (data) => {
    console.log(` >> received ${data}`);
    
    c.write('response');
  });
});
s.listen(path, () => {
  console.log('server listening at ./test.sock');
});


