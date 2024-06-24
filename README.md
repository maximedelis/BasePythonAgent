# BasePythonAgent

A simple Python agent for Mythic using the [http](https://github.com/MythicC2Profiles/http) C2 Profile. Based on Medusa.

## Setup and run locally

- Update the `rabbitmq_config.json` file with the correct RabbitMQ server information.
- Update the `generate_payload.py` file with the correct Mythic login password & host.

- `python3 main.py` to start the agent.
- `python3 generate_payload.py` to generate a payload automatically.

## Install

```bash
sudo ./mythic-cli install github https://github.com/maximedelis/BasePythonAgent.git
```

## Agent commands

- `shell <command>`: Execute a shell command.
- `cd <directory>`: Change the current working directory.
- `upload`: Upload a file to the target.
- `ls <directory>`: List the content of a directory. Default is the current working directory.