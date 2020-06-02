import pandas as pd

ffprobe_command = "signalstats='stat=tout+vrep+brng',deflicker=bypass=1,bitplanenoise"
drop_meta = "| cut -f30- -d ','"

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
    columns = ['ymin', 'ylow', 'yavg', 'yhigh', 'ymax', 'umin', 'ulow', 'uavg', 'uhigh', 'umax', 'vmin', 'vlow', 'vavg', 'vhigh', 'vmax', 'satmin', 'satlow', 'satavg', 'sathigh', 'satmax', 'huemed', 'hueavg', 'ydif', 'udif', 'vdif', 'ybitdepth', 'ubitdepth', 'vbitdepth', 'tout', 'vrep', 'brng', 'luminance', 'new_luminance', 'relative_change', 'bitplanenoise01', 'bitplanenoise11', 'bitplanenoise21']
    df = pd.read_csv(csv_path,names=columns)
    print(df.head())
    return {
        'avg_Yhigh': 60,
        'avg_Ylow': 60
    }