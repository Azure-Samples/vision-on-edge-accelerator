# Vision Based Order Pickup Experience

A vision-based order pickup solution which leverages ML on the edge capabilities in conjunction with Azure Applied AI Services to empower the retail store operations for improving the order pickup experience.

## Solution overview

Solution [high level architecture](./docs/high-level-architecture.md)

## Solution user guide

This solution can be demoed or experimented in two following different modes:

### 1. Simulation mode

#### Prerequisites

The following prerequisites are required to run the solution in simulation mode:

- Any development machine having Windows, MacOS and Linux OS, with minimum 8GB RAM and 4 CPU cores and AMD and ARM64v8 architecture support.
- An integrated Webcam or a external USB camera
- An Azure subscription with rights to create Azure resources
- Configure the development machine:
  - For Windows development machines, please install [WSL](https://docs.microsoft.com/en-us/windows/wsl/install)
  - Install [Docker Desktop](https://docs.docker.com/desktop/#download-and-install)
  - Install [Visual Studio Code](https://code.visualstudio.com/download)
  - Install [Visual Studio Code Remote Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
- Optional: Get some test orders items by printing (on a A4 sheet) the labels from [test_labels](./docs/test_labels.png) and sticking them on a order item (box, cup, etc.)

#### Deployment steps

1. In development machine, open the repository in Visual Studio Code dev container by following this [steps](./docs/dev_container.md)
1. Open a terminal in Visual Studio Code dev container and run the following command to execute the solution in simulated mode:

   ```bash
   cd /workspace/scripts
   ./deployment.sh -f <source-azure-form-recog-endpoint> -k <source-azure-form-recog-key>
   ```

   Example:

   ```bash
   cd /workspace/scripts
   ./deployment.sh -f https://abc.cognitiveservices.azure.com/ -k 1234567890
   ```

   **NOTEs:**

   - The above command will deploy the Azure infrastructure and start the application in simulated mode.
   - To overwrite the default values of the deployment parameters, or to execute in steps please refer to the [deployment document](./docs/deployment.md) for more details.
   - To get the source Azure Form Recognizer endpoint `source-azure-form-recog-endpoint` and key `source-azure-form-recog-key`, please reach out to cse-Aakash `cseAakash@microsoft.com`

#### Accessing the solution

1. By default the solution is deployed with a [test video file](./label-reader/modules/label_extraction/local_data/order_label_test_video.mp4) as a camera input, that runs in a loop to demonstrate the solution.
1. The solution can be accessed in any browser in development machine using the following URL: [http://localhost:8080](http://localhost:8080). For more details refer to the [deployment document](./docs/deployment.md#accessing-the-application)

#### Using integrated webcam or usb camera

Instead of using the default test video file, the solution can be configured to use the integrated webcam or usb camera as a camera input. To do so, follow the steps:

1. If running the solution with test video file, stop the solution by pressing `Ctrl+C` in the terminal where the solution is running.
1. Change the value of `CAMERA_PATH` to `'rtsp://localhost:8554/stream'` in the .env (`./label-reader/.env`) file.
   1. If the .env (`./label-reader/.env`) file does not exists, make sure that you have executed the deployment script `deployment.sh` either e2e (default) or performed application configuration update using `-c` option
1. Make sure that the camera is connected to the development machine.
1. Start the solution by executing the following commands (refer [deployment document](./docs/deployment.md) for additional flags):

   ```bash
   cd /workspace/scripts
   ./deployment.sh -L # List the existing Azure Infrastructure deployments
   ./deployment.sh -d -n <azure-infra-deployment-name-from-above-command> # Provide additional flags as per deployment documentation
   ```

1. Start the camera integration by following [integrating the camera to the solution](./docs/camera_integration_using_ffmpeg.md) document.

   > The camera integration steps must be executed inside the development machine by opening a terminal (Mac, Linux) or command prompt (for windows). Not inside the Visual Studio Code dev container.

1. Now you should be able to see the camera feed while accessing the solution as described in the [accessing the solution](#accessing-the-solution) section.
1. To test the solution place some test order items with label as created in the [prerequisites](#prerequisites) section in front of the camera and see the solution in action.

### 2. Edge mode

#### Prerequisites

The following prerequisites are required to run the solution in edge mode:

- Any development machine having Windows, MacOS and Linux OS, with minimum 8GB RAM and 4 CPU cores and AMD and ARM64v8 architecture support.
- An Edge device with minimum 4GB RAM and 2 CPU cores and AMD and ARM64v8 architecture support.
- An integrated Webcam or a external USB camera attached to the edge device
- An Azure subscription with rights to create Azure resources
- Configure the development machine:
  - For Windows development machines, please install [WSL](https://docs.microsoft.com/en-us/windows/wsl/install)
  - Install [Docker Desktop](https://docs.docker.com/desktop/#download-and-install)
  - Install [Visual Studio Code](https://code.visualstudio.com/download)
  - Install [Visual Studio Code Remote Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
- Optional: Get some test orders items by printing (on a A4 sheet) the labels from [test_labels](./docs/test_labels.png) and sticking them on a order item (box, cup, etc.)

#### Deployment steps

1. In development machine, open the repository in Visual Studio Code dev container by following this [steps](./docs/dev_container.md)
1. Configure the edge device by following the [edge device configuration](./docs/edge_device_configuration.md) document.
1. Open a terminal in Visual Studio Code dev container and run the following command to execute the solution in edge mode:

   ```bash
   cd /workspace/scripts
   ./deployment.sh -f <source-azure-form-recog-endpoint> -k <source-azure-form-recog-key> -m edge -o <os-type> -p <cpu-architecture> -e <edge-device-id>
   ```

   Example:

   ```bash
   cd /workspace/scripts
   ./deployment.sh -f https://abc.cognitiveservices.azure.com/ -k 1234567890 -m edge -o linux -p arm64v8 -e my-demo-edge-device
   ```

   **NOTEs:**

   - The above command will deploy the Azure infrastructure and start the application in edge mode.
   - To overwrite the default values of the deployment parameters, or to execute in steps please refer to the [deployment document](./docs/deployment.md) for more details.
   - To get the source Azure Form Recognizer endpoint `source-azure-form-recog-endpoint` and key `source-azure-form-recog-key`, please reach out to cse-Aakash `cseAakash@microsoft.com`

#### Accessing the solution

1. By default the solution is deployed with a [test video file](./label-reader/modules/label_extraction/local_data/order_label_test_video.mp4) as a camera input, that runs in a loop to demonstrate the solution.
1. The solution can be accessed in any browser in edge/developer machine using the Edge machine URL as provided in [deployment document](./docs/deployment.md#accessing-the-application)

#### Using integrated webcam or usb camera

Instead of using the default test video file, the solution can be configured to use the integrated webcam or usb camera as a camera input. To do so, follow the steps:

1. Change the value of `CAMERA_PATH` to `'rtsp://localhost:8554/stream'` in the .env (`./label-reader/.env`) file.
1. Make sure that the camera is connected to the edge device.
1. Re-deploy the solution by executing the following commands (refer [deployment document](./docs/deployment.md) for additional flags):

   ```bash
   cd /workspace/scripts
   ./deployment.sh -L # List the existing Azure Infrastructure deployments
   ./deployment.sh -d -n <azure-infra-deployment-name-from-above-command> -m edge -o <os-type> -p <cpu-architecture> -e <edge-device-id> # Provide additional flags as per deployment documentation
   ```

1. Start the camera integration by following [integrating the camera to the solution](./docs/camera_integration_using_ffmpeg.md) document.

   > The camera integration steps must be executed inside the edge device by opening a terminal inside the edge device.

1. Now you should be able to see the camera feed while accessing the solution as described in the [accessing the solution](#accessing-the-solution-1) section.
1. To test the solution place some test order items with label as created in the [prerequisites](#prerequisites-1) section in front of the camera and see the solution in action.

### Additional Notes

- This solution is pre-packaged with a custom Azure Form Recognizer model, which is trained with labels similar to what is there in [test video file](./label-reader/modules/label_extraction/local_data/order_label_test_video.mp4). If you want to use this solution with your own label formats, please refer the [Bring your own label (BYOL)](#bring-your-own-label-byol) section.
- This solution may works with a RTSP camera as well, but it is not tested. If you want to use this solution with a RTSP camera, please change the value of `CAMERA_PATH` to `'<RTSP address>'` in the .env (`./label-reader/.env`) file and do let us know how is the experience.

## Solution advance usage

### Experimenting with different configurations

The solution can be experimented with different configurations parameters like TTS voice profile, pitch, etc. For more details refer to the [configuration document](./docs/application_configuration.md)

### Bring your own label (BYOL)

The following steps are required to use this solution with your own label formats:

1. Train a custom Azure Form Recognizer model with your own label formats by following the steps mentioned in [Bring Your Own Label design document](./docs/byol-implementation-details.md)
1. Once the model is trained, update the new model id in the .env (`./label-reader/.env`) file.
   - `AZURE_COGNITIVE_SERVICE_FORMRECOG_MODEL_ID` - The model id of the custom Azure Form Recognizer model.
   - `AZURE_COGNITIVE_SERVICE_FORMRECOG_KEY` - If the custom Azure Form Recognizer model is in a different Azure resource, then update the key of the custom Azure Form Recognizer resource, else keep the same as updated by deployment script.
   - `AZURE_COGNITIVE_SERVICE_FORMRECOG_ENDPOINT` - If the custom Azure Form Recognizer model is in a different Azure resource, then update the endpoint of the custom Azure Form Recognizer resource, else keep the same as updated by deployment script.
1. Re-deploy/Re-start the solution by executing the following command from development machine (refer [deployment document](./docs/deployment.md) for additional flags):

   1. Simulation mode:

      ```bash
      cd /workspace/scripts
      ./deployment.sh -L # List the existing Azure Infrastructure deployments
      ./deployment.sh -d -n <azure-infra-deployment-name-from-above-command> # Provide additional flags as per deployment documentation
      ```

   1. Edge Mode

      ```bash
      cd /workspace/scripts
      ./deployment.sh -L # List the existing Azure Infrastructure deployments
      ./deployment.sh -d -n <azure-infra-deployment-name-from-above-command> -m edge -o <os-type> -p <cpu-architecture> -e <edge-device-id> # Provide additional flags as per deployment documentation
      ```

## References

- [VSCode Dev Container](https://code.visualstudio.com/docs/remote/containers)
- [Azure IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/)
- [Azure Form Recognizer](https://docs.microsoft.com/en-us/azure/cognitive-services/form-recognizer/)
- [Azure TTS](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/text-to-speech)
- [ffmpeg](https://ffmpeg.org/)
