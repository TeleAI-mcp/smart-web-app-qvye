"""
FastAPI default application class.
"""
from typing import Any

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Match

from fastapi.routing import APIRouter, APIRoute


class FastAPI(Starlette):
    """
    The main FastAPI application class.

    This is the class that you would normally use to create a FastAPI application.

    Read more in the [FastAPI docs for Applications](https://fastapi.tiangolo.com/advanced/).
    """

    def __init__(
        self,
        *,
        debug: bool = False,
        routes: list[BaseRoute] | None = None,
        middleware: list[Middleware] | None = None,
        exception_handlers: dict[Any, Any] | None = None,
        on_startup: list[callable] | None = None,  # type: ignore
        on_shutdown: list[callable] | None = None,  # type: ignore
        lifespan: Any = None,
        **extra: Any,
    ) -> None:
        """
        Create a FastAPI application instance.

        ## Parameters

        * **debug**: Boolean indicating if debug tracebacks should be returned on server errors.
        * **routes**: A list of routes to serve incoming HTTP and WebSocket requests.
        * **middleware**: A list of middleware to run for every request.
        * **exception_handlers**: A dictionary of exception types (or custom exception keys)
            to handler functions.
        * **on_startup**: A list of startup event handler functions.
        * **on_shutdown**: A list of shutdown event handler functions.
        * **lifespan**: A lifespan context function, handling startup and shutdown in one.
        * **extra**: Additional keyword arguments to pass to Starlette.
        """
        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            **extra,
        )

    def openapi(self) -> dict[str, Any]:
        """
        Generate the OpenAPI schema for the application.

        Returns:
            The OpenAPI schema as a dictionary.
        """
        if not self.routes:
            return {"openapi": "3.1.0", "info": {"title": "FastAPI", "version": "0.1.0"}, "paths": {}}
        # This would normally generate the full OpenAPI schema
        return {"openapi": "3.1.0", "info": {"title": "FastAPI", "version": "0.1.0"}, "paths": {}}

    def add_api_route(
        self,
        path: str,
        endpoint: Any,
        *,
        methods: list[str] | None = None,
        response_model: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Add an API route to the application.

        ## Parameters

        * **path**: The URL path for the route.
        * **endpoint**: The endpoint function that will handle requests to this path.
        * **methods**: A list of HTTP methods that this route accepts.
        * **response_model**: The model to use for the response validation.
        * **kwargs**: Additional keyword arguments to pass to the route.
        """
        route = APIRoute(
            path=path,
            endpoint=endpoint,
            methods=methods or ["GET"],
            response_model=response_model,
            **kwargs,
        )
        self.routes.append(route)

    def include_router(self, router: APIRouter, *, prefix: str = "", **kwargs: Any) -> None:
        """
        Include an APIRouter in the application.

        ## Parameters

        * **router**: The APIRouter instance to include.
        * **prefix**: An optional path prefix for all routes in the router.
        * **kwargs**: Additional keyword arguments.
        """
        for route in router.routes:
            if isinstance(route, APIRoute):
                route.path = prefix + route.path
            self.routes.append(route)
