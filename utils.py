
def calculate_change(before, after):
    if before == 0:
        return None
    return ((before - after) / before) * 100



def compare_execution_plans(plans):
    """Compare execution plans using elapsed time and workload metrics."""
    if not plans:
        return None

    best_plan = min(
        plans,
        key=lambda plan: plan["elapsed_seconds"]
    )

    worst_plan = max(
        plans,
        key=lambda plan: plan["elapsed_seconds"]
    )

    fastest_time = best_plan["elapsed_seconds"]
    slowest_time = worst_plan["elapsed_seconds"]

    if slowest_time <= 0:
        improvement_percent = 0.0
    else:
        improvement_percent = (
            (slowest_time - fastest_time) / slowest_time
        ) * 100

    return {
        "best_plan_hash": best_plan["plan_hash_value"],
        "worst_plan_hash": worst_plan["plan_hash_value"],
        "fastest_time": fastest_time,
        "slowest_time": slowest_time,
        "improvement_percent": improvement_percent,
        "best_cpu_seconds": best_plan.get("cpu_seconds"),
        "best_buffer_gets": best_plan.get("buffer_gets"),
        "best_disk_reads": best_plan.get("disk_reads"),
        "best_executions": best_plan.get("executions"),
    }
