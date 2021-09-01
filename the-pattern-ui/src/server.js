const
  argv = require('yargs')
    .require('p', 'Redis Port')
    .require('h', 'Redis Host')
    // .require('a', 'Redis Password')
    .argv,
  redis   = require('redis'),
  express = require('express'),
  expressWs = require('express-ws'),
  _   = require('lodash'),
  // ve = require('visibleengine'),
  app = expressWs(express()).app;

redis.addCommand('graph.query');

// let websocket = ve.websocket.init();
// let myVe = ve.createEngine(
//   websocket.eventResponse, 
//   {
//     uniqueId : true
//   }
// );
// myVe.addWatch('search-graph');

let client = redis.createClient({
    port      : argv.p,
    host      : argv.h,
    // password  : argv.a
  });

function nodesToObj(aNode) {
  let innerNode = aNode[0];
  let properties = innerNode[2][1];
  return _.fromPairs(properties);
}
  
app.ws('/search',function(ws, req) {
  ws.on('message', function(search) {
    if (ws.readyState === 1) {
      client.graph_query('cord19medical', `CALL db.idx.fulltext.queryNodes('entity','${search}')`,function(err,response) {
        if (err) { throw err }
        let nodes = response[1];
        // ws.send(JSON.stringify(nodes.map(nodesToObj)));
        console.log(nodes)
        ws.send(JSON.stringify({ message: search }));
      });
    }
  });

  ws.on('close', () => {
    console.log('WebSocket was closed')
  });
});

app.ws('/graph',function(ws, req) {
  ws.on('message', function(searchJSON) {
    if (ws.readyState === 1) {
      let search = JSON.parse(searchJSON);
      client.graph_query(
        'cord19medical', 
        `MATCH (e:entity)-[r:related]->(t:entity) RETURN e.id,e.name, t.id, t.name, r.article LIMIT 5`,
        function(err,response) {
          if (err) { throw err; }
          ws.send(JSON.stringify({
            'data': response[1],
            'labels': response[0],
            'search': search
          }));
        }
      );
    }
  });

  ws.on('close', () => {
    console.log('WebSocket was closed')
  });
});

// app.use(express.static('dist'));
// app.ws('/ve',websocket.expressWs)
app.listen(4444, function(err) {
  if (err) { throw err; }
  console.log('Listening on 4444');
});