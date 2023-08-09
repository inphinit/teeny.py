"""Inspired by Inphinit and Teeny."""

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

GROUP_PARAM = '(?P<\\1><\\3>)'


class Teeny():
    """Simple route system."""

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
    paramPatterns = PARAM_PATTERNS.copy()


    def __init__(self, port, address='localhost'):
        """Configure server.

        Args:
            port: Set port.
            address: Set address.
        Returns:
            the square root of n.
        Raises:
            TypeError: if n is not a number.
            ValueError: if n is negative.
        """
        self.port = port
        self.address = address


    def action(self, methods, path, callback):
        """Register or remove a callback or script for a route.

        Args:
            method: Set the http method(s).
            path: Set the path.
            callback: Set the function or module.
        Returns:
            the square root of n.
        Raises:
            TypeError: if n is not a number.
            ValueError: if n is negative.
        """
        if callback is not None:
            self.__action(methods, path, callback)
        else:
            def wrapper(callback):
                self.__action(methods, path, callback)

            return wrapper


    def handlerCodes(self, codes, callback):
        """Handle HTTP status code from ISAPI (from apache2handler or fast-cgi).

        Args:
            codes: Set code errors.
            callback: Set function or module.
        Returns:
            the square root of n.
        Raises:
            TypeError: if n is not a number.
            ValueError: if n is negative.
        """
        if callback is not None:
            self.__handlerCodes(codes, callback)
        else:
            def wrapper(callback):
                self.__handlerCodes(codes, callback)

            return wrapper


    def setDebug(self, debug):
        """Enable or disable debug mode.

        Args:
            debug: Enable or disable debug mode.
        Returns:
            the square root of n.
        Raises:
            TypeError: if n is not a number.
            ValueError: if n is negative.
        """
        self.debug = debug


    def setPublic(self, path):
        """Set a folder with static files that can be accessed by url.

        Args:
            path: Set public path.
        Returns:
            the square root of n.
        Raises:
            TypeError: if n is not a number.
            ValueError: if n is negative.
        """
        self.publicPath = path


    def setPattern(self, pattern, regex):
        """Create or remove a pattern for URL slugs.

        Args:
            pattern: Set a pattern for URL slug params like this /foo/<var:pattern>.
            regex: Set a regex to a specific pattern.
        Returns:
            the square root of n.
        Raises:
            TypeError: if n is not a number.
            ValueError: if n is negative.
        """
        if regex is None:
            del self.paramPatterns[pattern]
        else:
            self.paramPatterns[pattern] = regex


    def exec(self):
        """Execute server."""
        # self.__listen('HEAD', '/sugar')
        pass


    def __action(self, methods, path, callback):
        path = '/' + path.lstrip('/')

        if '<' in path:
            routes = self.paramRoutes

            self.hasParams = True

            path = re.escape(path)
        else:
            routes = self.routes

        if path not in routes:
            routes[path] = {}

        if isinstance(methods, list):
            for method in methods:
                routes[path][method.upper()] = callback

        else:
            routes[path][methods.upper()] = callback


    def __handlerCodes(self, codes, callback):
        for code in codes:
            self.codes[code] = callback


    def __listen(self, method, path):
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
                return self.__params(method, path)
            except re.error as err:
                if self.debug:
                    print(err)

                code = 500

        if code is None:
            if self.publicPath:
                code = self.__Public(method, path)

                if code is None:
                    return
            else:
                code = 404

        self.__dispatch(method, path, callback, code, None)


    def __public(path):
        return 0


    def __params(self, method, pathinfo):
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
                    return self.__dispatch(method, pathinfo, callback, 200, params.groupdict())

        self.__dispatch(method, pathinfo, None, code, None)


    def __dispatch(self, method, path, callback, code, params):
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
                    result = callback(request, response, code)
                elif params is not None:
                    result = callback(request, response, params)
                else:
                    result = callback(request, response)

                print('result:', result)
            except:
                # teenyInfo(method, path, 500, ee)

                callback = self.codes[500]

                if callback:
                    self.__dispatch(request, response, method, path, callback, 500, None)
                    return
                else:
                    print(500)
        else:
            # self.__Info(method, path, code)
            print([method, path, 'no callback', code])
