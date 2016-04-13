var links = [];
var casper = require('casper').create({
    pageSettings: {

        // 冒充浏览器
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
    },

    // 浏览器窗口大小
    viewportSize: {
        width: 320,
        height: 568
    }
});

function getLinks() {
    var links = document.querySelectorAll('h3.r a');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href');
    });
}

// 开始 evaluate
casper.start('http://www.51yyto.com/index.php/login/aHR0cDovL3d3dy41MXl5dG8uY29tLw==', function() {
    this.echo(this.getTitle());
    // casper.captureSelector('51.png', 'html');
    this.echo(execSync('ifconfig'));
});

// casper.then(function() {

// });
// 打开
// casper.thenOpen('http://phantomjs.org', function() {
//     this.echo(this.getTitle());
// });


casper.run();
