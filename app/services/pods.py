from app.k8s_client import get_core_v1_client


PROBLEM_REASONS = {
    "CrashLoopBackOff",
    "ImagePullBackOff",
    "ErrImagePull",
    "CreateContainerConfigError",
    "Pending",
}


def get_problem_pods():
    v1 = get_core_v1_client()
    pods = v1.list_pod_for_all_namespaces().items

    result = []

    for pod in pods:
        phase = pod.status.phase
        reason = None

        if pod.status.container_statuses:
            for container in pod.status.container_statuses:
                waiting = container.state.waiting
                if waiting:
                    reason = waiting.reason

        if phase == "Pending" or reason in PROBLEM_REASONS:
            result.append({
                "namespace": pod.metadata.namespace,
                "name": pod.metadata.name,
                "phase": phase,
                "reason": reason,
                "restart_count": sum(
                    c.restart_count for c in pod.status.container_statuses or []
                ),
            })

    return result