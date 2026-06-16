from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


def load_kubernetes_config():
    try:
        config.load_incluster_config()
    except ConfigException:
        config.load_kube_config()


def get_core_v1_client():
    load_kubernetes_config()
    return client.CoreV1Api()


def get_apps_v1_client():
    load_kubernetes_config()
    return client.AppsV1Api()


def get_custom_objects_client():
    load_kubernetes_config()
    return client.CustomObjectsApi()