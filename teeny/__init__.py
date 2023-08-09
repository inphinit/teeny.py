import re

PARAM_PATTERNS = {
    'alnum': '[\\da-zA-Z]+',
    'alpha': '[a-zA-Z]+',
    'decimal': '\\d+\\.\\d+',
    'num': '\\d+',
    'noslash': '[^\\/]+',
    'nospace': '\\S+',
    'uuid': '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
    'version': '\\d+\\.\\d+(\\.\\d+(-[\\da-zA-Z]+(\\.[\\da-zA-Z]+)*(\\+[\\da-zA-Z]+(\\.[\\da-zA-Z]+)*)?)?)?'
}

GROUP_PARAM = r'(?P<\1><\3>)'


class Teeny():
    routes = {}
    paramRoutes = {}
    codes = {}
    hasParams = False
    publicPath = None
    port = None
    debug = False
    code = 200
    routesPath = None
    server = None
    maintenance = False
    paramPatterns = PARAM_PATTERNS.copy();


    def __init__(self, port, address = 'localhost'):
        self.port = port
        self.address = address


    def action(self, methods, path, callback = None):
        if callback is not None:
            self.teenyAction(methods, path, callback)
        else:
            def wrapper(callback):
                self.teenyAction(methods, path, callback)

            return wrapper


    def teenyAction(self, methods, path, callback):
        path = '/' + path.lstrip('/')

        if '<' in path:
            routes = self.paramRoutes

            self.hasParams = True

            path = re.escape(path)
        else:
            routes = self.routes

        if path not in routes:
            routes[path] = {};

        if isinstance(methods, list):
            for method in methods:
                routes[path][method.upper()] = callback

        else:
            routes[path][methods.upper()] = callback


    def handlerCodes(self, codes, callback=None):
        if callback is not None:
            self.teenyHandlerCode(codes, callback)
        else:
            def wrapper(callback):
                self.teenyHandlerCode(codes, callback)

            return wrapper


    def teenyHandlerCode(self, codes, callback):
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
        # self.teenyListen('HEAD', '/sugar')
        pass


    def teenyListen(self, method, path):
        if self.maintenance:
            print(503)
            print('Service Unavailable')
            return None

        code = None
        callback = None

        if path in self.routes:
            code = 200

            routes = self.routes[path]

            if method in routes:
                callback = routes[method]
            elif routes.ANY:
                callback = routes.ANY
            else:
                code = 405

        elif self.hasParams:
            try:
                return self.teenyParams(method, path)
            except re.error as err:
                if self.debug:
                    print(err)

                code = 500

        if code is None:
            if self.publicPath:
                code = self.teenyPublic(method, path)

                if code is None:
                    return
            else:
                code = 404

        self.teenyDispatch(method, path, callback, code, None)


    def teenyPublic(path):
        return 0


    def teenyParams(self, method, pathinfo):
        patterns = self.paramPatterns
        getParams = "[<](\\w+)(\\:(" + ("|".join(patterns.keys())) + ")|)[>]"

        callback = None
        code = 404

        for path, routes in self.paramRoutes.items():
            path = re.sub(getParams, GROUP_PARAM, path)
            path = path.replace('<>)', '.*?)')

            for pattern, value in patterns.items():
                path = path.replace('<' + pattern + '>)', value + ')')

            params = re.match('^' + path + '$', pathinfo)

            if params is not None:
                if method in routes:
                    callback = routes[method]
                elif method in routes:
                    callback = routes['ANY']

                if callback is None:
                    code = 405
                else:
                    return self.teenyDispatch(method, pathinfo, callback, 200, params.groupdict())

        self.teenyDispatch(method, pathinfo, None, code, None)


    def teenyDispatch(self, method, path, callback, code, params):
        print('\n<response>:')

        request = 'FAKE'
        response = 'FAKE'

        if code != 200 and code in self.codes:
            callback = self.codes[code]

        if callback is not None:
            print([method, path, callback, code, params])

            result = None

            try:
                if code != 200:
                    result = callback(request, response, code);
                elif params is not None:
                    result = callback(request, response, params);
                else:
                    result = callback(request, response);

                print('result:', result)
            except:
                # teenyInfo(method, path, 500, ee);

                callback = self.codes[500];

                if callback:
                    self.teenyDispatch(request, response, method, path, callback, 500, None)
                    return
                else:
                    print(500)
        else:
            # self.teenyInfo(method, path, code);
            print([method, path, 'no callback', code])
