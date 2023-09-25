#!/bin/bash

cp ./api/.env.example ./api/.env

sed -i "s/your_secret_key/$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')/g" ./api/.env