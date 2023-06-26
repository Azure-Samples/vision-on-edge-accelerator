# Label Reader

This is an Azure IoT Edge solution that uses Azure Cognitive Services to read labels from images. The solution is composed of the following modules:

- [label_extraction](./modules/label_extraction/): This module is responsible for receiving video frames from RTSP stream, running edge inferencing for text detection, sending eligible frames to Azure Form Recognizer for text extraction, processing the results to extract fields, posting requests to Azure TTS service with the extracted fields and receiving audio bytes for the same.
- [web_app_api](./modules/web_app_api/): This module is responsible for communication between the label extraction and UI components using websocket connection.
- [web_app_ui_mvp](./modules/web_app_ui_mvp/): This module is responsible for displaying the live video stream and extracted order information on the screen and voicing out the order information.

## Build

The solution can be built using the following command:

```bash
cd /workspace/scripts
./deployment.sh -L # List the existing Azure Infrastructure deployments
./deployment.sh -b -n <azure-infra-deployment-name-from-above-command> # Provide the required cpu architecture flag as per deployment documentation
```

## Deploy

The solution can be deployed in simulation mode or edge mode. In simulation mode, the modules are deployed to a local IoT Edge runtime. In edge mode, the modules are deployed to an IoT Edge device.

```bash
cd /workspace/scripts
./deployment.sh -L # List the existing Azure Infrastructure deployments
./deployment.sh -d -n <azure-infra-deployment-name-from-above-command> # Provide additional flags as per deployment documentation
```

## Unit Test

The solution can be unit tested using the following commands:

```bash
cd /workspace
make label_extraction_tests
make web_app_api_tests
```
