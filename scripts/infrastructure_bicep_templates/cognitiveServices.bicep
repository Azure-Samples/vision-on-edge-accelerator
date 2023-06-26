// Cognitive Service Resource
param cognitiveServiceName string
param restoreCogsService bool
param location string
param logAnalyticsID string

resource cognitiveServiceResource 'Microsoft.CognitiveServices/accounts@2021-10-01' = {
  name: cognitiveServiceName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'CognitiveServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    apiProperties: {}
    customSubDomainName: cognitiveServiceName
    publicNetworkAccess: 'Enabled'
    restore: restoreCogsService
  }
}

var cognitiveSettingName = 'CognitiveDiag'

// Enabling Diganostic Setting for Cognitive Service Resource
resource cognitiveServiceSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: cognitiveSettingName
  scope: cognitiveServiceResource
  properties: {
    workspaceId: logAnalyticsID
    logs: [
      {
        category: 'Audit'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
      {
        category: 'RequestResponse'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
      {
        category: 'Trace'
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

output cognitiveServiceAccountName string = cognitiveServiceResource.name
output cognitiveServiceAccountEndpoint string = cognitiveServiceResource.properties.endpoint
