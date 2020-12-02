import http.server
import io
import itertools
import json
import logging
import socketserver
import sys
import urllib.parse

logger = logging.getLogger(__name__)


class JSONHandler(http.server.BaseHTTPRequestHandler):

    protocol_version = 'HTTP/1.1'

    api = None

    def do_GET(self):

        request = JSONRequest('GET', self.path)

        response = self.process_request(request)

        self.respond(response)

    def do_POST(self):

        try:

            clen = int(self.headers['Content-Length'])

            content = self.rfile.read(clen).decode('utf-8')

            payload = json.loads(content)

        except (ValueError, KeyError):

            self.respond(JSONResponse.error('Invalid JSON payload'), code=400)

        else:

            request = JSONRequest('POST', self.path, payload)

            response = self.process_request(request)

            self.respond(response)

    def do_DELETE(self):

        request = JSONRequest('DELETE', self.path)

        response = self.process_request(request)

        self.respond(response)

    def process_request(self, request):

        try:

            response = self.api.handle_request(request)

            return response

        except NotFound:

            return JSONResponse.error('No such resource', code=404)

        except MethodNotAllowed:

            return JSONResponse.error('Method not allowed', code=405)

        except Exception:

            logger.exception('Unhandled error')

            return JSONResponse.error('Unhandled error', code=500)

    def respond(self, response):

        self.send_response(response.code)

        headers, content = response.prepare()

        for key, value in headers:

            self.send_header(key, value)

        self.end_headers()

        self.wfile.write(content)


class JSONRequest:

    def __init__(self, method, raw_path, payload=None):

        self.method = method

        self.raw_path = raw_path

        self.payload = payload

        _, _, self.path, _, self.query, _ = urllib.parse.urlparse(

            'http://server' + raw_path

        )


class JSONResponse:

    def __init__(self, code, payload):

        self.code = code

        self.payload = payload

    @classmethod
    def success(cls, data, code=200):

        payload = {'ok': True, 'data': data}

        return cls(code, payload)

    @classmethod
    def error(cls, message, code=400):

        payload = {'ok': False, 'error': message}

        return cls(code, payload)

    def prepare(self):

        content = json.dumps(self.payload, indent=2).encode('utf-8')

        headers = [

            ('Content-Type', 'application/json'),

            ('Content-Length', len(content)),

        ]

        return headers, content


class NotFound(Exception):

    pass


class MethodNotAllowed(Exception):

    pass


class QuotesAPI:

    def __init__(self, initial_quotes):

        self._initial_quotes = initial_quotes

        self._quotes = {}

        self._quote_id_seq = None

        self._reset_state()

    def _reset_state(self):

        self._quote_id_seq = itertools.count(1)

        self._quotes = {

            qid: {'id': qid, 'text': text}

            for text, qid in zip(self._initial_quotes, self._quote_id_seq)

        }

    def handle_request(self, request):

        if request.method not in ('GET', 'POST', 'DELETE'):

            raise MethodNotAllowed

        if request.path == '/reset':

            if request.method != 'POST':

                raise MethodNotAllowed

            return self.reset_all()

        if request.path == '/quotes':

            if request.method == 'POST':

                return self.add_quote(request.payload)

            elif request.method == 'GET':

                return self.list_quotes()

            raise MethodNotAllowed

        if request.path.startswith('/quotes/'):

            _, _, qid_string = request.path.partition('/quotes/')

            try:

                quote_id = int(qid_string)

            except ValueError:

                raise NotFound

            if quote_id not in self._quotes:

                raise NotFound

            if request.method == 'GET':

                return self.retrieve_quote(quote_id)

            elif request.method == 'DELETE':

                return self.remove_quote(quote_id)

            raise MethodNotAllowed

        raise NotFound

    def reset_all(self):

        self._reset_state()

        return JSONResponse.success(None)

    def add_quote(self, quote_payload):

        if 'text' not in quote_payload:

            return JSONResponse.error('Missing required field "text"')

        text = quote_payload['text']

        if not isinstance(text, str):

            return JSONResponse.error(

                'Invalid type for field "text", expected string'

            )

        qid = next(self._quote_id_seq)

        new_quote = {'id': qid, 'text': text}

        self._quotes[qid] = new_quote

        if len(self._quotes) > 18:

            self._quotes = None

        return JSONResponse.success(new_quote, code=201)

    def list_quotes(self):

        ordered_quotes = sorted(

            self._quotes.values(), key=lambda q: str(q['id'])

        )

        return JSONResponse.success(ordered_quotes)

    def retrieve_quote(self, quote_id):

        quote = self._quotes[quote_id]

        return JSONResponse.success(quote)

    def remove_quote(self, quote_id):

        del self._quotes[quote_id]

        return JSONResponse.success(None)


# Borrowed from Python 3.7

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):

    daemon_threads = True


def main():

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    server_class = ThreadingHTTPServer

    handler_class = JSONHandler

    interface = '127.0.0.1'

    port = 6543

    server_address = (interface, port)

    api = QuotesAPI([

        'We have nothing to fear but fear itself!',

        'All work and no play makes Jack a dull boy.',

        'Travel is fatal to prejudice, bigotry, and narrow-mindedness.',

    ])

    # XXX Hack the API instance onto the handler class directly.

    #     Really ugly, but if I wanted something robust I wouldn't use the

    #     stdlib's server anyway.

    handler_class.api = api

    httpd = server_class(server_address, handler_class)

    logger.info('Starting server on %s:%s' % server_address)

    httpd.serve_forever()


if __name__ == '__main__':

    main()
