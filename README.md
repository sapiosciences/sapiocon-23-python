# sapiocon-23-python

[![License](https://img.shields.io/pypi/l/sapiopylib.svg)](https://github.com/sapiosciences/sapio-py-tutorials/blob/master/LICENSE)

## What is it

This project contains the Sapio Python Webhook examples that were shown
at [SAPIOCON 2023](https://www.sapiosciences.com/sapiocon)

### What is included

`SAPIOCON23.ssg` is a synergy that contains a SapioCon23 data type that is designed to be used with the action button
and selection list examples here

`server.py` is the entry point for the python server that will host the webhook. It will configure the server and then
start it

`webhook/action_button.py` is an example of a webhook that will be called when a user clicks on an action button in the
UI. This webhook shows an example of how showing a client callback works

`webhook/custom_report.py` is a simple webhook demonstrating how you can directive the user to a Custom Report search result.

`webhook/hello_world.py` is a bare-bones webhook that you can use to verify that your Sapio System is successfully
communicating with your webhook

`webhook/list_homeworld.py` is a selection list webhook that will return a list of planets to be used by a selection
list in Sapio

`webhook/list_technicians.py` is a selection list webhook that will return a list of technicians to be used by a
selection list in Sapio

`webhook/load_instrument_data.py` is a ELN webhook that will mimic loading instrument data and inserting into your
active entry

`webhook/record_model.py` is a webhook that shows how to use the Record Model to retrieve/updated/create Data Records

## Requirements

This project depends on [sapiopylib](https://pypi.org/project/sapiopylib/)

For the `ROOT` `/` path to load it depends on the [markdown](https://pypi.org/project/Markdown/) package being installed
to generate the HTML

For SAPIOCON 23 we ran it on render.com for ease of use, but you can run it locally or anywhere you can run python and
host a webserver as long as your Sapio System can reach it.

## Building

Included with this project is a requirements.txt file that allows for you to quickly install the dependencies
through `pip`
> `pip install -r requirements.txt`

## Running

> `python -u server.py`

The `-u` unbuffered parameter is used so that the stdout/stderr console output isn't buffered, so it doesn't need to be
flushed before being shown.

For development of your own custom webhooks we recommend starting with at least 1vCPU and 2gb RAM. Since machine requirements are highly dependent on what your custom code is doing it's recommended to monitor system metrics and scale the server. You can use any OS that can run Python 3, but for server hosting we use Ubuntu 22.04 and if using docker we use the `python:3-slim` docker python image from the public [Docker Repo](https://hub.docker.com/_/python).

## Further Reading

In addition to this project we have interactive python tutorials that you can use to learn more about the Sapio REST API
and webhooks on GitHub at [Sapio Python Tutorials](https://github.com/sapiosciences/sapio-py-tutorials/)

## Licenses

sapiocon-23-python are licensed under MPL 2.0.

This license does not provide any rights to use any other copyrighted artifacts from Sapio Sciences. (And they are
typically written in another programming language with no linkages to this library.)

## Getting Help

If you have support contract with Sapio Sciences, please use our technical support channels. support@sapiosciences.com

If you have any questions about how to use sapiopylib, please visit our tutorial page.

If you would like to report an issue on sapiocon-23-python please feel free to create a issue ticket at the tutorial
github.

## About Us

Sapio is at the forefront of the Digital Lab with its science-aware platform for managing all your life science data
with its integrated Electronic Lab Notebook, LIMS Software and Scientific Data Management System.

Visit us at https://www.sapiosciences.com/
