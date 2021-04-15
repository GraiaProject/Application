Module graia.application.test.request_tracing
=============================================

Classes
-------

`HttpRequestTracing(logger: graia.application.logger.AbstractLogger)`
:   

    ### Class variables

    `logger: graia.application.logger.AbstractLogger`
    :

    ### Methods

    `build_session(self, apply_for: Union[aiohttp.client.ClientSession, NoneType] = None, *args, **kwargs) ‑> aiohttp.client.ClientSession`
    :

    `on_request_end(self, session: aiohttp.client.ClientSession, trace_config_ctx, params: aiohttp.tracing.TraceRequestEndParams)`
    :

    `on_request_start(self, session: aiohttp.client.ClientSession, trace_config_ctx, params: aiohttp.tracing.TraceRequestStartParams)`
    :