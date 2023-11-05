#!/bin/bash

sed -i "s/your_google_oauth2_mock_token/$(python3 -c 'import string; import random; print("".join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64)))')/g" ./api/.env
