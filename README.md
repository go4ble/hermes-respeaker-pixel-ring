# hermes-respeaker-pixel-ring

```
docker build -t go4ble/hermes-respeaker-pixel-ring:latest .

docker run --rm -it \
  --device /dev/spidev0.0 \
  --device /dev/spidev0.1 \
  --device /dev/gpiomem \
  -e HOST=localhost \
  -e PORT=1883 \
  -e SITE_ID=default \
  go4ble/hermes-respeaker-pixel-ring:latest
```
