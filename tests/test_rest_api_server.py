"""Test the rest_api_server module functionality."""


from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.rest_api_server import RESTAPIServer


class TestRESTAPIServer(TestMixin):
    """Test the rest_api_server module functionality."""

    def __init__(self) -> None:
        """TestRESTAPIServer Constructor."""
        super().__init__()
        self.logger.info("TestRESTAPIServer initialized.")

    async def test(self):
        """TestRESTAPIServer Test."""
        super().test()
        SERVER_HOST = "127.0.0.1"
        REST_API_PORT = 8083

        app = RESTAPIServer(SERVER_HOST, REST_API_PORT)

        app.get("/test-get", "GET Test Path Registered Successfully.")
        app.post("/test-post", '{"post": "POST Test Path Registered Successfully."}')
        app.put("/test-put", '{"put": "PUT Test Path Registered Successfully."}')
        app.delete("/test-delete", 'DELETE Test Path Registred Successfully.')

        await app.start_http_server()

