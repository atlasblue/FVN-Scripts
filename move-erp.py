import ntnx_networking_py_client

# Configure the client
config = ntnx_networking_py_client.Configuration()
# IPv4/IPv6 address or FQDN of Prism Central
config.host = ""
# Port to which to connect to
config.port = 9440
# Max retry attempts while reconnecting on a loss of connection
config.max_retry_attempts = 3
# Backoff factor to use during retry attempts
config.backoff_factor = 3
# UserName to connect to the cluster
config.username = "admin"
# Password to connect to the cluster
config.password = ""
#disable ssl certificate check
config.verify_ssl = False

# Create VPC Object and update with existing values w/o ERP
client = ntnx_networking_py_client.ApiClient(configuration=config)
vpcs_api = ntnx_networking_py_client.VpcsApi(api_client=client)
vpc_pri = ntnx_networking_py_client.Vpc()
vpc_dr = ntnx_networking_py_client.Vpc()
ext_id_pri = "3bc5985d-7087-4538-ac4f-120a3f29242c" # VPC Primary UUID
ext_id_dr = "e0e444dd-a5e9-4d60-93b4-214a8b1f95bb" # VPC DR UUID
api_reponse_pri = vpcs_api.get_vpc_by_id(extId=ext_id_pri)
api_reponse_dr = vpcs_api.get_vpc_by_id(extId=ext_id_dr)


# Remove ERPs VPC-Primary If ERP with value
if api_reponse_pri.data.externally_routable_prefixes is not None:
    try:  
        etag_value_pri = ntnx_networking_py_client.ApiClient.get_etag(api_reponse_pri)
        vpc_pri.name = api_reponse_pri.data.name
        vpc_pri.external_subnets = api_reponse_pri.data.external_subnets
        erp = api_reponse_pri.data.externally_routable_prefixes
        api_res = vpcs_api.update_vpc_by_id(extId=ext_id_pri, body=vpc_pri, if_match=etag_value_pri)
        
        etag_value_dr = ntnx_networking_py_client.ApiClient.get_etag(api_reponse_dr)
        vpc_dr.name = api_reponse_dr.data.name
        vpc_dr.external_subnets = api_reponse_dr.data.external_subnets
        vpc_dr.externally_routable_prefixes = erp
        api_res = vpcs_api.update_vpc_by_id(extId=ext_id_dr, body=vpc_dr, if_match=etag_value_dr)
    except ntnx_networking_py_client.rest.ApiException as e:
        print(e)

elif api_reponse_dr.data.externally_routable_prefixes is not None:
    try:  
        etag_value_dr = ntnx_networking_py_client.ApiClient.get_etag(api_reponse_dr)
        vpc_dr.name = api_reponse_dr.data.name
        vpc_dr.external_subnets = api_reponse_dr.data.external_subnets
        erp = api_reponse_dr.data.externally_routable_prefixes
        api_res = vpcs_api.update_vpc_by_id(extId=ext_id_dr, body=vpc_dr, if_match=etag_value_dr)
        
        etag_value_pri = ntnx_networking_py_client.ApiClient.get_etag(api_reponse_pri)
        vpc_pri.name = api_reponse_pri.data.name
        vpc_pri.external_subnets = api_reponse_pri.data.external_subnets
        vpc_pri.externally_routable_prefixes = erp
        api_res = vpcs_api.update_vpc_by_id(extId=ext_id_pri, body=vpc_pri, if_match=etag_value_pri)
    except ntnx_networking_py_client.rest.ApiException as e:
        print(e)





