// IotHub Resource
param iotHubName string
param location string
param iotHubSkuName string
param iotHubSkuCapacity int
param messageRetentionDays int
param d2cPartitions int
param logAnalyticsID string
var iotHubConsumerGroupName = 'consumer'

resource iotHubResource 'Microsoft.Devices/IotHubs@2021-07-02' = {
  name: iotHubName
  location: location
  sku: {
    name: iotHubSkuName
    capacity: iotHubSkuCapacity
  }
  identity: {
    type: 'None'
  }
  properties: {
    ipFilterRules: []
    eventHubEndpoints: {
      events: {
        retentionTimeInDays: messageRetentionDays
        partitionCount: d2cPartitions
      }
    }
    routing: {
      endpoints: {
        serviceBusQueues: []
        serviceBusTopics: []
        eventHubs: []
        storageContainers: []
      }
      routes: []
      fallbackRoute: {
        name: '$fallback'
        source: 'DeviceMessages'
        condition: 'true'
        endpointNames: [
          'events'
        ]
        isEnabled: true
      }
    }
    messagingEndpoints: {
      fileNotifications: {
        lockDurationAsIso8601: 'PT1M'
        ttlAsIso8601: 'PT1H'
        maxDeliveryCount: 10
      }
    }
    enableFileUploadNotifications: false
    cloudToDevice: {
      maxDeliveryCount: 10
      defaultTtlAsIso8601: 'PT1H'
      feedback: {
        lockDurationAsIso8601: 'PT1M'
        ttlAsIso8601: 'PT1H'
        maxDeliveryCount: 10
      }
    }
    features: 'None'
    disableLocalAuth: false
    allowedFqdnList: []
  }
}

// IoTHub Consumer Resource
resource iotHubEventHubEndpointConsumerGroupResource 'Microsoft.Devices/IotHubs/eventHubEndpoints/ConsumerGroups@2020-08-01' = {
  name: '${iotHubName}/events/${iotHubConsumerGroupName}'
  properties: {
    name: iotHubConsumerGroupName
  }
  dependsOn: [
    iotHubResource
  ]
}

var iotdiagSettingName = 'iotHubDiag'
// Enabling Diganostic Setting for IoTHub
resource iothubname_Microsoft_Insights_settingName 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: iotdiagSettingName
  scope: iotHubResource
  properties: {
    workspaceId: logAnalyticsID
    logs: [
      {
        category: 'Connections'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
      {
        category: 'Configurations'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
      {
        category: 'D2CTwinOperations'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
      {
        category: 'C2DTwinOperations'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
    ]
  }
}
output iotHubName string = iotHubResource.name
output iotHubResourceId string = iotHubResource.id
