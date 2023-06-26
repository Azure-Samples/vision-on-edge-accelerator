#!/bin/bash
# shellcheck disable=SC2034,SC1091
#
# Purpose: This script is used to enable onelcik deployment of the application on the target environment.
# 
# Scope:
#   1. Provision required Azure resources
#   2. Update the application configuration
#   2. Build and Deploy the application
#

## Logger
logger() {
    date +"%D-%R: $*"
}

## Usage
usage() {
    echo ""
    echo ""
    echo "Usage: $0 -a -i -c -b -d -L -f <source-azure-form-recog-endpoint> -k <source-azure-form-recog-key> -m <deployment-mode> \\"
    echo "              -r <resource-group> -l <location-name> -e <azure-iot-edge-device-id> \\"
    echo "              -o <OS Type> -p <azure-iot-edge-device-cpu-arch> -n <azure-infra-deployment-name>"
    echo "  -a: bool: Enable full (E2E) onelick deployment (default: true, nonmandatory)"
    echo "  -i: bool: Enable only infrastructure deployment (default: false, nonmandatory)"
    echo "  -c: bool: Enable only application configuration update (default: false, nonmandatory)"
    echo "  -b: bool: Enable only application build (default: false, nonmandatory)"
    echo "  -d: bool: Enable only application deployment (default: false, nonmandatory)"
    echo "  -L: bool: List all Azure deployments for a resource group (default: false, nonmandatory)"
    echo "  -f: string: Source Azure Form Recognizer endpoint (mandatory with -a (default) and -i options)"
    echo "  -k: string: Source Azure Form Recognizer key (mandatory with -a (default) and -i options)"
    echo "  -m: string: Application deployment mode (default: simulated, nonmandatory) possible values: simulated, edge"
    echo "  -r: string: Resource group name (default: labelreader-demo-environment, nonmandatory)"
    echo "  -l: string: Location (default: eastus2, nonmandatory)"
    echo "  -e: string: Azure IoT Edge device name (default: labelreader-device, nonmandatory)"
    echo "  -o: string: OS Type (default: linux, nonmandatory) possible values: linux, windows"
    echo "  -p: string: Azure IoT Edge device CPU architechture (default: amd64, nonmandatory) possible values: amd64, arm64v8"
    echo "  -n: string: Azure infrastructure deployment name (nonmandatory, mandatory if -c or -d)"
    echo "  -h: bool: Show this help (nonmandatory)"
    echo ""
    echo "Example 1 (using all default): $0"
    echo "Example 2 (mention resource group, location etc.): $0 -a -r my-demo-rg -l eastus2 -e my-demo-edge-device"
    echo "Example 3 (only config update): $0 -c -n LabelReaderDeployment24-Aug-2022-13-36-39"
    echo "Example 4 (only application deploy): $0 -d -n LabelReaderDeployment24-Aug-2022-13-36-39"
    echo ""
    echo "NOTE: If there are multiple azure subscriptions, set the respective subscription using 'az account set --name <subscription-name>'"
    exit 1
}

## Configurations
CONFIG_IOT_EDGE_WINDOWS_RUNTIME_VERSION="1.2"
CONFIG_IOT_EDGE_LINUX_RUNTIME_VERSION="1.4"
CONFIG_BICEP_SCRIPT_FOLDER="infrastructure_bicep_templates"
CONFIG_AZURE_IOT_SOLUTION_FOLDER="../label-reader"
CONFIG_AZURE_COGNITIVE_SERVICE_SPEECH_ENDPOINT="https://PARAM_AZURE_LOCATION.tts.speech.microsoft.com/cognitiveservices/v1"
CONFIG_AZURE_IOT_DEVICE_STORE_ID="demo-store"
CONFIG_AZURE_FORM_RECOG_COPY_MODEL="library_script/azure_form_recog_copy_model.py"
CONFIG_AZURE_FORM_RECOG_MODEL_ID="order-label-reader-neural-model-ga-v1"

