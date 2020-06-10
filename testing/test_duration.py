
from datetime import datetime
import subprocess
VIDEO = "tv_color_bars_test.mp4"
INTERVALS = [
    "00:10",
    "00:20",
    "00:30",
    "00:40",
    "00:50",
    "01:00",
    "02:00",
    "03:00",
]
FFPROBE_CMDS = {
    "only signalstats": "signalstats='stat=tout+vrep+brng'",
    "signalstats+interlacing":"signalstats=stat=tout+vrep+brng,bitplanenoise,idet=half_life=1,deflicker=bypass=1,split[a][b];[a]field=top[a1];[b]field=bottom,split[b1][b2];[a1][b1]psnr[c1];[c1][b2]ssim"
}
def interval2sec(interval):
    mmss = interval.split(':')
    return int(mmss[0])*60 + int(mmss[1])
dicts = {}
for ffcmd in FFPROBE_CMDS:
    dicts[ffcmd] = []
    print(ffcmd)
    for interval in INTERVALS:
        cmd = ["/bin/sh", "-c", '''ffprobe -f lavfi -i "movie=%s,%s" -read_intervals %%%s -show_frames -hide_banner -print_format csv | cut -f30- -d ',' '''%(VIDEO,FFPROBE_CMDS[ffcmd],interval)]
        ffprobe_start_time = datetime.now()
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # run ffprobe
        stdout, stderr = p.communicate()
        p.wait()
        dicts[ffcmd].append((datetime.now() - ffprobe_start_time).total_seconds())
        print("%s : %s sec"%(interval,dicts[ffcmd][-1]))

print("results = %s"%(dicts)) 
print("x = %s"%(list(map(interval2sec,INTERVALS))))                                                                                                              

''' 
# plotting the results
import matplotlib.pyplot as plt
results = {'only signalstats': [2.818146, 4.165485, 0.024359, 11.400025, 12.53656, 21.766588, 32.240704], 'signalstats+interlacing': [2.840394, 5.538977, 0.018016, 13.849626, 16.42738, 35.493639, 50.167398]}
x = [10, 20, 30, 50, 60, 120, 180]
for k in results:
    plt.plot(x,results[k],'.-',label=k)
plt.title("processing duration vs video length")
plt.xlabel("video length [seconds]")
plt.ylabel("processing duration [seconds]")
plt.legend(loc="upper left")
plt.show()
'''