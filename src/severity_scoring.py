def calculate_severity_counts(results):
    """
    Count validation findings by severity.
    """

    counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
        "none": 0
    }

    for result in results:

        severity = result.get(
            "severity",
            "none"
        )

        if severity in counts:
            counts[severity] += 1

    return counts


def calculate_status_counts(results):
    """
    Count passed, failed and warning results.
    """

    counts = {
        "passed": 0,
        "failed": 0,
        "warning": 0,
        "anomaly": 0
    }

    for result in results:

        status = result.get(
            "status",
            ""
        )

        if status in counts:
            counts[status] += 1

    return counts


def calculate_health_score(results):
    """
    Calculate an overall dataset health score.

    Starting score = 100

    High severity    = -5
    Medium severity  = -3
    Low severity     = -1

    Score is limited between 0 and 100.
    """

    score = 100

    severity_penalties = {
        "high": 5,
        "medium": 3,
        "low": 1,
        "none": 0
    }

    for result in results:

        severity = result.get(
            "severity",
            "none"
        )

        penalty = severity_penalties.get(
            severity,
            0
        )

        score -= penalty

    score = max(
        0,
        min(100, score)
    )

    return round(
        score,
        2
    )


def get_health_status(score):
    """
    Convert numerical health score
    into a descriptive status.
    """

    if score >= 90:
        return "healthy"

    elif score >= 75:
        return "mostly_healthy"

    elif score >= 50:
        return "needs_attention"

    else:
        return "poor"


def generate_severity_report(results):
    """
    Generate complete severity and
    dataset health information.
    """

    severity_counts = (
        calculate_severity_counts(
            results
        )
    )

    status_counts = (
        calculate_status_counts(
            results
        )
    )

    health_score = (
        calculate_health_score(
            results
        )
    )

    health_status = get_health_status(
        health_score
    )

    return {
        "total_findings": len(results),
        "severity_counts": severity_counts,
        "status_counts": status_counts,
        "health_score": health_score,
        "health_status": health_status
    }