# Edge Device Configuration

This document describes how to configure an edge device with Azure IoT Edge runtime for running the Label Reader solution.

## 1. For Linux (AMD and ARM64v8)

1. Follow the steps mentioned in [Create and provision an IoT Edge device on Linux using symmetric keys](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-provision-single-device-linux-symmetric?view=iotedge-1.4&tabs=azure-portal%2Cubuntu) document to create and provision an IoT Edge device on Linux using symmetric keys.

   > Additional notes, while following the steps mentioned in the document:

   - The same Azure IoT Hub must be used that is created as part of the Azure Infrastructure deployment, via `deployment.sh` script.
   - All of the commands need to be executed on the edge device.
   - If the edge device is having already docker installed, then the container engine installation steps can be skipped.

1. Please note the device id and use it in `deployment.sh` script by passing it via `-e` flag (`edge-device-id`)

## 2. For Windows (AMD and ARM64v8)

1. Follow the steps mentioned in [Create and provision an IoT Edge for Linux on Windows device using symmetric keys](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-provision-single-device-linux-on-windows-symmetric?view=iotedge-1.4&tabs=azure-portal%2Cpowershell) document to create and provision an IoT Edge device on Windows using symmetric keys.

   > Additional notes, while following the steps mentioned in the document:

   - The same Azure IoT Hub must be used that is created as part of the Azure Infrastructure deployment, via `deployment.sh` script.
   - While executing `Deploy-Eflow` command, please note the default 1 GB of RAM, 1 vCPU core is not sufficient for running the solution. Please increase the RAM to 4 GB and vCPU cores to 2. The following command can be executed to increase the RAM and vCPU cores:

     ```powershell
     Deploy-Eflow -cpuCount 2 -memoryInMB 4096
     ```

     > Note: if by mistake the Deploy-Eflow is executed without increasing the CPU and Memory, the same command can not be executed again. In that case, please [Uninstall IoT Edge for Linux on Windows](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-provision-single-device-linux-on-windows-symmetric?view=iotedge-1.4&tabs=azure-portal%2Cpowershell#uninstall-iot-edge-for-linux-on-windows) and follow the steps from beginning.

   - All of the commands need to be executed on the edge device.

1. Please note the device id and use it in `deployment.sh` script by passing it via `-e` flag (`edge-device-id`)
