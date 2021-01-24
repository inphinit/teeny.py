## under development

the project is not yet functional, it is just a preparation of the structure to be designed in the best possible way.

## Wrappers

Modules that will be used in the project:

- https://www.python.org/dev/peps/pep-0333/ (for production)
- https://docs.python.org/3/library/http.server.html (for development)

## Example

``` python
app = Teeny(4000)

app.setPublic('public')

@app.action('GET', '/')
def foo():
    print("foo!")


@app.action('ANY', '/test')
def bar():
    print("bar!")


@app.action([ 'GET', 'POST' ], '/what')
def bar():
    print("bar!")


app.action('HEAD', '/sugar', 'foo.py')


@app.handlerCodes([ 404, 405 ]);
def error_page(code):
    print("error page:", code)


app.exec()
```
