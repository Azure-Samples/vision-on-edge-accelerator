#!/bin/bash
#
# Purpose: This script contains the common functions for the application build deployment.
#

## Updating the iot edge solution configuration .env file
application_config_update() {
    logger "INFO: Running config update (it may take few minutes)..."
    if [ -z "$AZURE_DEPLOYMENT_NAME" ]; then
        logger "ERROR: Deployment name is not set. Please set it using -n option."
        exit 2
    fi
    # From bicep output
    _AZURE_IOTHUB_NAME=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.iotHubName.value -o tsv)
    _AZURE_IOTHUB_RESOURCE_ID=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.iotHubResourceId.value -o tsv)
    _AZURE_APP_INSIGHTS_CONNECTION_STRING=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.appInsightsConnectionString.value -o tsv)
    _AZURE_COGNITIVE_SERVICE_ENDPOINT=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.cognitiveServiceAccountEndpoint.value -o tsv)
    _AZURE_LOG_ANALYTICS_WORKSPACE_ID=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.loganalyticsWorkspaceID.value -o tsv)
    # From bicep output, neeeded in azure cli
    _AZURE_BLOB_STORAGE_ACCOUNT_NAME=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.storageAccountName.value -o tsv)
    _AZURE_COGNITIVE_SERVICE_ACCOUNT_NAME=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.cognitiveServiceAccountName.value -o tsv)
    _AZURE_LOG_ANALYTICS_WORKSPACE_NAME=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.loganalyticsWorkspaceName.value -o tsv)
    _AZURE_ACR_NAME=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.acrName.value -o tsv)
    _AZURE_ACR_LOGIN_SERVER=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.acrLoginServer.value -o tsv)
    # Via azure cli
    _AZURE_BLOB_STORAGE_CONN_STRING=$(az storage account show-connection-string -n "$_AZURE_BLOB_STORAGE_ACCOUNT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query connectionString -o tsv)
    _AZURE_COGNITIVE_SERVICE_KEY=$(az cognitiveservices account keys list -n "$_AZURE_COGNITIVE_SERVICE_ACCOUNT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query [key1] -o tsv)
    _AZURE_IOTHUB_CONN_STRING=$(az iot hub connection-string show -n "$_AZURE_IOTHUB_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query connectionString -o tsv)
    _AZURE_LOG_ANALYTICS_SHARED_KEY=$(az monitor log-analytics workspace get-shared-keys -n "$_AZURE_LOG_ANALYTICS_WORKSPACE_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query primarySharedKey -o tsv)
    _AZURE_ACR_USERNAME=$(az acr credential show -n "$_AZURE_ACR_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query username -o tsv)
    _AZURE_ACR_PASSWORD=$(az acr credential show -n "$_AZURE_ACR_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query passwords[0].value -o tsv)
    # FRom static configs
    CONFIG_AZURE_COGNITIVE_SERVICE_SPEECH_ENDPOINT=${CONFIG_AZURE_COGNITIVE_SERVICE_SPEECH_ENDPOINT/PARAM_AZURE_LOCATION/$PARAM_AZURE_LOCATION}
    # Update config
    # Check if env file exists, else create it from template
    if [ ! -f "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env" ]; then
        cp "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env_template" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    fi
    sed -i "s|AZURE_COGNITIVE_SERVICE_SPEECH_ENDPOINT=.*|AZURE_COGNITIVE_SERVICE_SPEECH_ENDPOINT=\"$CONFIG_AZURE_COGNITIVE_SERVICE_SPEECH_ENDPOINT\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|AZURE_COGNITIVE_SERVICE_SPEECH_KEY=.*|AZURE_COGNITIVE_SERVICE_SPEECH_KEY=\"$_AZURE_COGNITIVE_SERVICE_KEY\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|AZURE_COGNITIVE_SERVICE_FORMRECOG_ENDPOINT=.*|AZURE_COGNITIVE_SERVICE_FORMRECOG_ENDPOINT=\"$_AZURE_COGNITIVE_SERVICE_ENDPOINT\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|AZURE_COGNITIVE_SERVICE_FORMRECOG_KEY=.*|AZURE_COGNITIVE_SERVICE_FORMRECOG_KEY=\"$_AZURE_COGNITIVE_SERVICE_KEY\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|AZURE_COGNITIVE_SERVICE_FORMRECOG_MODEL_ID=.*|AZURE_COGNITIVE_SERVICE_FORMRECOG_MODEL_ID=\"$CONFIG_AZURE_FORM_RECOG_MODEL_ID\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|ACR_USERNAME=.*|ACR_USERNAME=\"$_AZURE_ACR_USERNAME\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|ACR_PASSWORD=.*|ACR_PASSWORD=\"$_AZURE_ACR_PASSWORD\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|ACR_ADDRESS=.*|ACR_ADDRESS=\"$_AZURE_ACR_LOGIN_SERVER\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|LOG_ANALYTICS_WORKSPACE_ID=.*|LOG_ANALYTICS_WORKSPACE_ID=\"$_AZURE_LOG_ANALYTICS_WORKSPACE_ID\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|LOG_ANALYTICS_SHARED_KEY=.*|LOG_ANALYTICS_SHARED_KEY=\"$_AZURE_LOG_ANALYTICS_SHARED_KEY\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|IOT_HUB_RESOURCE_ID=.*|IOT_HUB_RESOURCE_ID=\"$_AZURE_IOTHUB_RESOURCE_ID\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|APPINSIGHTS_CONNECTION_STRING=.*|APPINSIGHTS_CONNECTION_STRING=\"$_AZURE_APP_INSIGHTS_CONNECTION_STRING\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|BLOB_STORAGE_CONN_STRING=.*|BLOB_STORAGE_CONN_STRING=\"$_AZURE_BLOB_STORAGE_CONN_STRING\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    sed -i "s|STORE_ID=.*|STORE_ID=\"$CONFIG_AZURE_IOT_DEVICE_STORE_ID\"|g" "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/.env"
    # shellcheck disable=SC2034
    AZURE_IOTHUB_CONNECTION_STRING="$_AZURE_IOTHUB_CONN_STRING"
    logger "INFO: Config update completed"
}

## Iot edge solution applications build
application_build() {
    logger "INFO: Building Iot Edge Solution..."
    if [ -z "$AZURE_DEPLOYMENT_NAME" ]; then
        logger "ERROR: Deployment name is not set. Please set it using -n option."
        exit 2
    fi
    _azure_create_iot_device
    if [ "$PARAM_IOT_DEVICE_CPU_ARCHITECTURE" == "amd64" ] || [ "$PARAM_IOT_DEVICE_CPU_ARCHITECTURE" == "arm64v8" ]; then
        logger "INFO: Target architecture for build is $PARAM_IOT_DEVICE_CPU_ARCHITECTURE"
    else
        logger "ERROR: Unsupported target architecture please set it using -p option, supported modes are: amd64, arm64v8"
        exit 2
    fi
    cd "$CONFIG_AZURE_IOT_SOLUTION_FOLDER" && iotedgedev build -P "$PARAM_IOT_DEVICE_CPU_ARCHITECTURE"
    logger "INFO: Iot Edge Solution Build completed"
}

## Iot edge solution applications deployment
application_deploy() {
    logger "INFO: Running app deploy..."
    if [ "$PARAM_IOT_DEVICE_CPU_ARCHITECTURE" == "amd64" ] || [ "$PARAM_IOT_DEVICE_CPU_ARCHITECTURE" == "arm64v8" ]; then
        logger "INFO: Target architecture for build is $PARAM_IOT_DEVICE_CPU_ARCHITECTURE"
    else
        logger "ERROR: Unsupported target architecture please set it using -p option, supported modes are: amd64, arm64v8"
        exit 2
    fi
    if [ -z "$AZURE_DEPLOYMENT_NAME" ]; then
        logger "ERROR: Deployment name is not set. Please set it using -n option."
        exit 2
    fi
    if [ "$PARAM_IOT_DEVICE_DEPLOYMENT_MODE" == "simulated" ]; then
        logger "INFO: Iot Edge Simulator is starting, press Ctrl+C to stop..."
        cd "$CONFIG_AZURE_IOT_SOLUTION_FOLDER" && iotedgedev start -u -s -v -P "$PARAM_IOT_DEVICE_CPU_ARCHITECTURE" -f "config/deployment.$PARAM_IOT_DEVICE_CPU_ARCHITECTURE.json"
    elif [ "$PARAM_IOT_DEVICE_DEPLOYMENT_MODE" == "edge" ]; then
        _azure_acr_login
        cd "$CONFIG_AZURE_IOT_SOLUTION_FOLDER" && iotedgedev build -P "$PARAM_IOT_DEVICE_CPU_ARCHITECTURE" -p
        # shellcheck disable=SC2153
        az iot edge set-modules --device-id "$PARAM_IOT_DEVICE_ID" --hub-name "$AZURE_IOTHUB_NAME" --content "$CONFIG_AZURE_IOT_SOLUTION_FOLDER/config/deployment.$PARAM_IOT_DEVICE_CPU_ARCHITECTURE.json"
        logger "INFO: Iot Edge deployment is completed, to check the result go to Azure Portal -> IoT Hub and make sure the device is connected with IoT Hub"
    else
        logger "ERROR: Deployment mode is not set, please set it using -m option, supported modes are: simulated, edge"
        exit 2
    fi
    logger "INFO: App deploy completed"
}

## Azure ACR login
_azure_acr_login() {
    logger "INFO: Logging into Azure Container Registry..."
    _AZURE_ACR_NAME=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.acrName.value -o tsv)
    az acr login --name "$_AZURE_ACR_NAME"
    logger "INFO: Azure Container Registry logged in"
}
