# Deployment

This document describes how to deploy the Azure infrastructure, create application configuration, and deploy the application. The deployment process is described in the following steps:

1. Deploy the following Azure resources:
   1. A resource group
   1. Cognitive services account
   1. Container registry
   1. IoT Hub
   1. Storage account
   1. Log analytics workspace
   1. Application insights
1. Configure following Azure Resources
   1. Create an IoT Edge device in IoT Hub
   1. Copy the pre-trained Form Recognizer model to the newly created Cognitive Services account
1. Create application configuration (IoT Edge Solution .env file)
1. Build the application (IoT Edge Solution)
   1. Supported architectures: amd64 and arm64v8
1. Deploy the application (IoT Edge Solution)
   1. Deploy in Simulation mode (without IoT Edge device)
      1. Supported devices OS: Windows, Linux, macOS (including M1)
   1. Deploy in Edge mode (with IoT Edge device)
      1. Supported devices OS: Linux and Windows

## Steps

The above mentioned deployment process can be performed using the script [deployment.sh](../scripts/deployment.sh).

### Prerequisites

To run the script, the following installations are required:

1. Azure CLI
1. Azure CLI Bicep extension
1. Azure CLI IoT extension
1. Docker
1. `iotedgedev` CLI
1. `iotedgehubdev` CLI

**NOTE:** The above mentioned packages are already installed in DevContainer. If you are using DevContainer, you can skip these installations.

### Execution Guide

1. Open a terminal in the root of the repository.
1. Login to Azure CLI using `az login` command
1. Set the respective subscription using `az account set --name <subscription-name>` command
1. Go to [scripts](../scripts/) directory using `cd scripts` command
1. Run the script using `./deployment.sh` command, by following the user guide below

   **Usage:**

   ```bash
   ./deployment.sh -a -i -c -b -d -L -f <source-azure-form-recog-endpoint> \
        -k <source-azure-form-recog-key> -m <deployment-mode> \
        -r <resource-group> -l <location-name> -e <azure-iot-edge-device-id> \
        -o <OS Type> -p <azure-iot-edge-device-cpu-arch> -n <azure-infra-deployment-name>
   ```

   **Options:**

   - `-a`: bool: Enable full (E2E) one click deployment (default: true, non mandatory)
   - `-i`: bool: Enable only infrastructure deployment (default: false, non mandatory)
   - `-c`: bool: Enable only application configuration update (default: false, non mandatory)
   - `-b`: bool: Enable only application build (default: false, non mandatory)
   - `-d`: bool: Enable only application deployment (default: false, non mandatory)
   - `-L`: bool: List all Azure deployments for a resource group (default: false, non mandatory)"
   - `-f`: string: Source Azure Form Recognizer endpoint (**mandatory** with `-a` (default) and `-i` options)
   - `-k`: string: Source Azure Form Recognizer key (**mandatory** with `-a` (default) and `-i` options)
   - `-m`: string: Application deployment mode (default: simulated, non mandatory) possible values: simulated, edge
   - `-r`: string: Resource group name (default: labelreader-demo-environment, non mandatory)
   - `-l`: string: Location (default: eastus2, non mandatory)
   - `-e`: string: Azure IoT Edge device name (default: labelreader-device, non mandatory)
   - `-o`: string: OS Type (default: linux, nonmandatory) possible values: linux, windows
   - `-p`: string: Azure IoT Edge device CPU architecture (default: amd64, non mandatory) possible values: amd64, arm64v8
   - `-n`: string: Azure infrastructure deployment name (non mandatory, **mandatory** if `-c`, `-b` or `-d`)
   - `-h`: bool: Show this help (non mandatory)

### Execution order

The script can be executed E2E or in parts. While executing in parts make sure to execute the script in the following order:

1. Infrastructure deployment using `-i` option, once infrastructure is deployed, the script will print the name of the deployment (`Azure infrastructure deployment name`). This name will be used in the next steps using `-n` option.
1. Application configuration update using `-c` option, make sure to pass the name of the deployment using `-n` option.
1. Application build using `-b` option, make sure to pass the name of the deployment using `-n` option.
1. Application deployment using `-d` option, make sure to pass the name of the deployment using `-n` option.

**NOTE:** Once the infrastructure is deployed, same can be used for subsequent steps. If you missed to note the name of deployment during infrastructure deployment, you can list all the deployments using `-L` option any time later and get the name of the deployment.

### Examples

1. Using all default e2e run in simulation mode: `./deployment.sh -f <source-azure-form-recog-endpoint> -k <source-azure-form-recog-key>`
1. Mention resource group, location etc.: `./deployment.sh -f <source-azure-form-recog-endpoint> -k <source-azure-form-recog-key> -a -r my-demo-rg -l eastus2 -e my-demo-edge-device`
1. Only infrastructure deployment: `./deployment.sh -i -f <source-azure-form-recog-endpoint> -k <source-azure-form-recog-key>`
1. Only config update: `./deployment.sh -c -n LabelReaderDeployment24-Aug-2022-13-36-39`
1. Only application build: `./deployment.sh -b -n LabelReaderDeployment24-Aug-2022-13-36-39`
1. Only application deploy into solution mode: `./deployment.sh -d -n LabelReaderDeployment24-Aug-2022-13-36-39`
1. Only application deploy into edge mode: `./deployment.sh -d -n LabelReaderDeployment24-Aug-2022-13-36-39 -m edge -o linux -p arm64v8 -e my-demo-edge-device`
1. List all deployments: `./deployment.sh -L -r my-demo-rg`

## Accessing the application

Once the application is deployed, you can access the application using the following URL:

1. In simulation mode: `http://localhost:8080`
   1. If not able to access the above URL, please check if the port `8080`, `7001` and `8554` are being forwarded in VsCode `Ports` tab and these ports are not being used by any other applications in host machine.
1. In Edge mode: `http://<azure-iot-edge-device-ip>:8080`
   1. If not able to access the above URL, please check if the port `8080`, `7001` and `8554` are not blocked in the Azure IoT Edge device and these ports are not being used by any other applications in the Azure IoT Edge device.
   1. If the IoT Edge Device OS is Windows, the `EFLOW` IP address can be found using the PowerShell command [Get-EflowVmAddr](https://docs.microsoft.com/en-us/azure/iot-edge/reference-iot-edge-for-linux-on-windows-functions?view=iotedge-1.4) and the application can be accessed using the URL `http://<EFLOW-IP>:8080`

## Troubleshooting

1. While creating Azure resources, if you get permission error, please make sure to set the correct subscription using `az account set --name <subscription-name>` command.
1. Do not run the script from the root of the repository. Run the script from the [scripts](../scripts/) directory.
