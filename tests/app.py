from aiohttp import web


def hello(_: web.Request):
    return web.Response(text="Hello, world!")


app = web.Application()
app.router.add_get("/hello", hello)
