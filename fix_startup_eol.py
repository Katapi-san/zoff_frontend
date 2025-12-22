
content = b'#!/bin/bash\npython -m uvicorn application:app --host 0.0.0.0 --port 8000\n'

with open('backend/startup.sh', 'wb') as f:
    f.write(content)

print("Fixed startup.sh EOL")
