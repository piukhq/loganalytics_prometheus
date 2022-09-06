from datetime import timedelta
from time import sleep

from azure.core.exceptions import ServiceResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from prometheus_client import Gauge, start_http_server

from loganalytics_prometheus.settings import log, settings

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)


g = Gauge(
    name="loganalytics",
    documentation="count of logs in a given log source",
    labelnames=["source"],
)


def get_count() -> Gauge:
    log.warning("Beginning Log Analytics Metrics Collection")
    for _ in range(10):
        try:
            response = client.query_workspace(
                workspace_id=settings.workspace_id,
                query="search * | summarize count() by $table",
                timespan=timedelta(minutes=settings.query_interval_minutes),
            )
        except ServiceResponseError:
            log.warning("Failed to collect metrics, retrying...")
            continue
        if response.status == LogsQueryStatus.PARTIAL:
            log.warning("Failed to collect metrics, retrying...")
            continue
        elif response.status == LogsQueryStatus.SUCCESS:
            g.clear()
            result = response.tables[0].rows
            for i in result:
                key, value = i[0], i[1]
                log.warning("Collected Metric", extra={"table_name": key, "value": value})
                g.labels(key).set(value)
        log.warning("Finished Log Analytics Metrics Collection")
        break


def main():
    log.warning(
        "Starting Log Analytics Prometheus Server", extra={"query_interval_minutes": settings.query_interval_minutes}
    )
    start_http_server(9100)
    while True:
        get_count()
        sleep(settings.query_interval_minutes * 60)
