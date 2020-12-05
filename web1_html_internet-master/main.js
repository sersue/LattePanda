var http = require('http');
var fs = require('fs');
var url = require('url');

var app = http.createServer(function(request,response){
    var _url = request.url;
    var queryData = url.parse(_url, true).query;//query 객체로 url중에서 ? 뒷부분
    var pathname = url.parse(_url,true).pathname; 
    
    
    if (pathname ==='/'){
      if(queryData.id == undefined){
        fs.readFile(`data/${queryData.id}`,'utf8',function(err,description){
        var title= 'Welcome';
        var description = 'Hello';
        var template = `
        <!doctype html>
        <html>
        <head>
          <title>WEB1 - ${title}</title>
          <meta charset="utf-8">
        </head>
        <body>
          <h1><a href="/">WEB</a></h1>
          <ol>
            <li><a href="/?id=HTML">HTML</a></li>
            <li><a href="/?id=CSS">CSS</a></li>
            <li><a href="/?id=JavaScript">JavaScript</a></li>
          </ol>
          <h2>${title}</h2>
          <p>${description}</p>
        </body>
        </html>
        `;
        response.writeHead(200);
        response.end(template); //queryData.id == query string의 ID값
    
        });
      }else{
        fs.readFile(`data/${queryData.id}`,'utf8',function(err,description){
          var title = queryData.id
          var template = `
        <!doctype html>
        <html>
        <head>
          <title>WEB1 - ${title}</title>
          <meta charset="utf-8">
        </head>
        <body>
          <h1><a href="/">WEB</a></h1>
          <ol>
            <li><a href="/?id=HTML">HTML</a></li>
            <li><a href="/?id=CSS">CSS</a></li>
            <li><a href="/?id=JavaScript">JavaScript</a></li>
          </ol>
          <h2>${title}</h2>
          <p>${description}</p>
        </body>
        </html>
        `;
        response.writeHead(200);
        response.end(template); //queryData.id == query string의 ID값
    
        });
      }
      } else{
      response.writeHead(404);//잘 연결이 되었는지, 연결 안되면 약속된 404 숫자를 서버에 전송
      response.end('Not Found');
    }
  

});
app.listen(3000);
