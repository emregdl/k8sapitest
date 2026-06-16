from app.k8s_client import get_core_v1_client


def get_nodes_health():
    v1 = get_core_v1_client()
    nodes = v1.list_node().items

    result = []

    for node in nodes:
        conditions = {
            condition.type: condition.status
            for condition in node.status.conditions
        }

        result.append({
            "name": node.metadata.name,
            "ready": conditions.get("Ready") == "True",
            "memory_pressure": conditions.get("MemoryPressure") == "True",
            "disk_pressure": conditions.get("DiskPressure") == "True",
            "pid_pressure": conditions.get("PIDPressure") == "True",
        })

    return result