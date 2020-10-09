# APIStats

Simple django module with a middleware to track calls to django backend. 

## Description

APIStats is a middleware that stores basic information on the requests and responses to Django backend.

## Installation

* `pip install apistats`
* Add `apistats` to `INSTALLED_APPS`
* Run `./manage.py migrate`
* Add `'apistats.middlewares.LoggingMiddleware'` to `MIDDLEWARE` in `settings.py`

## Usage 

APIstats adds an admin interface to :
* view / sort / filter records
* view detail of a record and statistics

## Model

APIStats stores the following fields:
* user: user account making the request
* record_time: time of the record
* method: method of the request
* domain: first part of the request path
* path: complete path
* query: query parameters for GET requests
* ip: IP of the caller
* delay: nb of milliseconds between request and response
* status: response HTTP status
 
