output "resource_group_name" {
  description = "The name of the created Azure Resource Group."
  value       = azurerm_resource_group.rg.name
}

output "resource_group_location" {
  description = "The Azure region/location of the created Resource Group."
  value       = azurerm_resource_group.rg.location
}

output "resource_group_id" {
  description = "The Azure Resource Manager ID of the Resource Group."
  value       = azurerm_resource_group.rg.id
}

# ── Networking Outputs ─────────────────────────────────────────────────────
output "vnet_name" {
  description = "The name of the Azure Virtual Network."
  value       = azurerm_virtual_network.vnet.name
}

output "vnet_id" {
  description = "The Azure Resource Manager ID of the Virtual Network."
  value       = azurerm_virtual_network.vnet.id
}

output "aks_subnet_name" {
  description = "The name of the dedicated AKS subnet."
  value       = azurerm_subnet.aks_subnet.name
}

output "aks_subnet_id" {
  description = "The Azure Resource Manager ID of the dedicated AKS subnet."
  value       = azurerm_subnet.aks_subnet.id
}

# ── ACR Outputs ────────────────────────────────────────────────────────────
output "acr_name" {
  description = "The name of the Azure Container Registry."
  value       = azurerm_container_registry.acr.name
}

output "acr_login_server" {
  description = "The login server URL for the Azure Container Registry."
  value       = azurerm_container_registry.acr.login_server
}

output "acr_id" {
  description = "The Azure Resource Manager ID of the Azure Container Registry."
  value       = azurerm_container_registry.acr.id
}

# ── AKS Outputs ────────────────────────────────────────────────────────────
output "aks_cluster_name" {
  description = "The name of the Azure Kubernetes Service cluster."
  value       = azurerm_kubernetes_cluster.aks.name
}

output "aks_cluster_id" {
  description = "The Azure Resource Manager ID of the AKS cluster."
  value       = azurerm_kubernetes_cluster.aks.id
}

output "aks_fqdn" {
  description = "The FQDN of the Azure Kubernetes Service API server."
  value       = azurerm_kubernetes_cluster.aks.fqdn
}

output "aks_kubelet_identity_object_id" {
  description = "The Principal ID of the Kubelet Managed Identity."
  value       = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}

output "aks_node_resource_group" {
  description = "The auto-generated Resource Group containing worker node infrastructure."
  value       = azurerm_kubernetes_cluster.aks.node_resource_group
}
