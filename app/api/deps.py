from app.core.context import Context

async def get_context() -> Context:
    async with Context() as ctx:
        yield ctx
