========================
coveo-push-api-client.py
========================


Python Push API Client


Installation
============

``pip install coveo-push-api-client.py``

Usage
=====

See more examples in the ``./samples`` folder.

.. code-block:: python

    from push_api_clientpy import Source, DocumentBuilder

    source = Source("my_api_key", "my_org_id")

    myDocument = DocumentBuilder("https://my.document.uri", "My document title")\
       .withData("these words will be searchable")

    response = source.addOrUpdateDocument("my_source_id", myDocument)

    print(f"Document added: {response.json()}")


Exponential backoff retry configuration
=======================================

By default, the SDK leverages an exponential backoff retry mechanism. Exponential backoff allows for the SDK to make multiple attempts to resolve throttled requests, increasing the amount of time to wait for each subsequent attempt. Outgoing requests will retry when a `429` status code is returned from the platform.

The exponential backoff parameters are as follows:

* ``retry_after`` - The amount of time, in seconds, to wait between throttled request attempts.

  Optional, will default to 5.

* ``max_retries`` - The maximum number of times to retry throttled requests.

  Optional, will default to 10.

You may configure the exponential backoff that will be applied to all outgoing requests. To do so, specify a `BackoffOptions` object when creating either a `Source` or `PlatformClient` object:

.. code-block:: python

    source = Source("my_api_key", "my_org_id", BackoffOptions(3, 10))

By default, requests will retry a maximum of 10 times, waiting 10 seconds after the second attempt, with a time multiple of 2 (which will equate to a maximum execution time of roughly 1.5 hours. See `urllib3 Retry documentation <https://urllib3.readthedocs.io/en/2.0.4/reference/urllib3.util.html#urllib3.util.Retry>`_).

Dev
===

* Requires Python 3.9
* Requires pipenv: ``pip install pipenv``
* Install dependencies: ``pipenv install --dev``
* Build: ``pipenv run tox -e build``
* Tests: ``pipenv run tox``
* Full list of commands: ``pipenv run tox -av``

Release
=======

* Tag the commit to release with semver format ``v{Major}.{Minor}.{Patch}`` eg: ``v1.2.5``.
* Checkout the newly created tag, e.g.: ``git checkout v1.2.5``
* Run ``pipenv run tox -e clean``
* Run ``pipenv run tox -e build``
* Run ``pipenv run tox -e publish``

Note
====

This project has been set up using PyScaffold 4.0.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
