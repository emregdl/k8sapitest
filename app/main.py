from fastapi import FastAPI

from app.services.nodes import get_nodes_health
from app.services.pods import get_problem_pods
from app.services.metrics import get_node_metrics, get_pod_metrics_by_node

from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title="K8s Health Dashboard",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "service": "K8s Health Dashboard",
        "status": "running"
    }


@app.get("/health/nodes")
def nodes_health():
    return {
        "nodes": get_nodes_health()
    }


@app.get("/health/pods/problems")
def pod_problems():
    return {
        "problem_pods": get_problem_pods()
    }


@app.get("/health/summary")
def health_summary():
    nodes = get_nodes_health()
    pods = get_problem_pods()

    not_ready_nodes = [n for n in nodes if not n["ready"]]

    return {
        "cluster_status": "critical" if not_ready_nodes or pods else "healthy",
        "node_count": len(nodes),
        "not_ready_node_count": len(not_ready_nodes),
        "problem_pod_count": len(pods),
        "not_ready_nodes": not_ready_nodes,
        "problem_pods": pods,
    }

@app.get("/metrics/nodes")
def node_metrics():
    return {
        "nodes": get_node_metrics()
    }


@app.get("/metrics/pods-by-node")
def pod_metrics_by_node():
    return {
        "pods": get_pod_metrics_by_node()
    }

@app.get("/dashboard")
def dashboard(request: Request):
    node_metrics = get_node_metrics()
    pod_metrics = get_pod_metrics_by_node()

    return templates.TemplateResponse(
    request=request,
    name="dashboard.html",
    context={
        "node_metrics": node_metrics,
        "pod_metrics": pod_metrics
    }
)