## Variables declaration
AZURE_DEPLOYMENT_NAME=""
AZURE_IOT_DEVICE_CONNECTION_STRING=""
AZURE_IOTHUB_NAME=""
AZURE_IOTHUB_CONNECTION_STRING=""

## Input parameters and their default values
PARAM_E2E='true'
PARAM_INFRA_PROVISION='false'
PARAM_CONFIG_UPDATE='false'
PARAM_APP_BUILD='false'
PARAM_APP_DEPLOY='false'
PARAM_LIST_DEPLOYMENTS='false'
PARAM_SOURCE_AZURE_FORM_RECOG_ENDPOINT=""
PARAM_SOURCE_AZURE_FORM_RECOG_KEY=""
PARAM_AZURE_RESOURCE_GROUP_NAME="labelreader-demo-environment"
PARAM_AZURE_LOCATION='eastus2'
PARAM_IOT_DEVICE_ID='labelreader-device'
PARAM_OS_TYPE='linux'
PARAM_IOT_DEVICE_CPU_ARCHITECTURE='amd64'
PARAM_IOT_DEVICE_DEPLOYMENT_MODE='simulated'
while getopts "aicbdLf:k:m:r:l:e:o:p:n:h" OPTKEY; do
  case $OPTKEY in
    a)
        PARAM_E2E="true"
        ;;
    i)
        PARAM_INFRA_PROVISION="true"
        PARAM_E2E="false"
        ;;
    c)
        PARAM_CONFIG_UPDATE="true"
        PARAM_E2E="false"
        ;;
    b)
        PARAM_APP_BUILD="true"
        PARAM_E2E="false"
        ;;
    d)
        PARAM_APP_DEPLOY="true"
        PARAM_APP_BUILD="true" # App build is mandatory for app deployment
        PARAM_E2E="false"
        ;;
    L)
        PARAM_LIST_DEPLOYMENTS="true"
        PARAM_E2E="false"
        ;;
    f)
        PARAM_SOURCE_AZURE_FORM_RECOG_ENDPOINT="${OPTARG}"
        ;;
    k)
        PARAM_SOURCE_AZURE_FORM_RECOG_KEY="${OPTARG}"
        ;;
    m)
        PARAM_IOT_DEVICE_DEPLOYMENT_MODE="${OPTARG}"
        ;;
    r)
        PARAM_AZURE_RESOURCE_GROUP_NAME="${OPTARG}"
        ;;
    l)
        PARAM_AZURE_LOCATION="${OPTARG}"
        ;;
    e)
        PARAM_IOT_DEVICE_ID="${OPTARG}"
        ;;
    o)
        PARAM_OS_TYPE="${OPTARG}"
        ;;
    p)
        PARAM_IOT_DEVICE_CPU_ARCHITECTURE="${OPTARG}"
        ;;
    n)
        AZURE_DEPLOYMENT_NAME="${OPTARG}"
        ;;
    h)
        usage
        ;;
    \?)
        logger "ERROR: Invalid option: -$OPTARG" >&2
        usage
        ;;
    :)
        logger "ERROR: Option -$OPTARG requires an argument." >&2
        usage
        ;;
    *)
        logger "ERROR: Unimplemented option -- ${OPTKEY}" >&2
        usage
        ;;
  esac
done

## Input parameters validation
if [ "$PARAM_E2E" == "true" ] || [ "$PARAM_INFRA_PROVISION" == "true" ]; then
    if [ -z "$PARAM_SOURCE_AZURE_FORM_RECOG_ENDPOINT" ]; then
        logger "ERROR: Source Azure Form Recognizer endpoint is mandatory with -a (default) and -i options" >&2
        usage
    fi
    if [ -z "$PARAM_SOURCE_AZURE_FORM_RECOG_KEY" ]; then
        logger "ERROR: Source Azure Form Recognizer key is mandatory with -a (default) and -i options" >&2
        usage
    fi
fi

## Functions

### Infrastructure functions
# shellcheck source=./library_script/infrastructure.sh
source ./library_script/infrastructure.sh

