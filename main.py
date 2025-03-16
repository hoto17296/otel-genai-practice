from asyncio import run, sleep

from openai import AsyncOpenAI, OpenAI

# NOTE: OpenTelemetry Python Logs and Events APIs are in beta
from opentelemetry import _events, _logs, trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
from opentelemetry.sdk._events import EventLoggerProvider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# configure tracing
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

# configure logging and events
_logs.set_logger_provider(LoggerProvider())
_logs.get_logger_provider().add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
_events.set_event_logger_provider(EventLoggerProvider())

# instrument OpenAI
OpenAIInstrumentor().instrument()


def main_sync():
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Write a short poem on OpenTelemetry.",
            },
        ],
    )
    print(response.choices[0].message.content)


# TODO: This code doesn't work for some reason, make it work.
async def main_async():
    client = AsyncOpenAI()
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Write a short poem on OpenTelemetry.",
            },
        ],
        stream=True,
        stream_options={"include_usage": True},
    )
    async for chunk in stream:
        choice = chunk.choices[0]
        if choice.delta.content is None:
            print()
            break
        print(choice.delta.content, end="")
    await sleep(1)


if __name__ == "__main__":
    # main_sync()
    run(main_async())
