from kubernetes import client, config

KUBECONFIG_PATH = r"C:\Users\omer.gudul\Desktop\k8stest.kubeconfig"
config.load_kube_config(config_file=KUBECONFIG_PATH)

core_v1 = client.CoreV1Api()
custom_api = client.CustomObjectsApi()

def get_core_v1_client():
    return core_v1


def get_custom_objects_client():
    return custom_api