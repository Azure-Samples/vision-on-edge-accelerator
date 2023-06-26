#!/bin/bash
#
# Purpose: This script contains the common functions for the infrastructure.
#

# Provision infrastructure using bicep scripts
infrastructure_provision() {
    _azure_create_resource_group
    logger "INFO: Running infra provision..."
    _AZURE_DEPLOYMENT_NAME=LabelReaderDeployment"$(date +"%d-%b-%Y-%H-%M-%S")"
    az deployment group create \
        --name "$_AZURE_DEPLOYMENT_NAME" \
        --resource-group "$PARAM_AZURE_RESOURCE_GROUP_NAME" \
        --template-file "$CONFIG_BICEP_SCRIPT_FOLDER/main.bicep" \
        --parameters "$CONFIG_BICEP_SCRIPT_FOLDER/parameters.json"
    _PROVISION_STATUS=$(az deployment group show -n "$_AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.provisioningState -o tsv)
    if [ "$_PROVISION_STATUS" != "Succeeded" ]; then
        _PROVISION_ERROR_CODE=$(az deployment group show -n "$_AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query "properties.error.details[0].code" -o tsv)
        # Fix for Azure Cognitive Service creation error, when the resource group is deleted and recreated
        if [ "$_PROVISION_ERROR_CODE" == "FlagMustBeSetForRestore" ]; then
            logger "WARN: Provisioning failed. Azure Cognitive Service needs to be restored. Trying to restore it..."
            az deployment group create \
                --name "$_AZURE_DEPLOYMENT_NAME" \
                --resource-group "$PARAM_AZURE_RESOURCE_GROUP_NAME" \
                --template-file "$CONFIG_BICEP_SCRIPT_FOLDER/main.bicep" \
                --parameters "$CONFIG_BICEP_SCRIPT_FOLDER/parameters.json" \
                --parameters restoreCogsService=true
            _PROVISION_STATUS=$(az deployment group show -n "$_AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.provisioningState -o tsv)
            if [ "$_PROVISION_STATUS" != "Succeeded" ]; then
                logger "ERROR: Provisioning failed. Please check the logs and try again."
                exit 2
            fi
        else
            logger "ERROR: Provisioning failed. Please check the logs and try again."
            exit 2
        fi
    fi
    # shellcheck disable=SC2034
    AZURE_DEPLOYMENT_NAME="$_AZURE_DEPLOYMENT_NAME"
    _azure_create_iot_device
    _azure_form_recog_copy_model
    logger "INFO: Infra provision completed, created deployment: ${_AZURE_DEPLOYMENT_NAME}"
}

# List Azure Deployments for a resource group
list_azure_deployments() {
    logger "INFO: Listing Azure deployments..."
    az deployment group list -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query "[?contains(name, 'LabelReaderDeployment')].{Name:name, ProvisioningState:properties.provisioningState, Timestamp:properties.timestamp}" -o table
}

## Create Azure Resource Group (will not fail if already exists)
_azure_create_resource_group() {
    logger "INFO: Creating resource group..."
    az group create --name "$PARAM_AZURE_RESOURCE_GROUP_NAME" --location "$PARAM_AZURE_LOCATION"
    _AZURE_SUBSCRIPTION_NAME=$(az account show --query name -o tsv)
    logger "INFO: Created resource group $PARAM_AZURE_RESOURCE_GROUP_NAME location: $PARAM_AZURE_LOCATION subscription: $_AZURE_SUBSCRIPTION_NAME"
}

## Copy pre-trained Azure Form Recognizer custom model from source resource to newly created resource
_azure_form_recog_copy_model() {
    logger "INFO: Copying Azure Form Recognizer custom model..."
    if [ -z "$AZURE_DEPLOYMENT_NAME" ]; then
        logger "ERROR: Deployment name is not set. Please set it using -n option."
        exit 2
    fi
    _AZURE_COGNITIVE_SERVICE_ENDPOINT=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.cognitiveServiceAccountEndpoint.value -o tsv)
    _AZURE_COGNITIVE_SERVICE_ACCOUNT_NAME=$(az deployment group show -n "$AZURE_DEPLOYMENT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query properties.outputs.cognitiveServiceAccountName.value -o tsv)
    _AZURE_COGNITIVE_SERVICE_KEY=$(az cognitiveservices account keys list -n "$_AZURE_COGNITIVE_SERVICE_ACCOUNT_NAME" -g "$PARAM_AZURE_RESOURCE_GROUP_NAME" --query [key1] -o tsv)
    python "$CONFIG_AZURE_FORM_RECOG_COPY_MODEL" \
        --source-endpoint "$PARAM_SOURCE_AZURE_FORM_RECOG_ENDPOINT" \
        --source-key "$PARAM_SOURCE_AZURE_FORM_RECOG_KEY" \
        --dest-endpoint "$_AZURE_COGNITIVE_SERVICE_ENDPOINT" \
        --dest-key "$_AZURE_COGNITIVE_SERVICE_KEY" \
        --model-id "$CONFIG_AZURE_FORM_RECOG_MODEL_ID"
    logger "INFO: Copied Azure Form Recognizer custom model"
}