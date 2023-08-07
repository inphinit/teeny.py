# from ...teeny import Teeny

from teeny import Teeny


def test(request, response, params=None):
    return 'get sugar'


app = Teeny(8080)

app.action('GET', '/sugar', test)


@app.action('POST', '/sugar')
def xyz(request, response):
    return 'add sugar to coffee'


app.action('GET', '/^,$,|,[,],(,),:,<,>,!,?,#/<abc>', test)


@app.action('GET', '/blog/<name>-<id:num>')
def article(request, response, params):
    return 'Hello world blog'


## app.exec()

app.teenyListen('GET', '/sugar')
app.teenyListen('POST', '/sugar')

app.teenyListen('GET', '/^,$,|,[,],(,),:,<,>,!,?,#/foobar')
app.teenyListen('GET', '/blog/john-1000')
