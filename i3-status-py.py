import subprocess
import time
import os

def get_date():
    date = subprocess.check_output('date +"%d/%m/%Y | %H:%M"', shell=True)
    date = str(date).replace("b'","")
    date = str(date).replace("\\n'","")
    return(date)
def get_ip():
    interface = str(subprocess.check_output('ip link | grep "state UP"', shell=True))
    if interface == "":
        ip_str = "no connection"
    else:
        interface_split = interface.split(":")
        interface = interface_split[1]
        interface = interface.replace(" ","")
        ip = str(subprocess.check_output(f"ip -br addr show | grep {interface}", shell=True))
        ip_split = ip.split("UP")
        ip = ip_split[1]
        ip = ip.replace(" ","")
        ip_split = ip.split("/")
        ip = ip_split[0]
        ip_str = str(f"{interface}: {ip}")
    return(ip_str)
def get_volume():
    volume = str(subprocess.check_output("amixer -D pulse sget Master | grep %", shell=True))
    if "[on]" in volume:
        mute = "[on]"
    else:
        mute = "[off]"
    volume_split = volume.split("[")
    volume = volume_split[1]
#    volume = volume.replace("]","",1)
    return("["+volume+mute)
def get_volume_mic():
    volume = str(subprocess.check_output("amixer -D pulse sget Capture | grep %", shell=True))
    if "[on]" in volume:
        mute = "[on]"
    else:
        mute = "[off]"
    return(mute)
def get_music():
    try:
        music = str(subprocess.check_output("playerctl -a metadata", shell=True))
        music_split = music.split(" ")
#        if len(music_split) == 3:
        try:
            music_split = music.split("\\n")
            artist = music_split[1]
            artist_split = artist.split("artist")
            artist = artist_split[1]
            title = music_split[2]
            title_split = title.split("title")
            title = title_split[1]
            artist = artist.lstrip()
            title = title.lstrip()
#        else:
        except:
            music_split = music.split("\\n")
            artist = music_split[0]
            artist_split = artist.split("artist")
            artist = artist_split[1]
            title = music_split[1]
            title_split = title.split("title")
            title = title_split[1]
            artist = artist.lstrip()
            title = title.lstrip()
        status = str(subprocess.check_output("playerctl status", shell=True))
        title = title.strip()
        artist = artist.strip()
        if (len(title)+len(artist))> 90:
            title = title[:30]+"..."
        if (len(artist)+len(title)) > 60:
            if len(artist) > 15:
                artist = artist[:15]+"..."
            if len(title) > 25:
                title = title[:25]+"..."
        if "Playing" in status:
            if artist != "":
                playing_str = str(f" {artist} :: {title}")
            else:
                playing_str = str(f" {title}")
        else:
            if artist != "":
                playing_str = str(f" {artist} :: {title}")
            else:
                playing_str = str(f" {title}")
    except:
        playing_str = ("")
    return(playing_str)

while True:
    status_ip = get_ip()
    status_date = get_date()
    status_volume = get_volume()
    status_mic = get_volume_mic()
    status_music = get_music()
    if len(status_music) > 30:
        status = str(f"{status_music} |  {status_volume}  {status_mic} |  {status_date}")
    else:
        status = str(f" {status_music} |  {status_ip} |  {status_volume}  {status_mic} |  {status_date}")


#    print(status)
    if '"' in status:
        status = status.replace('"',"'")
    os.system(f'xsetroot -name "                                                                                            {status}"')
    time.sleep(1)
