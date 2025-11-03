from starlette.responses import StreamingResponse

async def sse_response(generator):
    async def event_gen():
        async for chunk in generator:
            yield f"data: {chunk}\n\n"
    return StreamingResponse(event_gen(), media_type="text/event-stream")
