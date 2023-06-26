// Log Analytics Resource
param location string 
param workspaceName string
param sku string
param retentionDays int
resource log_analytics 'Microsoft.OperationalInsights/workspaces@2020-03-01-preview' = {
  location: location
  name: workspaceName
  properties: {
    sku: {
      name: sku
    }
    retentionInDays: retentionDays
  }
}

output loganalyticsResourceID string = log_analytics.id
output loganalyticsWorkspaceID string = log_analytics.properties.customerId
output loganalyticsWorkspaceName string = log_analytics.name
