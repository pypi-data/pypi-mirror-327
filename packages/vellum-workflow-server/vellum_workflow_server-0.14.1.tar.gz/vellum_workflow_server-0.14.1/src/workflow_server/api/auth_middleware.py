import json
from typing import Any, Dict

from flask import Flask, Request, Response
import jwt
from jwt import ExpiredSignatureError

from workflow_server.config import VEMBDA_PUBLIC_KEY, is_development


class AuthMiddleware:
    def __init__(self, app: Flask) -> None:
        self.app = app

    def __call__(self, environ: Dict[str, Any], start_response: Any) -> Any:
        try:
            request = Request(environ)
            if not request.path.startswith("/healthz") and not is_development():
                token = request.headers.get("X-Vembda-Signature")
                if token:
                    jwt.decode(token, VEMBDA_PUBLIC_KEY, algorithms=["RS256"])
                else:
                    res = Response(json.dumps({"detail": "Signature missing"}), mimetype="application/json", status=401)
                    return res(environ, start_response)

        except ExpiredSignatureError:
            res = Response(
                json.dumps({"detail": "Signature token has expired. Please obtain a new token."}),
                mimetype="application/json",
                status=401,
            )
            return res(environ, start_response)
        except Exception as e:
            res = Response(
                json.dumps({"detail": f"Invalid signature token {str(e)}"}), mimetype="application/json", status=401
            )
            return res(environ, start_response)

        return self.app(environ, start_response)
