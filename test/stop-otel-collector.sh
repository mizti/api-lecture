#!/bin/bash
# Find and kill the OpenTelemetry Collector process
ps aux | grep "otelcol --config test/otel-collector-config.yaml" | grep -v grep | awk '{print $2}' | xargs -r kill
