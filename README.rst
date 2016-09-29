What is this
------------

A simplified reliable distributed (and ideally scalable) version of a
thing somewhat akin to `heat`_ and `warm`_, but really not either.

The general idea
----------------

1. Receive user request to build X via REST (applying typical
   OpenStack authn/z and such to make this happen); if not authorized blow
   up and return typical error.
2. Parse build X request into some useful internal structure Y (at the same
   time validate it); if request is invalid, blow up and return typical
   error.
3. Drop internal structure Y into a per-build zookeeper Z directory and return
   back a identifier (an encoded version of the directory Z name per-say)
   that can be sent back in to see the current status of whatever was
   requested to build.
4. Worker (one of many) watching zookeeper takes ownership of build
   directory Z and progresses build through needed steps (updating zookeeper
   with status so that user can request status of build X and get back
   useful information); if worker dies, another worker takes over and
   continues, if build is not possible due
   to runtime issue, fail build and leave note that can be fetched by future
   user request with details on why.
5. Build X finishes, profit! Now either delete build directory Z in zookeeper
   or leave it and prune it at a later date (via a mechanism akin to
   cache eviction or garage collection).

.. _heat: https://wiki.openstack.org/wiki/Heat
.. _warm: https://wiki.openstack.org/wiki/Warm