### Application functions
# shellcheck source=./library_script/application.sh
source ./library_script/application.sh

### Common functions
# shellcheck source=./library_script/common.sh
source ./library_script/common.sh

### Environment check
check_environment() {
    logger "INFO: Chcecking environment..."
    logger "INFO: Checking if docker is installed..."
    if ! command -v docker >/dev/null 2>&1; then
        logger "ERROR: Docker is not installed. Please install docker and try again."
        exit 1
    fi
    logger "INFO: Checking if docker is running..."
    if ! docker info >/dev/null 2>&1; then
        logger "ERROR: Docker is not running. Please start docker and check using 'docker info' and try again."
        exit 1
    fi
    logger "INFO: Checking if iotedgedev is installed..."
    if ! command -v iotedgedev >/dev/null 2>&1; then
        logger "ERROR: iotedgedev is not installed. Please install iotedgedev using 'pip install iotedgedev' and try again."
        exit 1
    fi
    logger "INFO: Checking if iotedgehubdev is installed..."
    if ! command -v iotedgehubdev >/dev/null 2>&1; then
        logger "ERROR: iotedgehubdev is not installed. Please install iotedgehubdev using 'pip install iotedgehubdev' and try again."
        exit 1
    fi
    logger "INFO: Checking if azure cli is installed..."
    if ! command -v az > /dev/null; then
        logger "ERROR: Azure cli is not installed. Please install it and try again."
        exit 2
    fi
    logger "INFO: Checking if azure cli is authenticated..."
    if ! az account show > /dev/null; then
        logger "ERROR: Azure cli is not authenticated. Please authenticate using 'az login' and try again."
        exit 2
    fi
    logger "INFO: Checking if azure bicep cli is installed..."
    if ! az bicep version > /dev/null; then
        logger "ERROR: Azure bicep cli is not installed. Please install it using 'az bicep install' and try again."
        exit 2
    fi
    logger "INFO: Checking if azure iot extension is installed..."
    if ! az extension show -n azure-iot --query version -o tsv > /dev/null; then
        logger "ERROR: Azure iot extension is not installed. Please install it using 'az extension add --name azure-iot' and try again."
        exit 2
    fi
}

### E2E deployment
e2e() {
    logger "INFO: Running e2e deploymen..."
    infrastructure_provision
    application_config_update
    application_build
    application_deploy
    logger "INFO: E2E deployment completed"
}

### Logging final notes for future reference
final_message() {
    logger "INFO: Deployment completed"
    logger "==================NOTES========================"
    if [ "$AZURE_IOT_DEVICE_CONNECTION_STRING" != "" ]; then
        logger "INFO: Azure IoT Edge device connection string: $AZURE_IOT_DEVICE_CONNECTION_STRING"
    fi
    if [ "$AZURE_IOTHUB_CONNECTION_STRING" != "" ]; then
        logger "INFO: Azure IoT hub connection string: $AZURE_IOTHUB_CONNECTION_STRING"
    fi
    if [ "$AZURE_DEPLOYMENT_NAME" != "" ]; then
        logger "INFO: Azure infrastructure deployment name: $AZURE_DEPLOYMENT_NAME"
    fi
    logger "==============================================="
}

## Main
check_environment
if [ "$PARAM_LIST_DEPLOYMENTS" == "true" ]; then
    list_azure_deployments
    echo ""
    logger "INFO: The latest successful deployment name can be used in the -n parameter for deploy or config-update commands"
    exit 0
fi
if [ "$PARAM_E2E" == "true" ]; then
    e2e
else
    if [ "$PARAM_INFRA_PROVISION" == "true" ]; then
        infrastructure_provision
    fi
    if [ "$PARAM_CONFIG_UPDATE" == "true" ]; then
        application_config_update
    fi
    if [ "$PARAM_APP_BUILD" == "true" ]; then
        application_build
    fi
    if [ "$PARAM_APP_DEPLOY" == "true" ]; then
        application_deploy
    fi
fi
final_message
exit 0