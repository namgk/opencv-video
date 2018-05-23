var cp = require('child_process')
var fs = require("fs");


var net = require('net');
var client;

// stream.write('hello');
// stream.end();



let py1 = cp.spawn('python', ['-u', 'video.py'], {
  cwd: __dirname, detached: false
});

let py2 = cp.spawn('python', ['-u', 'video1.py'], {
  cwd: __dirname, detached: false
});

// py2.stdout.on('data', (data)=>{})

// node.onInput
// py1.stdout.pipe(py2.stdin)
py2.stdout.pipe(fs.createWriteStream('/dev/null'))
// return

let exit = false
let connected = false


// py2.on('close', ()=>{
//   console.log('close')
// })
// py1.on('close', ()=>{
//   console.log('close')
// })
// py1.on('error', ()=>{
//   console.log('err')
// })
py1.on('exit', ()=>{
  exit = true
  console.log('exit')
})
py2.on('exit', ()=>{
  exit = true
  console.log('exit')
})
// py2.on('error', ()=>{
//   console.log('err')
// })

var server = net.createServer(function(stream) {
  console.log('client connected')
  stream.on('data', function(c) {
    if (!exit)
      py2.stdin.write(c)
  });
  stream.on('end', function() {
    console.log('server disconnected')
    server.close();
  });
  // stream.on('error', ()=>{
  //   console.log('error')
  // })
  // stream.on('close', ()=>{
  //   console.log('close')
  // })
});

server.listen('/tmp/test.sock');

client = net.connect('/tmp/test.sock', ()=>{
  connected = true
  console.log('connected to server')
});

// client.on('error', ()=>{
//   console.log('errddor')
// })

// client.on('close', ()=>{
//     console.log('closes')
//   })

py1.stdout.on('data', data => {
  // node.send
  if (!exit)
    //write to client connection
    client.write(data);
  // py2.stdin.write(data)
})