#!/bin/bash


./manage.py shell -c "from api.populate import populate;populate()"
