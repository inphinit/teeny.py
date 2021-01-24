class Teeny():
    routes = {}
    codes = {}
    hasParams = False
    publicPath = None
    port = None
    debug = False
    codes = {}
    routes = {}
    code = 200
    routesPath = None
    server = None


    def __init__(self, port, address = 'localhost'):
        self.port = port
        self.address = address


    def action(self, methods, path, callback=None):
        if callback is not None:
            self.teenyAction(methods, path, callback)
        else:
            def wrapper(callback): # , *args, **kwargs
                self.teenyAction(methods, path, callback)

            return wrapper


    def teenyAction(self, methods, path, callback):
        if isinstance(methods, list): 
            for method in methods:
                self.teenyAction(method, path, callback)

        else:
            if path not in self.routes:
                self.routes[path] = {}

            if '<' in path:
                self.hasParams = True

            self.routes[path][methods.upper()] = callback


    def handlerCodes(self, codes, callback=None):
        if callback is not None:
            self.teenyHandlerCode(codes, callback)
        else:
            def wrapper(callback):
                self.teenyHandlerCode(codes, callback)

            return wrapper


    def teenyHandlerCodes(self, codes, callback):
        for code in codes:
            self.codes[code] = callback


    def setDebug(self, debug):
        self.debug = debug


    def setPublic(self, path):
        self.publicPath = path


    def setPattern(self, pattern, regex):
        if regex is None:
            del self.paramPatterns[pattern]
        else:
            self.paramPatterns[pattern] = regex


    def exec(self):
        print('exec')
        self.listen('HEAD', '/sugar')


    def listen(self, method, path):
        callback = None
        newCode = 0

        if path in self.routes:
            routes = self.routes[path]

            if method in routes:
                callback = routes[method]
            elif 'ANY' in routes:
                callback = routes['ANY']
            else:
                newCode = 405

        elif self.hasParams: # and self.teenyParams(request, response, method, path):
            return True
        else:
            newCode = 404

        if newCode != 0 and newCode in self.codes:
            callback = self.codes[newCode]

        if callback is not None:
            print('self.dispatch =>', callback)
            # self.dispatch(callback, newCode, null)
