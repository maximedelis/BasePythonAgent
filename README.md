# BasePythonAgent

A basic Python agent for Mythic. Based on Medusa.

## Setup and run locally

- Update the `rabbitmq_config.json` file with the correct RabbitMQ server information.
- Update the `generate_payload.py` file with the correct Mythic login password & host.

- `python3 main.py` to start the agent.
- `python3 generate_payload.py` to generate a payload automatically.

## Install

- `sudo ./mythic-cli install github https://github.com/maximedelis/BasePythonAgent.git`

## Agent commands

- `shell <command>`: Execute a shell command.
- `cd <directory>`: Change the current working directory.