========================
coveo-push-api-client.py
========================


Python Push API Client


Installation
============

``pip install coveo-push-api-client.py``

Usage
=====

.. code-block:: python
    from push_api_clientpy import Source, DocumentBuilder

    source = Source("my_api_key", "my_org_id")

    myDocument = DocumentBuilder("https://my.document.uri", "My document title")\
        .withData("these words will be searchable")

    response = source.addOrUpdateDocument("my_source_id", myDocument)

    print(f"Document added: {response.json()}")

See more examples in the `./samples` folder.

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
