# Report Portal Agent for nose2

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

Run nose2 with parameter `-rp`.
