# from ...teeny import Teeny

from teeny import Teeny


def test():
    print('[[1234]]')


app = Teeny(8080)

app.action('GET', '/sugar', test)


@app.action('POST', '/sugar')
def xyz():
    print(12345)


app.action('GET', '/^,$,|,[,],(,),:,<,>,!,?,#/<abc>', test)


@app.action('GET', '/blog/<name>-<id:num>')
def article():
    print(12345)


## app.exec()

app.listen('GET', '/^,$,|,[,],(,),:,<,>,!,?,#/A1000')
