import argparse
import os
import subprocess
from datetime import datetime
from configparser import ConfigParser
import linecache
import sys
import random
import alerts

save_csv = False
start_time = datetime.now()
operational_log = {
    "log_type": "report"
}

def send_log(log,output_url="stdout"):
    for name, value in config.items('metadata'): # include metadata anyway
        log[name] = value
    if output_url == "stdout":
        print(log)
    else:
        pass

def generate_report(csv_path):
    report = alerts.extract_metrics(csv_path)
    report['report_id'] = str(hex(hash(random.random())))
    generate_alerts(report)
    return report

def generate_alerts(report):
    for alert_type in alerts.ALERTS:
        if alert_type['rule'](report):
            alert = {
                "log_type": "alert",
                "relevant_report": report['report_id'],
                "alert_code": alert_type['alert_code'],
                "relevant_metric": alert_type['relevant_metric'],
                "metric_value": report[alert_type['relevant_metric']]
            }
            send_log(alert)

parser = argparse.ArgumentParser(description='Analyzes video quality and sends results in JSON format.')
parser.add_argument('v_path',
                       metavar='video-path',
                       type=str,
                       help='the path to video')
parser.add_argument('config_path',
                       metavar='config_path',
                       nargs='?',
                       default='config.ini',
                       help='the url for the server which will store the results, "stdout" for writing to stdout')
# read args
args = parser.parse_args()
video_path = args.v_path
config_path = args.config_path

try:
    ffprobe_output = video_path + '.csv'
    config = ConfigParser()
    config.read(config_path) # read configuration
    output_url = config['paths']['output_url'] # set url for sending logs 
    save_csv = config['debugging'].getboolean('save_csv') # should we need to save the csv
    operational_log["video_size_bytes"] = os.path.getsize(video_path) # log video size
    cmd = ["/bin/sh", "-c", "ffprobe -f lavfi movie=%s,%s %s -show_frames -hide_banner -print_format csv > %s"%(video_path,
                                                                                                                config['ffprobe']['ffprobe_command'],
                                                                                                                config['ffprobe']['interval'],
                                                                                                                ffprobe_output)]
    ffprobe_start_time = datetime.now() # log start time of ffprobe
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # run ffprobe
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        if str(stderr) == "b''":
            # ffprobe sends it's errors to stdout
            operational_log["ffprobe_error"] = str(stdout)
        else:
            # if ffprobe not installed or os related error...
            operational_log["ffprobe_error"] = str(stderr)
        operational_log["ffprobe_cmd"] = cmd[2] # log the command which caused the error
        raise Exception
    p.wait() # wait for ffprobe 
    operational_log["ffprobe_duration"] = (datetime.now() - ffprobe_start_time).total_seconds()
    # TODO: calc ffprobe output size
    metrics_start_time = datetime.now()
    operational_log.update(generate_report(ffprobe_output)) # add metrics to log
    operational_log["metrics_extraction_duration"] = (datetime.now() - metrics_start_time).total_seconds()
    operational_log["status"] = "success"
except Exception as e:
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno # get line number of exception
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals) # get the line which caused the exception
    operational_log["error_line_number"] = tb.tb_lineno
    operational_log["error_line"] = line.strip()
    operational_log["status"] = "failed"
    operational_log["error"] = str(e)
finally:
    if os.path.exists(ffprobe_output): # delete ffprobe output
        if not save_csv:
            os.remove(ffprobe_output)
    operational_log["total_duration"] = (datetime.now() - start_time).total_seconds()
    send_log(operational_log,output_url)