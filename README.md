# Report Portal Agent for nose2

![Build Status](https://github.com/diegorubin/nose2-reportportal-agent/workflows/Report%20Portal%20Agent%20For%20Nose2%20CI/badge.svg)
![Agent Publish](https://github.com/diegorubin/nose2-reportportal-agent/workflows/Agent%20Publish/badge.svg)
[![PyPI version](https://badge.fury.io/py/nose2-reportportal-agent.svg)](https://badge.fury.io/py/nose2-reportportal-agent)
[![SourceLevel](https://app.sourcelevel.io/github/diegorubin/-/nose2-reportportal-agent.svg)](https://app.sourcelevel.io/github/diegorubin/-/nose2-reportportal-agent)

## Install

Use pip:

```
pip install nose2-reportportal-agent
```

## Usage

Enable plugin in `nose2.cfg` and configure Report Portal parameters.

```cfg
[unittest]
plugins = nose2_rp_agent

[reportportal]
token = <token>
endpoint = http://endpoint:8080
project = project_name
launch_name = UnitTests
launch_attributes = 'Unit'
launch_description = 'Unit Tests'
```

Run nose2 with parameter `--rp`.
