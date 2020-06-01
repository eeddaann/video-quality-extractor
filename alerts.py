def check_low_signal(report):
    return report['avg_Yhigh'] < 70

def check_high_signal(report):
    return report['avg_Ylow'] < 70

ALERTS = [
    {
        "rule": check_low_signal,
        "alert_code": "low_signal",
        "relevant_metric": "avg_Yhigh"
    },
    {
        "rule": check_high_signal,
        "alert_code": "high_signal",
        "relevant_metric": "avg_Ylow"
    },
]

def extract_metrics(csv_path):
    return {
        'avg_Yhigh': 60,
        'avg_Ylow': 60
    }