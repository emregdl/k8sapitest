from app.k8s_client import get_custom_objects_client, get_core_v1_client


def parse_cpu(cpu):
    if cpu.endswith("n"):
        return int(cpu[:-1]) / 1_000_000
    if cpu.endswith("u"):
        return int(cpu[:-1]) / 1000
    if cpu.endswith("m"):
        return int(cpu[:-1])
    return int(cpu) * 1000


def parse_memory(memory):
    if memory.endswith("Ki"):
        return int(memory[:-2]) / 1024
    if memory.endswith("Mi"):
        return int(memory[:-2])
    if memory.endswith("Gi"):
        return int(memory[:-2]) * 1024
    return int(memory) / 1024 / 1024


def get_node_metrics():
    api = get_custom_objects_client()

    metrics = api.list_cluster_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        plural="nodes"
    )

    result = []

    for item in metrics["items"]:
        cpu_millicores = parse_cpu(item["usage"]["cpu"])
        memory_mib = parse_memory(item["usage"]["memory"])

        result.append({
            "node": item["metadata"]["name"],
            "cpu_millicores": round(cpu_millicores, 2),
            "memory_mib": round(memory_mib, 2),
        })

    return result


def get_pod_metrics_by_node():
    metrics_api = get_custom_objects_client()
    core_api = get_core_v1_client()

    pod_metrics = metrics_api.list_cluster_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        plural="pods"
    )

    pods = core_api.list_pod_for_all_namespaces().items

    pod_node_map = {
        f"{pod.metadata.namespace}/{pod.metadata.name}": pod.spec.node_name
        for pod in pods
    }

    result = []

    for item in pod_metrics["items"]:
        namespace = item["metadata"]["namespace"]
        pod_name = item["metadata"]["name"]
        key = f"{namespace}/{pod_name}"

        total_cpu = 0
        total_memory = 0

        for container in item["containers"]:
            total_cpu += parse_cpu(container["usage"]["cpu"])
            total_memory += parse_memory(container["usage"]["memory"])

        result.append({
            "node": pod_node_map.get(key),
            "namespace": namespace,
            "pod": pod_name,
            "cpu_millicores": round(total_cpu, 2),
            "memory_mib": round(total_memory, 2),
        })

    return result