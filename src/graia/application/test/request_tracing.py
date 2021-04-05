import functools
from typing import Optional
from aiohttp import TraceConfig
from aiohttp.client import ClientSession
from aiohttp.tracing import TraceRequestEndParams, TraceRequestStartParams
from ..logger import AbstractLogger
import random
import string


class HttpRequestTracing:
    logger: AbstractLogger

    def __init__(self, logger: AbstractLogger) -> None:
        self.logger = logger

    async def on_request_start(
        self, session: ClientSession, trace_config_ctx, params: TraceRequestStartParams
    ):
        req_id = "".join(random.choices(string.ascii_letters, k=12))
        trace_config_ctx.req_id = req_id
        if params.method == "GET":
            self.logger.debug(f"Request[{req_id}:GET]: {params.url}")
        elif params.method == "POST":
            self.logger.debug(
                f"Request[{req_id}:POST]: {params.url} using [{trace_config_ctx.trace_request_ctx[1]['json'] if trace_config_ctx.trace_request_ctx else None}]"
            )

    async def on_request_end(
        self, session: ClientSession, trace_config_ctx, params: TraceRequestEndParams
    ):
        if params.method == "GET":
            self.logger.debug(f"Response[{trace_config_ctx.req_id}:GET]: {params.url}")
        elif params.method == "POST":
            self.logger.debug(
                f"Response[{trace_config_ctx.req_id}:POST]: {params.url} using [{trace_config_ctx.trace_request_ctx[1]['json'] if trace_config_ctx.trace_request_ctx else None}], responsed [{await params.response.text()}]"
            )

    def build_session(
        self, apply_for: Optional[ClientSession] = None, *args, **kwargs
    ) -> ClientSession:
        trace_config = TraceConfig()
        trace_config.on_request_start.append(self.on_request_start)
        trace_config.on_request_end.append(self.on_request_end)
        session = apply_for or ClientSession(
            trace_configs=[trace_config], *args, **kwargs
        )
        if apply_for is not None:
            session.trace_configs.append(trace_config)
            trace_config.freeze()

        def hook_method(method):
            def hooked_wrapper(*args, **kwargs):
                return method(*args, **{**kwargs, "trace_request_ctx": (args, kwargs)})

            return hooked_wrapper

        session.get = hook_method(session.get)
        session.post = hook_method(session.post)
        return session
