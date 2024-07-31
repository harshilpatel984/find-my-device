# Find My Device Tool

This tool is finding serial number details from business central with part number and its warranty details.

Note: This is developed by @harshilpatel

![alt text](image.png)

### Docker Deployment

```docker build . -t find-my-device```

```docker run --name find-my-device --restart unless-stopped -d -p 5000:5000 find-my-device```