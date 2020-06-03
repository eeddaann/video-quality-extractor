import pandas as pd

#ffprobe_command = "signalstats='stat=tout+vrep+brng',deflicker=bypass=1,bitplanenoise"
ffprobe_command = "signalstats=stat=tout+vrep+brng,bitplanenoise,idet=half_life=1,deflicker=bypass=1,split[a][b];[a]field=top[a1];[b]field=bottom,split[b1][b2];[a1][b1]psnr[c1];[c1][b2]ssim"
drop_meta = "| cut -f30- -d ','"

def check_low_signal(report):
    return report['avg_Yhigh'] < 70

def check_high_signal(report):
    return report['avg_Ylow'] < 70

def check_interlace(report):
    return report['interlace_pct'] > 0.75

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
    #columns = ['ymin', 'ylow', 'yavg', 'yhigh', 'ymax', 'umin', 'ulow', 'uavg', 'uhigh', 'umax', 'vmin', 'vlow', 'vavg', 'vhigh', 'vmax', 'satmin', 'satlow', 'satavg', 'sathigh', 'satmax', 'huemed', 'hueavg', 'ydif', 'udif', 'vdif', 'ybitdepth', 'ubitdepth', 'vbitdepth', 'tout', 'vrep', 'brng', 'luminance', 'new_luminance', 'relative_change', 'bitplanenoise01', 'bitplanenoise11', 'bitplanenoise21']
    columns = ['ymin', 'ylow', 'yavg', 'yhigh', 'ymax', 'umin', 'ulow', 'uavg', 'uhigh', 'umax', 'vmin', 'vlow', 'vavg', 'vhigh', 'vmax', 'satmin', 'satlow', 'satavg', 'sathigh', 'satmax', 'huemed', 'hueavg', 'ydif', 'udif', 'vdif', 'ybitdepth', 'ubitdepth', 'vbitdepth', 'tout', 'vrep', 'brng', 'bitplanenoise01', 'bitplanenoise11', 'bitplanenoise21', 'idet_repeated_current_frame', 'idet_repeated_neither', 'idet_repeated_top', 'idet_repeated_bottom', 'idet_single_current_frame', 'idet_single_tff', 'idet_single_bff', 'idet_single_progressive', 'idet_single_undetermined', 'idet_multiple_current_frame', 'idet_multiple_tff', 'idet_multiple_bff', 'idet_multiple_progressive', 'idet_multiple_undetermined', 'luminance', 'new_luminance', 'relative_change', 'psnr_mse_y', 'psnr_psnr_y', 'psnr_mse_u', 'psnr_psnr_u', 'psnr_mse_v', 'psnr_psnr_v', 'psnr_mse_avg', 'psnr_psnr_avg', 'ssim_y', 'ssim_u', 'ssim_v', 'ssim_all', 'ssim_db']
    df = pd.read_csv(csv_path,names=columns)
    return {
        'avg_Yhigh': round(df.yhigh.mean(),4),
        'avg_Ylow': round(df.ylow.mean(),4),
        'yrang': round((df.yhigh-df.ylow).mean(),4),
        'urang': round((df.uhigh-df.ulow).mean(),4),
        'vrang': round((df.vhigh-df.vlow).mean(),4),
        'interlace_pct': round((df.idet_multiple_bff.sum() + df.idet_multiple_tff.sum())/(2*len(df)),4)
    }