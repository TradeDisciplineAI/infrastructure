variable "location" {
  description = "The Azure region where resources will be created."
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "The name of the Azure Resource Group."
  type        = string
  default     = "trading-rg"
}

variable "project_name" {
  description = "The name of the trading platform project."
  type        = string
  default     = "trading"
}

variable "environment" {
  description = "The target deployment environment (e.g., development, staging, production)."
  type        = string
  default     = "development"
}

# ── Networking Variables ───────────────────────────────────────────────────
variable "vnet_name" {
  description = "The name of the Azure Virtual Network (VNet)."
  type        = string
  default     = "trading-vnet"
}

variable "vnet_address_space" {
  description = "The address space for the Azure Virtual Network."
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "aks_subnet_name" {
  description = "The name of the dedicated subnet for AKS nodes."
  type        = string
  default     = "aks-subnet"
}

variable "aks_subnet_address_prefixes" {
  description = "The address prefixes for the dedicated AKS node subnet."
  type        = list(string)
  default     = ["10.0.1.0/24"]
}

# ── ACR Variables ──────────────────────────────────────────────────────────
variable "acr_name" {
  description = "The name of the Azure Container Registry (must be alphanumeric only)."
  type        = string
  default     = "tradingacr"
}

variable "acr_sku" {
  description = "The SKU of the Azure Container Registry (Basic, Standard, Premium)."
  type        = string
  default     = "Basic"
}

# ── AKS Variables ──────────────────────────────────────────────────────────
variable "aks_name" {
  description = "The name of the Azure Kubernetes Service cluster."
  type        = string
  default     = "trading-aks"
}

variable "aks_dns_prefix" {
  description = "The DNS prefix for the Azure Kubernetes Service cluster."
  type        = string
  default     = "trading-aks-dns"
}

variable "aks_node_count" {
  description = "The initial number of nodes in the default AKS node pool."
  type        = number
  default     = 2
}

variable "aks_vm_size" {
  description = "The Virtual Machine SKU size for AKS node pool instances."
  type        = string
  default     = "Standard_D2s_v5"
}
