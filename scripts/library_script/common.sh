#!/bin/bash
#
# Purpose: This script contains the common functions.
#

_azure_create_iot_device() {
    logger "INFO: Creating Azure IoT Edge device..."
    _AZURE_IOTHUB_NAME=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.iotHubName.value -o tsv)
    _CHECK_IF_DEVICE_EXIST=$(az iot hub device-identity list --ee --hub-name "$_AZURE_IOTHUB_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query "[?deviceId=='$PARAM_IOT_DEVICE_ID'].deviceId")
    if [ "$_CHECK_IF_DEVICE_EXIST" != "[]" ]; then
        logger "INFO: Azure IoT Edge device already exists"
    else
        az iot hub device-identity create --device-id "$PARAM_IOT_DEVICE_ID" --ee --hub-name "$_AZURE_IOTHUB_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME"
        logger "INFO: Azure IoT Edge device created"
    fi
    _AZURE_IOT_HUB_HOSTNAME=$(az iot hub device-identity show --device-id "$PARAM_IOT_DEVICE_ID" --hub-name "$_AZURE_IOTHUB_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query hub -o tsv)
    _AZURE_IOT_DEVICE_KEY=$(az iot hub device-identity show --device-id "$PARAM_IOT_DEVICE_ID" --hub-name "$_AZURE_IOTHUB_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query authentication.symmetricKey.primaryKey -o tsv)
    # shellcheck disable=SC2034
    AZURE_IOTHUB_NAME="$_AZURE_IOTHUB_NAME"
    # shellcheck disable=SC2034
    AZURE_IOT_DEVICE_CONNECTION_STRING="HostName=$_AZURE_IOT_HUB_HOSTNAME;DeviceId=$PARAM_IOT_DEVICE_ID;SharedAccessKey=$_AZURE_IOT_DEVICE_KEY"
    # Update config file with Azure IoT Edge device connection string
    sed -i "s|DEVICE_CONNECTION_STRING=.*|DEVICE_CONNECTION_STRING=\"$AZURE_IOT_DEVICE_CONNECTION_STRING\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    if [ "$PARAM_IOT_DEVICE_DEPLOYMENT_MODE" == "edge" ]; then
        if [ "$PARAM_OS_TYPE" == "linux" ]; then
            # Update config file with Azure IoT Edge runtime version for Linux
            sed -i "s|IOT_EDGE_RUNTIME_VERSION=.*|IOT_EDGE_RUNTIME_VERSION=\"$CONFIG_IOT_EDGE_LINUX_RUNTIME_VERSION\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
            logger "INFO: Using Azure IoT Edge Runtime version for linux: ${CONFIG_IOT_EDGE_LINUX_RUNTIME_VERSION}"
        elif [ "$PARAM_OS_TYPE" == "windows" ]; then
            # Update config file with Azure IoT Edge runtime version for Windows
            sed -i "s|IOT_EDGE_RUNTIME_VERSION=.*|IOT_EDGE_RUNTIME_VERSION=\"$CONFIG_IOT_EDGE_WINDOWS_RUNTIME_VERSION\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
            logger "INFO: Using Azure IoT Edge Runtime version for windows : ${CONFIG_IOT_EDGE_WINDOWS_RUNTIME_VERSION}"
        else
            logger "ERROR: OS type ${PARAM_OS_TYPE} not supported, suported OS types are: linux, windows"
            exit 2
        fi
    else
        logger "INFO: Using deafult Azure IoT Edge Runtime version: ${CONFIG_IOT_EDGE_LINUX_RUNTIME_VERSION}"
    fi
}