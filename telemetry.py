import logging, time
from contextlib import contextmanager
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
provider=TracerProvider(); provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter())); trace.set_tracer_provider(provider)
tracer=trace.get_tracer('tagi')
@contextmanager
def span(name, **attributes):
    with tracer.start_as_current_span(name) as current:
        for key,value in attributes.items(): current.set_attribute(key,str(value))
        started=time.perf_counter()
        try: yield current
        finally: current.set_attribute('duration_ms',round((time.perf_counter()-started)*1000,2))
