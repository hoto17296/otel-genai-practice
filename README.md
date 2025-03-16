# OpenTelemetry for Generative AI Practice
See also: [OpenTelemetry for Generative AI | OpenTelemetry](https://opentelemetry.io/blog/2024/otel-generative-ai/)

## Setup
Create `.devcontainer/compose.env.yml` file.

``` yaml:.devcontainer/compose.env.yml
services:
  workspace:
    environment:
      OPENAI_API_KEY: ...
```

## Run
1. Open this repository in DevContainer (VSCode is recommended).
2. Access the Aspire Dashboard.
  - http://localhost:18888/
3. Running main.py will send telemetry, which you can view in the Aspire Dashboard.
  - `python main.py`