import sys
import csv
import requests
import subprocess


def get_site_id_dict():
    url = "https://www.nhk.or.jp/radioondemand/json/index_v3/index.json"
    site_id_dict = {}
    with requests.get(url) as response:
        data_list = response.json()["data_list"]
        for program in data_list:
            site_id_dict[program["program_name"]] = program["site_id"]
        return site_id_dict

def get_m3u8(site_id):
    url = f"https://www.nhk.or.jp/radioondemand/json/{site_id}/bangumi_{site_id}_01.json"
    file_name_list = []
    date_list = []
    with requests.get(url) as response:
        main = response.json()["main"]
        program_name = main["program_name"].replace(" ","_")
        detail_list = main["detail_list"]
        for detail in detail_list:
            file_list = detail["file_list"]
            for file in  file_list:
                date_list.append(file["open_time"].split("+")[0])
                file_name_list.append(file["file_name"].split("?")[0])
    file_name_list.reverse()
    date_list.reverse()
    return file_name_list, date_list, program_name


def call_ffmpeg(m3u8, program_name, date):
# ffmpeg < 4.3
#    cmd = ["ffmpeg", "-v", "quiet", "-i", m3u8, "-c", "copy", f"{program_name}-{date}.m4a"]
    cmd = ["ffmpeg", "-http_seekable", "0", "-v", "quiet", "-i", m3u8, "-c", "copy", f"{program_name}-{date}.m4a"]
    print(" ".join(cmd))
    status = subprocess.run(cmd)
#   print(f"return code: {status.returncode}")
#   print(f"stdout: {status.stdout}")
#   print(f"stderr: {status.stdout}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        site_id_dict = get_site_id_dict()
        for k, v in site_id_dict.items():
            print(f"{v},{k}")
    else:
        for i in range(1, len(sys.argv)):
            fname = sys.argv[i]
            print(f"processing {fname}")
            site_id_list = []
            with open(fname) as csvfile:
                for row in csv.reader(csvfile):
                    site_id_list.append(row[0])
            print(site_id_list)
            for site_id in site_id_list:
                file_name_list, date_list, program_name = get_m3u8(site_id)
                for f, d in zip(file_name_list, date_list):
                    call_ffmpeg(f, program_name, d)

