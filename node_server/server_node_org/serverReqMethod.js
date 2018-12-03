var http = require('http');
var fs = require('fs');
var url = require('url');
var qs = require('querystring');

var index2Page = fs.readFileSync('./index2.html', 'utf-8');

var server = http.createServer(function(req, res) {
    if (req.method == 'GET') {
        var urlParts = url.parse(req.url, true);

        console.log('---GET Request');
        console.log('nameは' + urlParts.query.name);
        console.log('ageは' + urlParts.query.age);

    } else {
        var body = '';
        req.on('data', function(data) {
            body += data;
        });
        req.on('end', function() {
            var params = qs.parse(body);

            console.log('---POST Request');
            console.log('nameは' + params.name);
            console.log('ageは' + params.age);
        });
    }

    res.writeHead(200, {'Content-Type':'text/html'});
    res.write(index2Page);
    res.end();
});

server.listen(1234);
console.log('サーバを起動しました');
