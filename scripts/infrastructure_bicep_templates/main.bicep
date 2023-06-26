@minLength(3)
@maxLength(15)
param projectName string = 'labelreader'
param projectEnvironment string
param iotHubSkuName string
param iotHubSkuCapacity int
param msgRetentionDays int
param d2cPartitions int // partitions used for the event stream
param location string = resourceGroup().location
param sku string // For Log Analytics
param acrSku string
param dataRetention int
param restoreCogsService bool

param cognitiveServiceName string = 'cogs${projectName}${projectEnvironment}${uniqueString(resourceGroup().id)}' // Name of the cognitive service
param storageAccountName string = 'store${projectEnvironment}${uniqueString(resourceGroup().id)}' // Name of the storage account
param iotHubName string = 'iot${projectName}${projectEnvironment}${uniqueString(resourceGroup().id)}' // Name of the IoTHub Service
param workspaceName string = 'log${projectName}${projectEnvironment}${uniqueString(resourceGroup().id)}' // Name of the Log Analytics Service
param appInsightsName string = 'appins${projectName}${projectEnvironment}${uniqueString(resourceGroup().id)}' // Name of the App Insights Service
param acrName string = 'acr${projectName}${projectEnvironment}${uniqueString(resourceGroup().id)}' // Name of the Log Analytics Service

module logAnalyticsWorkspace 'logAnalyticsWorkspace.bicep' = {
  name: workspaceName
  params: {
    location: location
    workspaceName: workspaceName
    retentionDays: dataRetention
    sku: sku
  }
}
module iotHub 'iotHub.bicep' = {
  name: iotHubName
  params: {
    iotHubName: iotHubName
    iotHubSkuCapacity: iotHubSkuCapacity
    iotHubSkuName: iotHubSkuName
    location: location
    logAnalyticsID: logAnalyticsWorkspace.outputs.loganalyticsResourceID
    d2cPartitions: d2cPartitions
    messageRetentionDays: msgRetentionDays
  }
}

module storage 'storage.bicep' = {
  name: storageAccountName
  params: {
    storageAccountName: storageAccountName
    location: location
    logAnalyticsID: logAnalyticsWorkspace.outputs.loganalyticsResourceID
  }
}

module cognitiveServices 'cognitiveServices.bicep' = {
  name: cognitiveServiceName
  params: {
    location: location
    cognitiveServiceName: cognitiveServiceName
    restoreCogsService: restoreCogsService
    logAnalyticsID: logAnalyticsWorkspace.outputs.loganalyticsResourceID

  }
}

module appInsights 'appInsights.bicep' = {
  name: appInsightsName
  params: {
    location: location
    appInsightsName: appInsightsName
    workSpaceResourceID: logAnalyticsWorkspace.outputs.loganalyticsResourceID

  }
}

module containerRegistry 'containerRegistry.bicep' = {
  name: acrName
  params: {
    acrName: acrName
    location: location
    acrAdminUserEnabled: true
    acrSku: acrSku
  }
}

output storageAccountName string = storage.outputs.storageAccountName
output iotHubName string = iotHub.outputs.iotHubName
output appInsightsConnectionString string = appInsights.outputs.appInsightsConnectionString
output appInsightsInstrumentationKey string = appInsights.outputs.appInsightsInstrumentationKey
output cognitiveServiceAccountName string = cognitiveServices.outputs.cognitiveServiceAccountName
output cognitiveServiceAccountEndpoint string = cognitiveServices.outputs.cognitiveServiceAccountEndpoint
output loganalyticsWorkspaceResourceID string = logAnalyticsWorkspace.outputs.loganalyticsResourceID
output loganalyticsWorkspaceID string = logAnalyticsWorkspace.outputs.loganalyticsWorkspaceID
output loganalyticsWorkspaceName string = logAnalyticsWorkspace.outputs.loganalyticsWorkspaceName
output iotHubResourceId string = iotHub.outputs.iotHubResourceId
output acrLoginServer string = containerRegistry.outputs.acrLoginServer
output acrName string = containerRegistry.outputs.acrName
