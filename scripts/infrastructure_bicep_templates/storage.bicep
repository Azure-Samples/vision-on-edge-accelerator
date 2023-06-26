// Storage Account Resource
param storageAccountName string
param location string
param logAnalyticsID string

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-08-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: true
    allowSharedKeyAccess: true
    networkAcls: {
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: []
      defaultAction: 'Allow'
    }
    supportsHttpsTrafficOnly: true
    accessTier: 'Hot'
  }
}

resource storageAccountBlob 'Microsoft.Storage/storageAccounts/blobServices@2021-08-01' = {
  parent: storageAccount
  name: 'default'
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
  properties: {
    changeFeed: {
      enabled: false
    }
    restorePolicy: {
      enabled: false
    }
    cors: {
      corsRules: []
    }
    deleteRetentionPolicy: {
      enabled: true
      days: 7
    }
    isVersioningEnabled: false
  }
}

resource storageAccountBlob_data 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-08-01' = {
  parent: storageAccountBlob
  name: 'data'
  properties: {
    defaultEncryptionScope: '$account-encryption-key'
    denyEncryptionScopeOverride: false
    publicAccess: 'None'
  }
  dependsOn: [
    storageAccount
  ]
}
//Enabling Diganostic Setting for Storage Account
var storagediagsettingName = 'diagnostics'
resource storage_Microsoft_Insights_settingName 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: storagediagsettingName
  scope: storageAccount
  properties: {
    workspaceId: logAnalyticsID
    metrics: [
      {
        category: 'Transaction'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
    ]
  }
}

var blobdiagsettingName = 'diagnostics'
// Enabling Diganostic Setting for Storage Account Blob
resource storage_blob_Microsoft_Insights_settingName 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: blobdiagsettingName
  scope: storageAccountBlob
  properties: {
    workspaceId: logAnalyticsID
    metrics: [
      {
        category: 'Transaction'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
    ]
  }
}

output storageAccountName string = storageAccount.name
