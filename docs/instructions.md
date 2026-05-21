----------------------------------------
-- Create Azure SQL Database & Server --
----------------------------------------
  DB_SERVER: abin-sql-server-2026.database.windows.net
  DB_NAME: userdb
  DB_USER: sqladmin
  DB_PASSWORD: Mysql123

Location: Asia Pacific South East Asia

# To create table in Azure SQL Query Editor

CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(100)
);

------------------------------------------
------- DEBUG Azure SQL ISSUE ------------
------------------------------------------
CMD:
	ping abin-sql-server-2026.database.windows.net  (test whether the server is reachable)

	nslookup abin-sql-server-2026.database.windows.net  (lookup the domain name and ip address it belongs to)

POWERSHELL:

	Test-NetConnection abin-sql-server-2026.database.windows.net -Port 1433  (check if TCP port opens on a target machine)

Azure Firewall issue (for laptop)
   - + Add your client IPv4 address

------------------------------------------------------------------------------
-- What You Need for AKS (add AKS outbound IP in azure SQL server firewall) --
------------------------------------------------------------------------------

How To Do It

# Step 1 — Get AKS Outbound Public IP #

Run:

az aks show \
  --resource-group <RESOURCE_GROUP> \
  --name <AKS_CLUSTER_NAME> \
  --query networkProfile.loadBalancerProfile.effectiveOutboundIPs \
  -o table

az aks show --resource-group abindev-rg --name aks-practice-cluster --query networkProfile.loadBalancerProfile.effectiveOutboundIPs -o table


# Step 2 Get the AKS outbound public ip 


az network public-ip list \
  --resource-group MC_<RG>_<AKSNAME>_<REGION> \
  -o table

az network public-ip list --resource-group MC_abindev-rg_aks-practice-cluster_southeastasia -o table

You’ll get something like:

52.xx.xx.xx

That is the IP Azure SQL sees.

# Step 3 — Add AKS IP to Azure SQL Firewall


Go to:

	Azure Portal

Then:

	SQL Server → Networking → Firewall Rules

Add:

	AKS outbound IP

Save.

----------------------
-- kubectl commands --
----------------------

# 1. Connect to AKS Cluster

az aks get-credentials --resource-group abindev-rg --name aks-practice-cluster
kubectl cluster-info

C:\Users\Abin Singh R\.kube

To switch back to minikube and aks cluster:
kubectl config use-context minikube
kubectl config use-context aks-practice-cluster

# 2. Create Azure Container Registry (ACR)

a. Create ACR

az acr create --resource-group abindev-rg --name akspracticeacr26abin  --sku Basic

# if gets error then as follows,
az provider register --namespace Microsoft.ContainerRegistry

# 3. Attach ACR to AKS

az aks update --resource-group abindev-rg --name aks-practice-cluster --attach-acr akspracticeacr26abin

# 4. Build Docker Image

a. Get ACR Login Server
az acr show --name akspracticeacr26abin --query loginServer --output tsv

b. login to ACR
az acr login --name akspracticeacr26abin
az acr login -n akspracticeacr26abin --expose-token

c. Build Image
docker build -t backend:v1 .

Delete image if required after use:
docker rmi backend:v1

# 5. Tag image
docker tag backend:v1 akspracticeacr26abin.azurecr.io/backend:v1


# 6. Push Image
# make sure you login before pushing
az acr login --name akspracticeacr26abin
docker push akspracticeacr26abin.azurecr.io/backend:v1

# 7. verify image exist in ACR
az acr repository list --name akspracticeacr26abin --output table

# 8. Deploy manifest files

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 9. To delete all pods and service

kubectl delete pods,services --all

# 10. Cleanup Resources
az group delete --name abindev-rg --yes --no-wait
az group list --output table

# 11. to delete secret

kubectl delete secret sql-secret

# 12. to rollout
kubectl rollout restart deployment backend-deployment

# 13. Delete pods and service

# to delete a pod
kubectl delete pod <pod-name>

# to delete all pod
kubectl delete pods --all

# to delete service
kubectl delete svc --all

# to delete all deployments
kubectl delete deployments --all

# to delete everything
kubectl delete all --all

# 14. logs

kubectl logs <pod-name>

# 15. get deployments, pods, svc
kubectl get deployments
kubectl get pods

-----------------------
----- az commands -----
-----------------------

# 1 .How to delete docker images in ACR?

# list repository
az acr repository list --name <ACR_NAME> --output table

# list tags
az acr repository show-tags --name <ACR_NAME> --repository <REPOSITORY_NAME> --output table

# delete options
az acr repository delete --name <ACR_NAME> --image <REPOSITORY>:<TAG> --yes

# Delete an entire repository
az acr repository delete --name <ACR_NAME> --repository <REPOSITORY_NAME> --yes

# Delete all untagged manifests (cleanup)
az acr run --registry <ACR_NAME> --cmd "acr purge --untagged" /dev/null

# verify deletion
az acr repository list --name <ACR_NAME> --output table

# check images
docker images

# Delete the tagged images
docker rmi akspracticeacr26abin.azurecr.io/backend:v1

# delete from acr
az acr repository delete --name akspracticeacr26abin --image backend:v1 --yes





