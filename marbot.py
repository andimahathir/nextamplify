
import traceback
import requests
import time
import openai
#from asyncio.windows_events import NULL
# from msilib.schema import File
import os
import json
import mysql.connector
from bs4 import BeautifulSoup
from threading import Thread
import datetime
from datetime import date, datetime, timedelta
from random import seed, randint, choice
from speedtest import Speedtest
import sys
from EdgeGPT import Chatbot, ConversationStyle
import asyncio


version = "1.5"
update_id = ""
ipversion = 4
botToken = '767662956:AAEWpGMqRyu27ISRAG8mr-BapYzrIig8fg8'
url = 'https://api.telegram.org/bot'+botToken+'/'
phoenix = True
counter = 0
statusabsen = False
jamabsen = ""
menitabsen = ""
boschatid = 267093573
statusgrouppvu = False
testpvuscan = False
pvubot = False
dumpupdate = False
oldelementsdeera = ''
oldelementsindra = ''
autodeera = False
autoindra = False
deeradump = False
resiresult = None
direkturpulang = "-"
direkturchecker = False
killbot = False
cekresionprogress = False
marbotGPT = {}
bingGPT = {}

superAdmin = ["andimahathir", "jangandonk99"]
userJember = ["siapasaya90", "ekodownloader", "yatnosyarifudin"]
userGold = ["selaxass"]
userAbsen = ["satyapragolapati", "Shkmhs", "Deeyan127", "salchum"]

commandAdmin = ["chatid", "private", "petani", "libur", "hapusabsen", "pvu", "download", "dumpupdate", "perdin", "cekabsen", "turtle", "ceklimit", "adios", "direkturcheck", "absenmasuk", "absenpulang"]
commandJember = ["nik", "name", "name2", "name3", "date", "add", "nokk", "niknokk", "nikadd", "nameadd", "resi", "putu", "eko", "lord", "jember", "hapusresi", "restart", "generatealamat", "kemendagri", "/speedtest", "/kill", "/restart", "/testdatabase", "chatgpt", "cp", "gpt", "bing", "bp"]
commandGold = ["Gold", "gold"]
commandAbsen = ["absen", "wfh", "resi", "hapusresi", "kemendagri"]

helpTextJember = "nik <nomor nik>\nname <nama target>\nname2 <2 kata nama acak>\nname3 <3 kata nama acak>\ndate <tanggal lahir dd-mm-yyyy>\nadd <alamat>\nnokk <nomor kk>\nniknokk <nomor nik>\nnikadd <nomor nik>\nnameadd <nama>;<alamat/kelurahan/kecamatan>\nkemendagri <nama atau nip>\nresi <resi> <item>\nresi update\nhapusresi <resi>\ndumpupdate\n/restart ya buat restart bot\n/kill buat stop spam chat karena kegoblokanmu sendiri\nList all possible command : \n" + str(commandJember)
helpTextAdmin = helpTextJember + "\n" + str(commandAdmin)


def autoabsen():
    try:
        waktu = datetime.now()
        hari = waktu.strftime("%A")
        tanggal = waktu.strftime("%Y%m%d")
        tanggaldoang = waktu.strftime("%d")
        bulandoang = waktu.strftime("%m")
        tahundoang = waktu.strftime("%Y")
        jam = waktu.strftime("%H")
        menit = waktu.strftime("%M")
        # tanggalkemarin = waktu - timedelta(1)
        # tanggalkemarin = tanggalkemarin.strftime("%Y%m%d")

        if hari != "Sunday" and hari != "Saturday":
            filejson = open("listabsen.json",)
            listabsen = json.load(filejson)
            filejson.close()
            if tanggal not in listabsen:
                if hari != "Friday":
                    listabsen[tanggal] = {
                        "pagi": {
                            "menit": randint(0, 57),
                            "status": "done"
                        },
                        "sore": {
                            "menit": randint(0, 57),
                            "status": "notyet"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                else:
                    listabsen[tanggal] = {
                        "pagi": {
                            "menit": randint(0, 30),
                            "status": "done"
                        },
                        "sore": {
                            "menit": randint(31, 57),
                            "status": "notyet"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
            for i in listabsen.copy():
                if int(i) < int(tanggal):
                    listabsen.pop(i, None)
                # listabsen.pop(tanggalkemarin, None)
            if listabsen[tanggal]["pagi"]["status"] == "notyet" or listabsen[tanggal]["pagi"]["status"] == "wfh":
                if (int(jam) == 8 and int(menit) >= int(listabsen[tanggal]["pagi"]["menit"])) or (int(jam) > 8):
                    sendchat(boschatid, "initiate autoabsen...")
                    if listabsen[tanggal]["pagi"]["status"] == "wfh":
                        wfhmode = True
                    else:
                        wfhmode = False
                    listabsen[tanggal]["pagi"]["status"] = "processing"
                    with open('listabsen.json', 'w') as outfile:
                        json.dump(listabsen, outfile, indent=4)
                    if wfhmode:
                        result = wfh()
                    else:
                        result = absen()
                    try:
                        result = json.loads(result)
                        if result["status"] == "1":
                            listabsen[tanggal]["pagi"]["status"] = "done"
                        else:
                            if wfhmode:
                                listabsen[tanggal]["pagi"]["status"] = "wfh"
                            else:
                                listabsen[tanggal]["pagi"]["status"] = "notyet"
                    except:
                        if wfhmode:
                            listabsen[tanggal]["pagi"]["status"] = "wfh"
                        else:
                            listabsen[tanggal]["pagi"]["status"] = "notyet"
                        sendchat(boschatid, "problem with simpeg")
                    sendchat(boschatid, listabsen)
            if listabsen[tanggal]["sore"]["status"] == "notyet" or listabsen[tanggal]["sore"]["status"] == "wfh":
                if (int(jam) == 17 and int(menit) >= int(listabsen[tanggal]["sore"]["menit"])) or (int(jam) > 17):
                    sendchat(boschatid, "initiate autoabsen...")
                    if listabsen[tanggal]["sore"]["status"] == "wfh":
                        wfhmode = True
                    else:
                        wfhmode = False
                    listabsen[tanggal]["sore"]["status"] = "processing"
                    with open('listabsen.json', 'w') as outfile:
                        json.dump(listabsen, outfile, indent=4)
                    if wfhmode:
                        result = wfh()
                    else:
                        result = absen()
                    try:
                        result = json.loads(result)
                        if result["status"] == "1":
                            listabsen[tanggal]["sore"]["status"] = "done"
                        else:
                            if wfhmode:
                                listabsen[tanggal]["sore"]["status"] = "wfh"
                            else:
                                listabsen[tanggal]["sore"]["status"] = "notyet"
                    except:
                        if wfhmode:
                            listabsen[tanggal]["sore"]["status"] = "wfh"
                        else:
                            listabsen[tanggal]["sore"]["status"] = "notyet"
                        sendchat(boschatid, "problem with simpeg")
                    sendchat(boschatid, listabsen)
            if listabsen[tanggal]["sikerja"]["status"] == "notyet":
                if (int(jam) >= 16):
                    sendchat(boschatid, "initiate autosikerja...")
                    listabsen[tanggal]["sikerja"]["status"] = "processing"
                    with open('listabsen.json', 'w') as outfile:
                        json.dump(listabsen, outfile, indent=4)
                    result = sikerja(tanggaldoang, bulandoang, tahundoang)
                    try:
                        result = json.loads(result)
                        if result["status"] == 1:
                            listabsen[tanggal]["sikerja"]["status"] = "done"
                        else:
                            listabsen[tanggal]["sikerja"]["status"] = "notyet"
                    except:
                        listabsen[tanggal]["sikerja"]["status"] = "notyet"
                        sendchat(boschatid, "problem with sikerja")
                    # listabsen[tanggal]["sore"]["status"] = "done"
                    sendchat(boschatid, listabsen)
            with open('listabsen.json', 'w') as outfile:
                json.dump(listabsen, outfile, indent=4)
    except Exception as e:
        sendchat(boschatid, "Error autoabsen()\n" + getattr(e, 'message', repr(e)))
        # debug()


def sikerja(day, month, year):
    try:
        user = "199207292020121010"
        password = "jangandonk"
        payload = {'nip': user, 'password': password}
        r = requests.post("http://sikerja.kemendagri.go.id/auth/login", data=payload, timeout=60, verify=False)
        cookie = r.headers["Set-Cookie"]
        keterangan = "-"
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://sikerja.kemendagri.go.id',
                'Referer': 'http://sikerja.kemendagri.go.id/transaksi/home2/add',
                'Cookie': cookie}
        date = day + "-" + month + "-" + year
        if int(day) % 2 == 0:
            urtug = "303554"
        else:
            urtug = "303711"

        payload = {
            'data_sender[urtug]': urtug,
            'data_sender[flag_urtug]': '',
            'data_sender[tgl_mulai_raw]': date,
            'data_sender[tgl_selesai_raw]': date,
            'data_sender[jam_mulai]': '08:00',
            'data_sender[jam_selesai]': '16:00',
            'data_sender[ket_pekerjaan]': keterangan,
            'data_sender[kuantitas]': '0',
            'data_sender[file_pendukung]': ''
        }
        r = requests.post("http://sikerja.kemendagri.go.id/transaksi/add_pekerjaan_without_file/", data=payload, headers=header, timeout=60, verify=False)
        # print("----Date 1----")
        sendchat(boschatid, r.headers)
        sendchat(boschatid, r.text)
        return r.text
        # r = requests.post("http://sikerja.kemendagri.go.id/transaksi/add_pekerjaan_without_file/", data=payload2, headers=header)
        # print("----Date 2----")
        # print(r.headers)
        # print(r.text)
    except Exception as e:
        sendchat(boschatid, traceback.format_exc())
        # sendchat(boschatid, "Error sikerja()\n" + getattr(e, 'message', repr(e)))
        # debug()


def restartrouter():
    try:
        r = requests.post("https://192.168.1.1/", verify=False)
        # print(r.status_code)
        result = r.text
        loginchecktoken = result.split(
            'createHiddenInput("Frm_Loginchecktoken", "')[1].split('");')[0]
        logintoken = result.split(
            'createHiddenInput("Frm_Logintoken", "')[1].split('"),')[0]
        # print(loginchecktoken)
        # print(logintoken)
        headers = {
            'Cookie': '_TESTCOOKIESUPPORT=1',
            'Host': '192.168.1.1',
            'Origin': 'https://192.168.1.1',
            'Referer': 'https://192.168.1.1/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        payload = {
            'action': 'login',
            'Username': 'user',
            'Password': '917ccc0e983a28537586ba4f26726f2fd69df735fe7f9df1c4419ee9cbc7db3b',
            'Frm_Logintoken': logintoken,
            'UserRandomNum': 66541935,
            'Frm_Loginchecktoken': loginchecktoken
        }
        r = requests.post("https://192.168.1.1/", data=payload,
                        headers=headers, verify=False, allow_redirects=False)
        # print(r.status_code)
        # print(r.headers)
        cookie = r.headers["Set-Cookie"].split(';')[0]

        headers = {
            'Cookie': '_TESTCOOKIESUPPORT=1; ' + cookie,
            'Host': '192.168.1.1',
            'Origin': 'https://192.168.1.1',
            'Referer': 'https://192.168.1.1/',
            'Upgrade-Insecure-Requests': '1',
        }

        r = requests.get(
            "https://192.168.1.1/getpage.gch?pid=1002&nextpage=manager_dev_conf_t.gch", headers=headers, verify=False)
        result = r.text
        session_token = result.split('var session_token = "')[1].split('";')[0]
        # print(session_token)

        headers = {
            'Cookie': '_TESTCOOKIESUPPORT=1; ' + cookie,
            'Host': '192.168.1.1',
            'Origin': 'https://192.168.1.1',
            'Referer': 'https://192.168.1.1/',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {
            'IF_ACTION': 'devrestart',
            'IF_ERRORSTR': 'SUCC',
            'IF_ERRORPARAM': 'SUCC',
            'IF_ERRORTYPE': '-1',
            'flag': '1',
            '_SESSION_TOKEN': session_token
        }

        r = requests.post(
            "https://192.168.1.1/getpage.gch?pid=1002&nextpage=manager_dev_conf_t.gch", headers=headers, data=payload, verify=False)
    except Exception as e:
        sendchat(boschatid, "Error restartrouter()\n" + getattr(e, 'message', repr(e)))


def logger(message):
    a = 1
    # timestamp = datetime.datetime.now()
    # konten = str(timestamp)+" : "+str(message)
    # f = open("log marbot.txt", "a")
    # f.write(konten + "\n")
    # f.close()



def updateresi(chat_id = 0):
    try:
        global resiresult, cekresionprogress
        
        filejson = open("listresi.json",)
        listresi = json.load(filejson)
        filejson.close()
        if datetime.timestamp(datetime.now()) - 1200 > listresi["lastchecked"] and cekresionprogress:
            cekresionprogress = False
        
        if not cekresionprogress:
            cekresionprogress = True
            # filejson = open("listresi.json",)
            # listresi = json.load(filejson)
            # filejson.close()
            if datetime.timestamp(datetime.now()) - 600 > listresi["lastchecked"] or chat_id != 0:
                for i in listresi["data"][:]:
                    resiresult = None
                    if i["kurir"] == "SiCepat":
                        resisicepat(i["resi"])
                    elif i["kurir"] == "J&T":
                        resijnt(i["resi"])
                    elif i["kurir"] == "AnterAja":
                        resianteraja(i["resi"])
                    elif i["kurir"] == "Tokopedia":
                        resitokopedia(i["resi"])
                    elif i["kurir"] == "JNE":
                        resijne(i["resi"])
                    else:
                        kurir = []
                        kurir.append(Thread(target=resitokopedia, args=(i["resi"],)))
                        kurir.append(Thread(target=resisicepat, args=(i["resi"],)))
                        kurir.append(Thread(target=resijnt, args=(i["resi"],)))
                        kurir.append(Thread(target=resianteraja, args=(i["resi"],)))
                        kurir.append(Thread(target=resijne, args=(i["resi"],)))
                        for thread in kurir:
                            thread.start()
                        for thread in kurir:
                            thread.join()
                    if resiresult != None:
                        i["kurir"] = resiresult["kurir"]
                        if i["last_history"] != resiresult["last_history"] and chat_id == 0:
                            i["last_history"] = resiresult["last_history"]
                            if resiresult["status"] == "delivered":
                                status_text = choice(["paket dah nyampe bre", "paket lu nih nyet", "PAAKEEET, PANTAT TOKEET"])
                                report = status_text + "\n" + resiresult["kurir"] + " - " + resiresult["resi"]
                                if i["item"] != '':
                                    report += "\n" + i["item"]
                                report += "\n\n" + resiresult["history"]
                                listresi["data"].remove(i)
                            else:
                                if resiresult["status"] == "otw":
                                    status_text = choice(["otw cuuy", "gaskuyngeng", "dah otewe ngab", "OTW ngentooood"])
                                elif resiresult["status"] == "error":
                                    status_text = choice(["error anjir", "kek ada yg aneh", "problematika", "kenapaneh?"])
                                else:
                                    status_text = "update"
                                report = resiresult["kurir"] + " " + status_text + " - " + resiresult["resi"]
                                if i["item"] != '':
                                    report += "\n" + i["item"]
                                report += "\n\n" + resiresult["last_history"]
                            if "foto" in resiresult:
                                if i["kurir"] == "AnterAja":
                                    sendphotousingcontent(i["chat_id"], resiresult["foto"])
                            sendchat(i["chat_id"], report)
                        if i["chat_id"] == chat_id:
                            report = resiresult["kurir"] + " - " + resiresult["resi"]
                            if i["item"] != '':
                                report += "\n" + i["item"]
                            report += "\n\n" + resiresult["history"]
                            if "foto" in resiresult:
                                if i["kurir"] == "AnterAja":
                                    sendphotousingcontent(i["chat_id"], resiresult["foto"])
                            sendchat(chat_id, report)
                listresi["lastchecked"] = datetime.timestamp(datetime.now())
                with open('listresi.json', 'w') as outfile:
                    json.dump(listresi, outfile, indent=4)
            cekresionprogress = False
    except:
        sendchat(boschatid, traceback.format_exc())

def resisicepat(resi):
    try:
        url = "https://content-main-api-production.sicepat.com/public/check-awb/" + str(resi)
        r = requests.get(url)
        if r.status_code == 200:
            r = json.loads(r.text)["sicepat"]["result"]
            result = {}
            result["resi"] = resi
            result["kurir"] = "SiCepat"
            result["sender"] = r["sender"]
            result["sender_address"] = r["sender_address"]
            result["receiver"] = r["receiver_name"]
            result["receiver_address"] = r["receiver_address"]
            result["foto"] = [r["pod_img_path"],r["pod_sigesit_img_path"],r["pod_sign_img_path"],r["pop_sigesit_img_path"]]
            if r["last_status"]["status"] == "ANT":
                result["status"] = "otw"
            elif r["last_status"]["status"] == "DELIVERED":
                result["status"] = "delivered"
            elif r["last_status"]["status"] in ("PICKREQ", "DROP", "IN", "OUT", "PICK"):
                result["status"] = "update"
            else:
                result["status"] = "error"
            result["history"] = ""
            for i in r["track_history"]:
                try:
                    result["last_history"] = "> " + str(i["date_time"]) + " - " + str(i["city"])
                except:
                    result["last_history"] = "> " + str(i["date_time"]) + " - " + str(i["receiver_name"])
                result["history"] += result["last_history"] + "\n"
            global resiresult
            resiresult = result
        return
    except:
        return

def resijne(resi):
    try:
        s = requests.session()
        r = s.get("https://www.jne.co.id/id/tracking/trace")
        r = r.text
        token = r.split('<input name="_token" type="hidden" value="')[1].split('">')[0]
        payload = {
            '_token' : token,
            'code' : resi
        }
        s.headers['Referer'] = 'https://www.jne.co.id/id/tracking/trace'
        r = s.post("https://www.jne.co.id/id/tracking/trace", data=payload)
        r = s.get("https://cekresi.jne.co.id/" + resi)
        r = r.text
        
        if "Airwaybill is not found or not process yet" not in r:
            result = {}
            result["resi"] = resi
            result["kurir"] = "JNE"
            result["sender"] = r.split('Shipper Name')[1].split('<b>')[1].split('</b>')[0]
            result["history"] = ""
            history = r.split('History Status')[1].split('Receiver Name')[0].split('<li>')
            del history[0]
            for i in history:
                history_info = i.split('<a>')[1].split('</a>')[0]
                history_timestamp = i.split('<span>')[1].split('</span>')[0]
                result["last_history"] = "> " + history_timestamp + " - " + history_info
                if "WITH DELIVERY COURIER" in result["last_history"]:
                    result["status"] = "otw"
                elif "DELIVERED TO" in result["last_history"]:
                    result["status"] = "delivered"
                    result["receiver"] = r.split('Receiver Name')[1].split('<h4>')[1].split('</h4>')[0]
                else:
                    result["status"] = "update"
                if "receiver" in result:
                    result["history"] += result["last_history"] + " " + result["receiver"] + "\n"
                else:
                    result["history"] += result["last_history"] + "\n"
            global resiresult
            resiresult = result
        return
    except:
        return

def resijnt(resi):
    try:
        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        payload = {
            'method': 'query/findTrack',
            'data[billcode]': 'JP1743202221',
            'data[lang]': 'en',
            'data[source]': 3,
            'pId': '2baa4b6adf3ef723abf6ad53595382fe',
            'pst': '618d73cfacf737b97331b1ff45291888'
        }
        url = "https://jet.co.id/index/router/index.html"
        r = requests.post(url, data=payload, headers=header)
        r = json.loads(r.text.replace("\\",""))
        if not r["data"]["details"]:
            return
        else:
            r = r["data"]["details"]
            result = {}
            result["resi"] = resi
            result["kurir"] = "J&T"
            if r[-1]["scanstatus"] == "On Delivery":
                result["status"] = "otw"
            elif r[-1]["scanstatus"] == "Delivered":
                result["status"] = "delivered"
            elif r[-1]["scanstatus"] in ("Picked Up", "Departed", "Arrived"):
                result["status"] = "update"
            else:
                result["status"] = "error"
            result["history"] = ""
            for i in r:
                result["last_history"] = "> " + str(i["scantime"]) + " - " + str(i["desc"])
                if ["latitude"] != "-" and ["longitude"] != "-":
                    result["latitude"] = int(r["latitude"])
                    result["longitude"] = int(r["longitude"])
                    result["last_history"] += " : " + "https://www.google.com/maps/search/?api=1&query=" + str(result["latitude"]) + "," + str(result["longitude"])
                result["history"] += result["last_history"] + "\n"
            global resiresult
            resiresult = result
    except:
        return
    
def resianteraja(resi):
    try:
        header = {
            'Host': 'api.anteraja.id',
            'aca-customerphone': '',
            'appid': 'JV_APP',
            'msgid': '1555315559769',
            # 'ehead': {'accuracy': 0.0, 'lat': 0.0, 'lng': 0.0, 'time':-1, 'type': -1},
            'version': '1.0',
            'appversion': '1.7.40',
            'pushtoken': 'eyDqsepTQ5mIihsbUkdKi9:APA91bEXLSKS6OYfgWgjD9t-d4HlTHe1ENvrt65_R42qq1IXFR1jG-nhXCUsc_DubrcPTFAEtDdD_p0TLFbtNcZbOpfViDlozV9H4s8ns4rjpLIquBbXtacA6RrSAnmpU2ED6ENPfhbW',
            'imei': '702e29e7-d818-4dbd-bbe3-e54a0c604931',
            'deviceuuid': '702e29e7-d818-4dbd-bbe3-e54a0c604931',
            'hardwareserialno': '702e29e7-d818-4dbd-bbe3-e54a0c604931',
            'manufacture': 'OnePlus',
            'model': 'ONEPLUS A5010',
            'os': 'Android',
            'osversion': '10 Q',
            'latitude': '-6.980870',
            'longitude': '108.477570',
            'mv': '1.2',
            'source': 'aca_android',
            'clientcode': 'ACA',
            'accept': 'application/json',
            'token': 'pr_903cc66df009aff0a91efaf02943859a',
            'content-type': 'application/json; charset=UTF-8',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/4.7.2'
        }
        headerimage = {
            'Host': 'api.anteraja.id',
            'aca-customerphone': '',
            'appid': 'JV_APP',
            'msgid': '1555315559769',
            # 'ehead': {'accuracy': 0.0, 'lat': 0.0, 'lng': 0.0, 'time':-1, 'type': -1},
            'version': '1.0',
            'appversion': '1.7.40',
            'pushtoken': 'eyDqsepTQ5mIihsbUkdKi9:APA91bEXLSKS6OYfgWgjD9t-d4HlTHe1ENvrt65_R42qq1IXFR1jG-nhXCUsc_DubrcPTFAEtDdD_p0TLFbtNcZbOpfViDlozV9H4s8ns4rjpLIquBbXtacA6RrSAnmpU2ED6ENPfhbW',
            'imei': '702e29e7-d818-4dbd-bbe3-e54a0c604931',
            'deviceuuid': '702e29e7-d818-4dbd-bbe3-e54a0c604931',
            'hardwareserialno': '702e29e7-d818-4dbd-bbe3-e54a0c604931',
            'manufacture': 'OnePlus',
            'model': 'ONEPLUS A5010',
            'os': 'Android',
            'osversion': '10 Q',
            'latitude': '-6.980870',
            'longitude': '108.477570',
            'mv': '1.2',
            'source': 'aca_android',
            'clientcode': 'ACA',
            'token': 'pr_903cc66df009aff0a91efaf02943859a',
            'content-type': 'image/jpeg',
            'accept': 'image/jpeg',
            'user-agent': 'okhttp/4.7.2'
        }
        payload = [{"codes":resi,"phoneNumber":""}]
        payload = json.dumps(payload)
        url = "https://api.anteraja.id/order/tracking"
        r = requests.post(url, headers=header, data=payload)
        r = json.loads(r.text)["content"][0]
        if r != None:
            result = {}
            result["resi"] = resi
            result["kurir"] = "AnterAja"
            result["sender"] = r["detail"]["sender"]["name"]
            result["sender_address"] = r["detail"]["sender"]["address"]
            result["receiver"] = r["detail"]["receiver"]["name"]
            result["receiver_address"] = r["detail"]["receiver"]["address"]
            if int(r["detail"]["final_status"]) >= 400:
                result["status"] = "error"
            elif int(r["detail"]["final_status"]) == 240:
                result["status"] = "otw"
            elif int(r["detail"]["final_status"]) == 250:
                result["status"] = "delivered"
                try:
                    url = "https://api.anteraja.id/order/pod?awb=" + str(resi)
                    ri = requests.get(url,headers=header)
                    ri = json.loads(ri.text)["content"]
                    result["foto"] = []
                    for i in ri:
                        if i["imageType"] == "103":
                            url = "https://api.anteraja.id/order/pod/image?url=" + str(i["imageUrl"])
                            img = requests.get(url, headers=headerimage)
                            result["foto"] = img.content
                except Exception as e:
                    sendchat(boschatid, traceback.format_exc())
            else:
                result["status"] = "update"
            result["history"] = ""
            for i in reversed(r["history"]):
                result["last_history"] = "> " + str(i["timestamp"]) + " - " + str(i["message"]["id"])
                result["history"] += result["last_history"] + "\n"
            global resiresult
            resiresult = result
    except:
        return
        # sendchat(boschatid, traceback.format_exc())
        # sendchat(boschatid, traceback.format_exc())
        # sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
    
def resitokopedia(resi):
    try:
        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.tokopedia.com',
            'pragma': 'no-cache',
            'referer': 'https://www.tokopedia.com/',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
            }
        url = 'https://orchestra.tokopedia.com/orc/v1/microsite/tracking?airwaybill=' + str(resi)
        r = requests.get(url, headers=header)
        r = json.loads(r.text)["data"][0]
        if r["error_message"] == '':
            result = {}
            result["resi"] = resi
            result["kurir"] = "Tokopedia"
            result["sender"] = r["seller"]["name"]
            result["sender_address"] = r["seller"]["address"]
            result["receiver"] = r["buyer"]["name"]
            result["receiver_address"] = r["buyer"]["address"]
            result["status"] = "update"
            result["history"] = ""
            for i in reversed(r["tracking_data"]):
                result["last_history"] = "> " + str(i["tracking_time"]) + " - " + str(i["message"])
                result["history"] += result["last_history"] + "\n"
            global resiresult
            resiresult = result
    except:
        return
        # sendchat(boschatid, traceback.format_exc())


def sendchat(chat_id, chat, dump = True, **kwargs):
    disableWebView = kwargs.get('disableWebView', False)
    chat = str(chat)
    if len(chat) > 4096:
        chats = chat.split("\n")
        chat = []
        lines = ""
        for line in chats:
            if len(lines + line + "\n") > 4096:
                chat.append(lines)
                lines = line + "\n"
            else:
                lines += line + "\n"
    if isinstance(chat, str):
        chats = []
        chats.append(chat)
    else:
        chats = chat

    for chat in chats:
        if killbot:
            break
        payload = {"chat_id": chat_id, "text": str(chat), "disable_web_page_preview": disableWebView}
        result = requests.post(url+'sendMessage', data=payload)
        if dump:
            payloaddump = {"chat_id": '-355139963', "text": "--- " + str(chat_id) + " ---\n" + str(chat)}
            Thread(target=requests.post, args=(url+'sendMessage', payloaddump,)).start()
    return result


def editmessage(chat_id, message_id, chat, **kwargs):
    disableWebView = kwargs.get('disableWebView', False)
    chat = str(chat)
    if len(chat) > 4096:
        Exception("chat too long")
    payload = {"chat_id": chat_id, "message_id": message_id, "text": str(chat), "disable_web_page_preview": disableWebView}
    return requests.post(url+'editMessageText', data=payload)

def deletechat(chat_id, message_id):
    payload = {"chat_id": chat_id, "message_id": message_id}
    requests.post(url+'deleteMessage', data=payload)

def sendvideo(chat_id, link):
    payload = {"chat_id": chat_id, "video": str(link)}
    try:
        requests.post(url+'sendVideo', data=payload)
    except Exception as e:
        sendchat(boschatid, "error sendvideo\n" + str(getattr(e, 'message', repr(e))))


def sendphoto(chat_id, photourl, caption):
    payload = {"chat_id": chat_id, "photo": str(photourl), "caption": str(caption)}
    try:
        r = requests.post(url+'sendPhoto', data=payload)
        return json.loads(r.text)
    except Exception as e:
        sendchat(boschatid, "error sendphoto\n" + str(getattr(e, 'message', repr(e))))


def sendphotousingcontent(chat_id, photocontent, caption = ""):
    payload = {"chat_id": chat_id, "caption": str(caption)}
    try:
        r = requests.post(url+'sendPhoto', data=payload, files={"photo": photocontent})
        return json.loads(r.text)
    except Exception as e:
        sendchat(boschatid, "error sendphoto\n" + str(getattr(e, 'message', repr(e))))


def sendmediagroup(chat_id, photourl1, photourl2, caption):
    try:
        arraypayload = [{"type": "photo", "media": photourl1, "caption": caption}, {
            "type": "photo", "media": photourl2}]
        arraypayload = json.dumps(arraypayload)
        payload = {"chat_id": chat_id, "media": arraypayload}
        r = requests.post(url+'sendMediaGroup', data=payload)
        return json.loads(r.text)
    except Exception as e:
        sendchat(boschatid, "error sendmediagroup\n" + str(getattr(e, 'message', repr(e))))


def dump(sender, chat_id, chat):
    # payload = {"chat_id": "-355139963", "text": sender + "(" + str(chat_id) + '):' + str(chat)}
    try:
        # sendchat('-355139963',sender +"(" + str(chat_id) + '):' + str(chat), False)
        Thread(target=sendchat, args=('-355139963',sender +"(" + str(chat_id) + '):' + str(chat), False,)).start()
        # requests.post(url+'sendMessage', data=payload)
    except Exception as e:
        sendchat(boschatid, "error dump\n" + str(getattr(e, 'message', repr(e))))


def deeraTheGoldDigger():
    while phoenix and autodeera:
        global oldelementsdeera, deeradump
        try:
            a = "a"
            url = 'https://t.me/s/DeeraTheGoldigger'
            a = "b"
            r = requests.get(url,timeout=30)
            a = "c"
            soup = BeautifulSoup(r.content, 'html.parser')
            a = "d"
            timeElement = soup.find_all("time", class_="time")
            a = "e"
            timeElement = timeElement[len(timeElement)-1]
            if deeradump:
                sendchat(boschatid,timeElement)
                deeradump = False
            a = "e2"
            if timeElement != oldelementsdeera and oldelementsdeera != '':
                a = "f"
                oldelementsdeera = timeElement
                a = "f2"
                messageElements = soup.find_all("div", class_="tgme_widget_message_wrap js-widget_message_wrap")
                a = "f3"
                elements = messageElements[len(messageElements)-1]
                a = "g"
                dump('deera',6969,str(elements))
                if "In The Zone" in str(elements):
                    try:
                        a = "h"
                        # soup = BeautifulSoup(elements, 'html.parser')
                        a = "i"
                        # elements = soup.find_all("div", class_="tgme_widget_message_text js-message_text")
                        a = "j"
                        elements = str(elements).split('<div class="tgme_widget_message_text js-message_text" dir="auto"><b>Gold ')[1]
                        elements = str(elements).split('<div class="tgme_widget_message_footer compact js-message_footer">')[0]
                        a = "k"
                        elements = str(elements).replace('<br/>','')
                        a = "l"
                        elements = str(elements).replace('</b>','')
                        a = "m"
                        elements = str(elements).replace('[','')
                        a = "n"
                        elements = str(elements).replace(']','')
                        a = "o"
                        # print(elements)
                        command(boschatid,'gold',elements,'andimahathir')
                        sendchat(boschatid,elements)
                    except Exception as e:
                        sendchat(boschatid,'gagal parsing In The Zone')
                        sendchat(boschatid, "error deera\n" + str(getattr(e, 'message', repr(e))))
            else:
                a = "p"
                oldelementsdeera = timeElement
        except Exception as e:
            sendchat(boschatid, "error deera\n" + str(getattr(e, 'message', repr(e))))
            sendchat(boschatid, a)
        time.sleep(5)

def chatGPT(chat_id, content):
    global marbotGPT
    chatHistory = []
    if chat_id in marbotGPT:
        chatHistory = marbotGPT[chat_id]
    openai.api_key = "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"
    chatHistory.append({"role": "user", "content": content},)
    # messageid = json.loads(sendchat(chat_id, "B🤖T thinkin💭...").text)["result"]["message_id"]
    messageid = json.loads(sendchat(chat_id, "🤖💭").text)["result"]["message_id"]
    answer = ""
    start = time.time()
    for delta in openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chatHistory, stream=True,):
        try:
            if start < time.time() - 1 and len(answer.replace(" ","")) > 0:
                start = time.time()
                editmessage(chat_id, messageid, answer)
            newdelta = str(delta["choices"][0]["delta"]["content"])
            # if len(answer) + len(newdelta) > 4096:
            #     # send the answer as edited message
            #     print(answer)
            #     answer = newdelta
            #     # sendchat(answer)
            #     messageidtoedit = messageidtoedit
            #     continue
            answer += newdelta
        except:
            pass
    editmessage(chat_id, messageid, answer + "\n\n### 🤖 ###")
    # sendchat(chat_id, "- D🤖NE -")
    chatHistory.append({"role": "assistant", "content": answer},)
    marbotGPT[chat_id] = chatHistory
    # sendchat(chat_id, answer["choices"][0]["message"]["content"])
    sendchat("-355139963", answer)

async def BingGPT(chat_id, prompt):
    messageid = json.loads(sendchat(chat_id, "🤖💭").text)["result"]["message_id"]
    answer = ""
    start = time.time()
    async for resp in  bingGPT[chat_id].ask_stream(prompt=prompt, conversation_style=ConversationStyle.creative):
        if resp[0] == False:
            try:
                answer = resp[1]
                if start < time.time() - 1 and len(answer.replace(" ","")) > 0:
                    answer = BingBracketCleaner(answer)
                    start = time.time()
                    editmessage(chat_id, messageid, answer, disableWebView = True)
            except:
                pass
        if resp[0] == True:
            answer = BingBracketCleaner(answer)
    await bingGPT[chat_id].close()
    answer += "\n### 🤖 ###"
    editmessage(chat_id, messageid, answer, disableWebView = True)
    Thread(target=sendchat, args=(-355139963, answer,)).start()


def BingBracketCleaner(answer):
    while True:
        if answer.find("[^") < 0:
            break
        pre = answer.find("[^")
        suf = answer.find("^]")
        answer = answer[:pre] + answer[suf+2:]
    return answer


def cekabsenweb(chat_id, nip, date_awal, date_akhir = ""):
    try:
        if date_akhir == "":
            date_akhir = date_awal
        
        if datetime.strptime(date_awal, "%d/%m/%Y") > datetime.strptime(date_akhir, "%d/%m/%Y"):
            date_awal, date_akhir = date_akhir, date_awal
        
        while datetime.strptime(date_awal, "%d/%m/%Y") <= datetime.strptime(date_akhir, "%d/%m/%Y"):
            
            urlcekabsen = "https://ropeg.setjen.kemendagri.go.id/restsimpeg/index.php/ssoview/cek_fp/" + str(nip) + "/" + str(date_awal)
                
            r = requests.get(urlcekabsen, timeout=60, verify=False)
            r = r.text.split("<tbody>")[1].split("</tbody>")[0]
            r = r.split("<b>")
            counter = 0
            result = ""
            for i in r[1:]:
                if counter == 0:
                    pass
                elif counter % 2 == 0:
                    result += "\n"
                else:
                    result += " : "
                result += i.split("</b>")[0]
                counter += 1
            if chat_id == "system":
                return result
            
            sendchat(chat_id, result)
            
            date_awal = (datetime.strptime(date_awal, "%d/%m/%Y") + timedelta(days= 1)).strftime("%d/%m/%Y")
    
    except Exception as e:
        sendchat(boschatid, traceback.format_exc())


def cekabsensimpeg(chat_id, nip, date_awal, date_akhir = ""):
    try:
        if date_akhir == "":
            date_akhir = date_awal

        if datetime.strptime(date_awal, "%Y-%m-%d") > datetime.strptime(date_akhir, "%Y-%m-%d"):
            date_awal, date_akhir = date_akhir, date_awal
        
        payload = {
            'tanggal_awal': date_awal,
            'nip': nip,
            'tanggal_akhir': date_akhir,
            'token': 'af9ec164748d7690c4f58021b6907d8d'
        }
        urlcekabsen = "https://ropeg.setjen.kemendagri.go.id/restsimpeg/api/bni_history_absen"
        r = requests.post(urlcekabsen, data=payload)
        r = json.loads(r.text)["results"]
        
        logabsen = ""
        for i in reversed(r):
            logabsen += i["areaname"] + " - " + i["alias"] + " - " + i["checktime"] + "\n"
        sendchat(chat_id, logabsen)
    
    except Exception as e:
        sendchat(boschatid, traceback.format_exc())


def indraNusantara():
    while phoenix:
        global oldelementsindra
        try:
            a = "a"
            url = 'https://t.me/s/indranusantara1'
            a = "b"
            r = requests.get(url,timeout=30)
            a = "c"
            soup = BeautifulSoup(r.content, 'html.parser')
            a = "d"
            timeElement = soup.find_all("time", class_="time")
            a = "e"
            timeElement = timeElement[len(timeElement)-1]
            # if deeradump:
            #     sendchat(boschatid,timeElement)
            #     deeradump = False
            a = "e2"
            if timeElement != oldelementsindra and oldelementsindra != '':
                a = "f"
                oldelementsindra = timeElement
                a = "f2"
                messageElements = soup.find_all("div", class_="tgme_widget_message_wrap js-widget_message_wrap")
                a = "f3"
                elements = messageElements[len(messageElements)-1]
                a = "g"
                elements = str(elements).split('<div class="tgme_widget_message_text js-message_text" dir="auto">')[1]
                elements = str(elements).split('<div class="tgme_widget_message_footer compact js-message_footer">')[0]
                # dump('indra',9696,str(elements))
                if "Gold buy now" in str(elements) and "top" not in str(elements):
                    try:
                        # command(boschatid,'gold','indrabuy','andimahathir')
                        sendchat(boschatid, "indrabuy")
                    except Exception as e:
                        sendchat(boschatid,'gagal sending command')
                        sendchat(boschatid, "error indrabuy\n" + str(getattr(e, 'message', repr(e))))
                elif "Gold sell now" in str(elements) and "top" not in str(elements):
                    try:
                        # command(boschatid,'gold','indrasell','andimahathir')
                        sendchat(boschatid, "indrasell")
                    except Exception as e:
                        sendchat(boschatid,'gagal sending command')
                        sendchat(boschatid, "error indrasell\n" + str(getattr(e, 'message', repr(e))))
                if "Gold buy now" in str(elements) or "Gold sell now" in str(elements):
                    try:
                        a = "h"
                        # soup = BeautifulSoup(elements, 'html.parser')
                        a = "i"
                        # elements = soup.find_all("div", class_="tgme_widget_message_text js-message_text")
                        a = "j"
                        # elements = str(elements).split('</div><div class="tgme_widget_message_footer compact js-message_footer">')[0]
                        a = "k"
                        elements = str(elements).replace('<br/>','')
                        elements = str(elements).replace('</div>','')
                        a = "l"
                        elements = str(elements).replace('</b>','')
                        a = "m"
                        elements = str(elements).replace('[','')
                        a = "n"
                        elements = str(elements).replace(']','')
                        a = "o"
                        # print(elements)
                        # command(boschatid,'gold',elements,'andimahathir')
                        sendchat(-1001194816434,elements)
                    except Exception as e:
                        sendchat(boschatid,'gagal parsing In The Zone')
                        sendchat(boschatid, "error indra\n" + str(getattr(e, 'message', repr(e))))
            else:
                a = "p"
                oldelementsindra = timeElement
        except Exception as e:
            pass
            # sendchat(boschatid, e)
            # sendchat(boschatid, a)
        time.sleep(5)

def generatealamat(lat,lang):
    generatealamaturl = "https://google-maps-geocoding.p.rapidapi.com/geocode/json"
    payload = {
        "latlng":lat + ","+ lang, "language":"en"
        }
    headers = {
        "X-RapidAPI-Host": "google-maps-geocoding.p.rapidapi.com",
        "X-RapidAPI-Key": "6b08c2ead2msh8e59c0c72450219p18ce3fjsn6b34f2f8d3a9"
        }
    try:
        r = requests.get(generatealamaturl, headers=headers, params=payload)
        if r.status_code == 200:
            r = json.loads(r.text)
            if r["status"] == "OK":
                return r
            else:
                sendchat(boschatid, "generate alamat error " + str(json.dumps(r)))
                return "not ok"
        else:
            sendchat(boschatid, "generate alamat error " + str(r.status_code))
            return "not ok"
    except Exception as e:
        sendchat(boschatid, "Error generate alamat()\n" + getattr(e, 'message', repr(e)))
        return "not ok"


def absen(content="now",target=boschatid):
    try:
        if content == "now":
            nip = "199207292020121010"
            imei = "6f439b7d9483f36f"
        elif content == "satya":
            nip = "199108082020121016"
            imei = "975b6dd1ba1f415f"
        elif content == "dita":
            nip = "199104072020122018"
            imei = "a6409573e48d69ec"
        elif content == "dian":
            nip = "198712192020122009"
            imei = "e5bce863ca598c0f"
        elif len(content) == 18:
            nip = content
            imei = ""
        else:
            sendchat(chat_id, "maksudnya?")
            return
        # if (statusabsen or time == "now"):
        # if (datetime.now().strftime("%H") == jamabsen or time == "now"):
        #     if(datetime.now().strftime("%M") >= menitabsen or time == "now"):
        #         time.sleep(int(randint(1,59)))
        
        sn = "MESIN002HPUPC"
        token = "af9ec164748d7690c4f58021b6907d8d"
        status = "2"

        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; ONEPLUS A5010 Build/QKQ1.191014.012)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'ropeg.setjen.kemendagri.go.id',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

        horizontalstart = -6.270512
        verticalstart = 106.8449850
        horizontaldiff = float("{0:.7f}".format(0.0000001 * randint(0, 8610)))
        verticaldiff = float("{0:.7f}".format(0.0000001 * randint(0, 3750)))
        horizontalline = "{0:.7f}".format(horizontalstart + horizontaldiff)
        verticalline = "{0:.7f}".format(verticalstart + verticaldiff)
        lokasi = horizontalline + "," + verticalline
        current_date = date.today().strftime("%d-%m-%Y")
        if int(datetime.now().strftime("%H")) == 9 and int(datetime.now().strftime("%M")) <= 7:
            current_time = "09:00:00"
        else:
            current_time = datetime.now().strftime("%H:%M:%S")
        current_datetime = current_date + " " + current_time
        # print(current_datetime)

        payload = {
            'nip': nip,
            'lokasi': lokasi,
            'imei': imei,
            'nohp': '',
            'sn': sn,
            'tanggal': current_datetime,
            'token': token,
            'status': status
        }

        r = requests.post("https://ropeg.setjen.kemendagri.go.id/restsimpeg/api/bni_absen2",data=payload, headers=headers, timeout=60, verify=False)
        sendchat(target, r.request.body)
        sendchat(target, r.text)
        if date.today().strftime("%d") == 16 and date.today().strftime("%A") != "Friday":
            sendchat(target, "Jangan lupa besok pake korpri")
        elif date.today().strftime("%d") == 14 and date.today().strftime("%A") == "Friday":
            sendchat(target, "Jangan lupa senin pake korpri")
        return r.text
    except Exception as e:
        sendchat(boschatid, "Error absen()\n" + getattr(e, 'message', repr(e)))


def notifdirekturpulang():
    global direkturpulang, direkturchecker
    hari = datetime.now().strftime("%A")
    if hari != "Sunday" and hari != "Saturday" and direkturchecker:
        today = date.today().strftime("%d/%m/%Y")
        result = cekabsenweb("system","197204251992031001",today)
        result = result.split("Jam Keluar : ")[1].split("\nKeterangan")[0]
        if result != direkturpulang:
            direkturpulang = result
            # sendchat(boschatid, result)
            if direkturpulang not in ["-", " "]:
                sendchat(boschatid, "direktur pulang")



def wfh(content="now", target=boschatid):
    try:
        if content == "now":
            nip = "199207292020121010"
            imei = "6f439b7d9483f36f"
            firstlat = -6.23159
            firstlong = 106.85637
            alamatcadangan = "Jl. Tebet Timur Dalam IV F No.16, RT.2/RW.11, Tebet Tim., Kec. Tebet, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12820, Indonesia"
        elif content == "satya":
            nip = "199108082020121016"
            imei = "975b6dd1ba1f415f"
            firstlat = -6.29354
            firstlong = 106.73511
            alamatcadangan = "Jl. Menjangan Raya No.88, RT.2/RW.1, Sawah Lama, Kec. Ciputat, Kota Tangerang Selatan, Banten 15412, Indonesia"
        elif content == "dita":
            nip = "199104072020122018"
            imei = "a6409573e48d69ec"
            firstlat = -6.40025
            firstlong = 106.84754
            alamatcadangan = "Jl. Abdullah No.142, Abadijaya, Kec. Sukmajaya, Kota Depok, Jawa Barat 16417, Indonesia"
        elif content == "dian":
            nip = "198712192020122009"
            imei = "e5bce863ca598c0f"
            firstlat = -6.39234
            firstlong = 106.83891
            alamatcadangan = "Blk. B, Jl. Proklamasi No.20, Mekar Jaya, Kec. Sukmajaya, Kota Depok, Jawa Barat 16411, Indonesia"
        else:
            nip = content
            imei = ""
            firstlat = -6.26996
            firstlong = 106.84531
            alamat = "komplek bangdes, RT.7/RW.1, West Pejaten, Pasar Minggu, South Jakarta City, Jakarta 12510, Indonesia"
            
        # if (statusabsen or time == "now"):
        # if (datetime.now().strftime("%H") == jamabsen or time == "now"):
        #     if(datetime.now().strftime("%M") >= menitabsen or time == "now"):
        #         time.sleep(int(randint(1,59)))
        
        sn = "MSSIMPEG001WFH"
        token = "af9ec164748d7690c4f58021b6907d8d"
        status = "2"

        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; ONEPLUS A5010 Build/QKQ1.191014.012)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'ropeg.setjen.kemendagri.go.id',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

        # horizontalstart = -6.270512
        # verticalstart = 106.8449850
        # horizontaldiff = float("{0:.7f}".format(0.0000001 * randint(0, 8610)))
        # verticaldiff = float("{0:.7f}".format(0.0000001 * randint(0, 3750)))
        # horizontalline = "{0:.7f}".format(horizontalstart + horizontaldiff)
        # verticalline = "{0:.7f}".format(verticalstart + verticaldiff)
        # lokasi = horizontalline + "," + verticalline
        
        lastlat = float("{0:.7f}".format(0.0000001 * randint(1, 99)))
        lastlong = float("{0:.7f}".format(0.0000001 * randint(1, 99)))
        lat = "{0:.7f}".format(firstlat - lastlat)
        long = "{0:.7f}".format(firstlong + lastlong)
        lokasi = lat + "," + long
        alamat = generatealamat(lat,long)
        if alamat != "not ok":
            alamat = alamat["results"][0]["formatted_address"]
            # alamat = alamat.replace(" ","+")
        else:
            alamat = alamatcadangan
        
        current_date = date.today().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        current_datetime = current_date + " " + current_time
        # print(current_datetime)

        payload = {
            'nip': nip,
            'lokasi': lokasi,
            'imei': imei,
            'nohp': '',
            'sn': sn,
            'tanggal': current_datetime,
            'token': token,
            'status': status,
            'alamat': alamat
        }

        r = requests.post("https://ropeg.setjen.kemendagri.go.id/restsimpeg/api/bni_absen_wfh",data=payload, headers=headers, timeout=60, verify=False)
        sendchat(target, r.request.body)
        sendchat(target, r.text)
        return r.text
    except Exception as e:
        sendchat(boschatid, "Error wfh()\n" + getattr(e, 'message', repr(e)))


def command(chat_id, order, content, username):
    global testpvuscan, pvubot, phoenix
    charcount = 0
    # try:
    #     mydb = mysql.connector.connect(
    #         host="localhost",
    #         user="root",
    #         password="",
    #         database="ktpsurabaya"
    #     )
    # except:
    #     sendchat(boschatid, "mysql connect error")
    # print("masuk mydb connect")
    if order == "nik":
        # try:
        #     mycursor = mydb.cursor(dictionary=True)
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian nik diproses...")
        # print(username+" is requesting for searching by nik...")
        # print(content)
        try:
            result = queryDatabase("SELECT no_kk,nik,nama_lengkap,pekerjaan,provinsi,kota,agama,tempat_lahir,tgl_lahir,kecamatan,kelurahan,alamat,rw,rt,jenis_kelamin,status_kawin,kewarganegaraan FROM ktpsurabaya WHERE nik LIKE '%"+content+"%'")
            # result = mycursor.fetchall()
            for i in result:
                sendchat(chat_id, str(i))
            sendchat(chat_id, "pencarian nik selesai!")
            print("searching by nik is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            print("wrong mantra")
    elif order == "add":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian berdasarkan alamat diproses...")
        # print(username+" is requesting for searching by add...")
        # print(content)
        try:
            result = queryDatabase("SELECT nik,alamat,tgl_lahir,nama_lengkap FROM ktpsurabaya WHERE alamat LIKE '%"+content+"%' ORDER BY alamat ASC", False)
            # result = mycursor.fetchall()
            hasil = ""
            for i in result:
                hasil = str(hasil) + str(i) + str("\n")
            sendchat(chat_id, str(hasil))
            sendchat(chat_id, "pencarian berdasarkan alamat selesai!")
            # print("searching by add is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "name":
        # # print("masuk elif name")
        # try:
        #     mycursor = mydb.cursor()
        #     # print("create cursor")
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian berdasarkan nama diproses...")
        # print(username+" is requesting for searching by name...")
        # print(content)
        try:
            # print("otw exe")
            result = queryDatabase("SELECT nik,tgl_lahir,nama_lengkap FROM ktpsurabaya WHERE nama_lengkap LIKE '%"+content+"%' ORDER BY nama_lengkap ASC", False)
            # print("cursor exe")
            # result = mycursor.fetchall()
            # print("fetchall beres")
            hasil = ""
            
            # for i in result:
            #     if killbot:
            #         break
            #     if len(str(hasil) + str(i) + str("\n")) > 4096:
            #         sendchat(chat_id, hasil)
            #         hasil = str(i) + str("\n")
            #         continue
            #     hasil += str(i) + str("\n")
            
            for i in result:
                hasil += str(i) + str("\n")
            
            sendchat(chat_id, str(hasil))
            sendchat(chat_id, "pencarian berdasarkan nama selesai!")
            # print("searching by name is done")
        # except mysql.connector.Error:
        #     sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
        #     print("wrong mantra")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "name2":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian nama berdasarkan 2 kata diproses...")
        # print(username+" is requesting for searching by name2...")
        # print(content)
        try:
            content1 = str(content).split(' ')[0]
            content2 = str(content).split(' ')[1]
            result = queryDatabase(
                "SELECT nik,tgl_lahir,nama_lengkap FROM ktpsurabaya WHERE nama_lengkap LIKE '%"+content1+"%' AND nama_lengkap LIKE '%"+content2+"%' ORDER BY nama_lengkap ASC", False)
            # result = mycursor.fetchall()
            hasil = ""
            for i in result:
                hasil = str(hasil) + str(i) + str("\n")
                
            sendchat(chat_id, str(hasil))
            sendchat(chat_id, "pencarian nama berdasarkan 2 kata selesai!")
            # print("searching by name2 is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "name3":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian nama berdasarkan 3 kata diproses...")
        # print(username+" is requesting for searching by name3...")
        # print(content)
        try:
            content1 = str(content).split(' ')[0]
            content2 = str(content).split(' ')[1]
            content3 = str(content).split(' ')[2]
            result = queryDatabase(
                "SELECT nik,tgl_lahir,nama_lengkap FROM ktpsurabaya WHERE nama_lengkap LIKE '%"+content1+"%' AND nama_lengkap LIKE '%"+content2+"%' AND nama_lengkap LIKE '%"+content3+"%' ORDER BY nama_lengkap ASC", False)
            # result = mycursor.fetchall()
            hasil = ""
            for i in result:
                hasil = str(hasil) + str(i) + str("\n")
                
            sendchat(chat_id, str(hasil))
            sendchat(chat_id, "pencarian nama berdasarkan 3 kata selesai!")
            # print("searching by name3 is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "nokk":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian berdasarkan nomor kk diproses...")
        # print(username+" is requesting for searching by nokk...")
        # print(content)
        try:
            result = queryDatabase(
                "SELECT nik,nama_lengkap FROM ktpsurabaya WHERE no_kk='"+content+"'")
            # result = mycursor.fetchall()
            hasil = ""
            for i in result:
                hasil = str(hasil) + str(i) + str("\n")
            sendchat(chat_id, str(hasil))
            sendchat(chat_id, "pencarian berdasarkan nomor kk selesai!")
            # print("searching by nokk is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "date":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian berdasarkan tanggal diproses...")
        # print(username+" is requesting for searching by date...")
        try:
            tanggal = str(content).split('-')[0]
            bulan = str(content).split('-')[1]
            tahun = str(content).split('-')[2]
            tanggalcowo = content
            tanggalcewe = str(int(tanggal)+40)+'-'+bulan+'-'+tahun
            # print(content)
            result = queryDatabase(
                "SELECT nik,nama_lengkap FROM ktpsurabaya WHERE tgl_lahir='"+tanggalcowo+"' OR tgl_lahir='"+tanggalcewe+"' ORDER BY nama_lengkap ASC", False)
            # result = mycursor.fetchall()
            hasil = ""
            for i in result:
                hasil = str(hasil) + str(i) + str("\n")
            sendchat(chat_id, str(hasil))
            sendchat(chat_id, "pencarian berdasarkan tanggal selesai!")
            # print("searching by date is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "niknokk":
        # try:
        #     mycursor = mydb.cursor(dictionary=True)
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian berdasarkan nik dan nokk diproses...")
        # print(username+" is requesting for searching by nik and nokk...")
        # print(content)
        try:
            result = queryDatabase(
                "SELECT no_kk,nik,nama_lengkap,pekerjaan,provinsi,kota,agama,tempat_lahir,tgl_lahir,kecamatan,kelurahan,alamat,rw,rt,jenis_kelamin,status_kawin,kewarganegaraan FROM ktpsurabaya WHERE no_kk=(SELECT no_kk FROM ktpsurabaya WHERE nik='"+content+"')")
            # result = mycursor.fetchall()
            hasil = ""
            for i in result:
                sendchat(chat_id, str(i))
            sendchat(chat_id, "pencarian berdasarkan nik dan nokk selesai!")
            # print("searching by nik and nokk is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "nikadd":
        # try:
        #     mycursor = mydb.cursor(dictionary=True)
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian berdasarkan nik dan alamat diproses...")
        # print(username+" is requesting for searching by nik and address...")
        # print(content)
        try:
            result = queryDatabase(
                "SELECT no_kk,nik,nama_lengkap,pekerjaan,provinsi,kota,agama,tempat_lahir,tgl_lahir,kecamatan,kelurahan,alamat,rw,rt,jenis_kelamin,status_kawin,kewarganegaraan FROM ktpsurabaya WHERE alamat=(SELECT alamat FROM ktpsurabaya WHERE nik='"+content+"')")
            # result = mycursor.fetchall()
            hasil = ""
            for i in result:
                sendchat(chat_id, str(i))
            sendchat(chat_id, "pencarian berdasarkan nik dan alamat selesai!")
            # print("searching by nik and address is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "nameadd":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        # print(username+" is requesting for searching by nameadd...")
        # print(content)
        try:
            content1 = str(content).split(';')[0]
            content2 = str(content).split(';')[1]
            result = queryDatabase(
                "SELECT nik,tgl_lahir,nama_lengkap FROM ktpsurabaya WHERE nama_lengkap LIKE '%"+content1+"%' AND (alamat LIKE '%"+content2+"%' OR kecamatan LIKE '%"+content2+"%' OR kelurahan LIKE '%"+content2+"%') ORDER BY nama_lengkap ASC")
            # result = mycursor.fetchall()
            hasil = ""
            for i in result:
                hasil = str(hasil) + str(i) + str("\n")
                
            sendchat(chat_id, str(hasil))
            sendchat(chat_id, "pencarian nama berdasarkan alamat kata selesai!")
            # print("searching by nameadd is done")
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "absen":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        try:
            if(username == "andimahathir" or username == "yatnosyarifudin"):
                if content == "list":
                    filejson = open("listabsen.json",)
                    listabsen = json.load(filejson)
                    filejson.close()
                    listabsenseparate = ""
                    for i in listabsen:
                        listabsenseparate = listabsenseparate + i + ":" + str(listabsen[i]) + "\n"
                    sendchat(chat_id, listabsenseparate)
                elif content == "fix":
                    listabsen = {}
                    waktu = datetime.now()
                    tanggal = waktu.strftime("%Y%m%d")
                    listabsen[tanggal] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "libur"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "libur"
                        },
                        "sikerja": {
                            "status": "libur"
                        }
                    }
                    sendchat(chat_id, "ok")
                    with open('listabsen.json', 'w') as outfile:
                        json.dump(listabsen, outfile, indent=4)
                elif content == "dump":
                    filejson = open("listabsen.json",)
                    listabsen = json.load(filejson)
                    filejson.close()
                    sendchat(chat_id,listabsen)
                else:
                    absen(content)
            elif username == "satyapragolapati" and content == "now":
                sendchat(chat_id, "wait, klo gua g bales cek simpeg y")
                absen("satya",chat_id)
            elif username == "Shkmhs" and content == "now":
                sendchat(chat_id, "wait, klo gua g bales cek simpeg y")
                absen("dita",chat_id)
            elif username == "Deeyan127" and content == "now":
                sendchat(chat_id, "wait, klo gua g bales cek simpeg y")
                absen("dian",chat_id)
            else:
                sendchat(chat_id, "kon sopo jancok wkwk")
        except Exception as e:
            sendchat(boschatid, "error command absen\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "libur":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        try:
            if(username == "andimahathir" or username == "yatnosyarifudin"):
                filejson = open("listabsen.json",)
                listabsen = json.load(filejson)
                filejson.close()
                if(content == "today"):
                    waktu = datetime.now()
                    tanggal = waktu.strftime("%Y%m%d")
                    listabsen[tanggal] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "libur"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "libur"
                        },
                        "sikerja": {
                            "status": "libur"
                        }
                    }
                    sendchat(chat_id, "ok")
                else:
                    listabsen[content] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "libur"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "libur"
                        },
                        "sikerja": {
                            "status": "libur"
                        }
                    }
                    sendchat(chat_id, "ok")
                # sendchat(chat_id, listabsen)
                with open('listabsen.json', 'w') as outfile:
                    json.dump(listabsen, outfile, indent=4)
                # sendchat(chat_id, "noted boss...")
            else:
                sendchat(chat_id, "kon sopo jancok wkwk")
        except Exception as e:
            sendchat(boschatid, "error command libur\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "wfh":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        try:
            if(username == "andimahathir" or username == "yatnosyarifudin"):
                filejson = open("listabsen.json",)
                listabsen = json.load(filejson)
                filejson.close()
                if(content == "today"):
                    waktu = datetime.now()
                    tanggal = waktu.strftime("%Y%m%d")
                    listabsen[tanggal] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "wfh"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "wfh"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                    sendchat(chat_id, "ok")
                elif len(content) == 8:
                    listabsen[content] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "wfh"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "wfh"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                    sendchat(chat_id, "ok")
                else:
                    wfh(content)
                # sendchat(chat_id, listabsen)
                with open('listabsen.json', 'w') as outfile:
                    json.dump(listabsen, outfile, indent=4)
                # sendchat(chat_id, "noted boss...")
            elif username == "satyapragolapati" and content == "now":
                wfh("satya",chat_id)
            elif username == "Shkmhs" and content == "now":
                wfh("dita",chat_id)
            elif username == "Deeyan127" and content == "now":
                wfh("dian",chat_id)
            else:
                sendchat(chat_id, "kon sopo jancok wkwk")
        except Exception as e:
            sendchat(boschatid, "error command wfh\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "perdin":
        try:
            if(username == "andimahathir" or username == "yatnosyarifudin"):
                filejson = open("listabsen.json",)
                listabsen = json.load(filejson)
                filejson.close()
                if(content == "today"):
                    waktu = datetime.now()
                    tanggal = waktu.strftime("%Y%m%d")
                    listabsen[tanggal] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "perdin"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "perdin"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                    sendchat(chat_id, "ok")
                elif len(content) == 8:
                    listabsen[content] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "perdin"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "perdin"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                    sendchat(chat_id, "ok")
                # else:
                #     wfh(content)
                # sendchat(chat_id, listabsen)
                with open('listabsen.json', 'w') as outfile:
                    json.dump(listabsen, outfile, indent=4)
                # sendchat(chat_id, "noted boss...")
            else:
                sendchat(chat_id, "kon sopo jancok wkwk")
        except Exception as e:
            sendchat(boschatid, "error command perdin\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
    elif order == "absenmasuk":
        try:
            if(username == "andimahathir" or username == "yatnosyarifudin"):
                filejson = open("listabsen.json",)
                listabsen = json.load(filejson)
                filejson.close()
                if(content == "today"):
                    waktu = datetime.now()
                    tanggal = waktu.strftime("%Y%m%d")
                    listabsen[tanggal] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "notyet"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "done"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                    sendchat(chat_id, "ok")
                elif len(content) == 8:
                    listabsen[content] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "notyet"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "done"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                    sendchat(chat_id, "ok")
                # else:
                #     wfh(content)
                # sendchat(chat_id, listabsen)
                with open('listabsen.json', 'w') as outfile:
                    json.dump(listabsen, outfile, indent=4)
                # sendchat(chat_id, "noted boss...")
            else:
                sendchat(chat_id, "kon sopo jancok wkwk")
        except Exception as e:
            sendchat(boschatid, "error command perdin\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "absenpulang":
        try:
            if(username == "andimahathir" or username == "yatnosyarifudin"):
                filejson = open("listabsen.json",)
                listabsen = json.load(filejson)
                filejson.close()
                if(content == "today"):
                    waktu = datetime.now()
                    tanggal = waktu.strftime("%Y%m%d")
                    listabsen[tanggal] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "done"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "notyet"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                    sendchat(chat_id, "ok")
                elif len(content) == 8:
                    listabsen[content] = {
                        "pagi": {
                            "menit": randint(1, 55),
                            "status": "done"
                        },
                        "sore": {
                            "menit": randint(1, 55),
                            "status": "notyet"
                        },
                        "sikerja": {
                            "status": "notyet"
                        }
                    }
                    sendchat(chat_id, "ok")
                # else:
                #     wfh(content)
                # sendchat(chat_id, listabsen)
                with open('listabsen.json', 'w') as outfile:
                    json.dump(listabsen, outfile, indent=4)
                # sendchat(chat_id, "noted boss...")
            else:
                sendchat(chat_id, "kon sopo jancok wkwk")
        except Exception as e:
            sendchat(boschatid, "error command perdin\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "hapusabsen":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        try:
            if(username == "andimahathir" or username == "yatnosyarifudin"):
                filejson = open("listabsen.json",)
                listabsen = json.load(filejson)
                filejson.close()
                if(content == "today"):
                    waktu = datetime.now()
                    tanggal = waktu.strftime("%Y%m%d")
                    listabsen.pop(tanggal, None)
                else:
                    listabsen.pop(content, None)
                sendchat(chat_id, listabsen)
                with open('listabsen.json', 'w') as outfile:
                    json.dump(listabsen, outfile, indent=4)
                # sendchat(chat_id, "noted boss...")
            else:
                sendchat(chat_id, "kon sopo jancok wkwk")
        except Exception as e:
            sendchat(boschatid, "error command hapusabsen\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
    elif order == "cekabsen":
        
        try:
            content = content.split(" ")
            date_akhir = ""
            
            if len(content) == 1:
                content1 = content[0]
                target_date = "today"
            elif len(content) == 2:
                content1 = content[0]
                target_date = content[1]
            elif len(content) == 3:
                content1 = content[0]
                target_date = content[1]
                date_akhir = content[2]
                
            if target_date == "today":
                target_date = date.today().strftime("%d/%m/%Y")
            elif target_date == "yesterday":
                target_date = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
            elif "-" in target_date:
                deltadays = int(target_date.split("-")[1])
                target_date = (date.today() - timedelta(days = deltadays)).strftime("%d/%m/%Y")
            elif "+" in target_date:
                deltadays = int(target_date.split("+")[1])
                target_date = (date.today() + timedelta(days = deltadays)).strftime("%d/%m/%Y")
            
            if content1 == "me":
                nip = "199207292020121010"
            elif content1 == "muchlas":
                nip = "199109242020121012"
            elif content1 == "satya":
                nip = "199108082020121016"
            elif content1 == "dita":
                nip = "199104072020122018"
            elif content1 == "direktur":
                nip = "197204251992031001"
            elif content1 == "dirjen":
                nip = "196806041996031001"
            elif content1 == "chandra":
                nip = "198105082008011001"
            elif content1 == "oci":
                nip = "199608232020082001"
            elif content1 == "sarino":
                nip = "196701231986031001"
            elif content1 == "satya":
                nip = "199108082020121016"
            elif content1 == "ardi":
                nip = "199312202020121009"
            elif content1 == "ipul":
                nip = "199503082020121013"
            elif len(content1) == 18:
                nip = content1
            else:
                sendchat(chat_id, "nip salah bos")
                return
            
            Thread(target=cekabsenweb, args=(chat_id,nip,target_date,date_akhir,)).start()
            
            date_awal = datetime.strptime(target_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            if "/" in date_akhir:
                date_akhir = datetime.strptime(date_akhir, "%d/%m/%Y").strftime("%Y-%m-%d")
            Thread(target=cekabsensimpeg, args=(chat_id,nip,date_awal,date_akhir)).start()
            
        except Exception as e:
            if content1 != "system":
                sendchat(chat_id, "format tanggal dd/mm/yyyy")
                sendchat(boschatid, "error command cekabsen\n" + str(getattr(e, 'message', repr(e))))
                sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "direkturcheck":
        try:
            global direkturchecker
            if content == "disable":
                direkturchecker = False
                sendchat(boschatid, "ok")
            if content == "status":
                sendchat(boschatid, str(direkturchecker))
        except Exception as e:
            sendchat(boschatid, traceback.format_exc())
    elif order == "adios":
        try:
            if content == 199207292020121010 or content == "199207292020121010":
                sendchat(chat_id, "matamu jancok")
                return
            
            header = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'ropeg.setjen.kemendagri.go.id'
            }
            payload = {
                'keterangan': 'Anda terdeteksi menggunakan Fake GPS',
                'nip': content,
                'token': 'af9ec164748d7690c4f58021b6907d8d'
            }
            r = requests.post("https://ropeg.setjen.kemendagri.go.id/restsimpeg/api/bni_post_fakegps", data=payload)
            sendchat(chat_id, r.text)
        except Exception as e:
            sendchat(boschatid, traceback.format_exc())
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "hapusresi":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        try:
            filejson = open("listresi.json",)
            listresi = json.load(filejson)
            filejson.close()
            for resi in listresi["data"][:]:
                if resi["resi"] == content:
                    listresi["data"].remove(resi)
            with open('listresi.json', 'w') as outfile:
                json.dump(listresi, outfile, indent=4)
            sendchat(chat_id, "resi removed")
        except Exception as e:
            sendchat(boschatid, "error command hapusresi\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "turtle":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        try:
            sendchat(boschatid, "ok")
            # turtle()
            sendchat(boschatid, "done")
        except Exception as e:
            sendchat(boschatid, "error command turtle\n" + str(getattr(e, 'message', repr(e))))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "kemendagri":
        try:
            sendchat(chat_id, "pencarian data kemendagri diproses!")
            kemendagri(chat_id, content)
            sendchat(chat_id, "pencarian data kemendagri selesai!")
        except Exception as e:
            sendchat(boschatid, "error command kemendagri\n" + traceback.format_exc())
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "Gold" or order == "gold":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        try:
            global autodeera, deeradump, autoindra
            if content == "check":
                if chat_id == boschatid:
                    r = requests.get("https://mhcktr.com/deera.php?signal=C00000000000000000000"+str(datetime.timestamp(datetime.now()))+"&owner=mhtr")
                    r = requests.get("https://mhcktr.com/indra.php?signal=C00000000000000000000"+str(datetime.timestamp(datetime.now()))+"&owner=mhtr")
                    # if autodeera:
                    #     sendchat(boschatid, "autodeera on")
                    # else:
                    #     sendchat(boschatid, "autodeera off")
                    # if autoindra:
                    #     sendchat(boschatid, "autoindra on")
                    # else:
                    #     sendchat(boschatid, "autoindra off")
                    # deeradump = True
                elif chat_id == 215836367:
                    r = requests.get("https://mhcktr.com/deera.php?signal=C00000000000000000000"+str(datetime.timestamp(datetime.now()))+"&owner=surya")
                elif chat_id == 1081855255:
                    r = requests.get("https://mhcktr.com/deera.php?signal=C00000000000000000000"+str(datetime.timestamp(datetime.now()))+"&owner=rendi")
            elif content == "disable":
                #global autodeera
                autodeera = False
                sendchat(boschatid, "autodeera disabled")
            elif content == "decline":
                r = requests.get("https://mhcktr.com/deera.php?signal=D00000000000000000000"+str(datetime.timestamp(datetime.now()))+"&owner=mhtr")
                sendchat(boschatid, "ok")
            elif content == "indrabuy":
                r = requests.get("https://mhcktr.com/indra.php?signal=B00000000000000000000"+str(datetime.timestamp(datetime.now()))+"&owner=mhtr")
                if r.status_code == 200:
                    sendchat(boschatid,"indrabuy done boss")
                else :
                    sendchat(boschatid,"there is a problem, status code " + str(r.status_code))
            elif content == "indrasell":
                r = requests.get("https://mhcktr.com/indra.php?signal=S00000000000000000000"+str(datetime.timestamp(datetime.now()))+"&owner=mhtr")
                if r.status_code == 200:
                    sendchat(boschatid,"indrasell done boss")
                else :
                    sendchat(boschatid,"there is a problem, status code " + str(r.status_code))
            elif content == "indraoff":
                autoindra = False
                sendchat(boschatid, "autoindra off")
            else :
                a = 0
                content = content.replace(" ","")
                content = content.replace("\n","")
                if content[0] == "S":
                    a = 1
                    mode = "S"
                    content = content.split('SellInTheZone:')[1]
                elif content[0] == "B":
                    a = 2
                    mode = "B"
                    content = content.split('BuyInTheZone:')[1]
                # try:
                #     a = 3
                #     pricerange = content[0:9]
                #     a = 4
                #     pricerange = pricerange.replace("-", "") 
                #     a = 5
                #     stoploss = int(content.split('SL:')[1][0:4])
                #     a = 6
                #     tp1 = int(content.split('TP:')[1][0:4])
                #     a = 7
                #     tp2 = int(content.split('TP2:')[1][0:4])
                #     a = 8
                # except :
                price = content[0:4]
                a = 9
                if mode == "S":
                    a = 10
                    stoploss = int(price) + 5
                    a = 11
                    tp1 = int(price) - 2
                    a = 12
                    tp2 = int(price) - 5
                    a = 13
                    pricerange = str(price) + (str(int(price) + 2))
                    a = 14
                elif mode == "B":
                    a = 15
                    stoploss = int(price) - 5
                    a = 16
                    tp1 = int(price) + 2
                    a = 17
                    tp2 = int(price) + 5
                    a = 18
                    pricerange = str(price) + str(int(price) - 2)
                    a = 19
                    # sendchat(boschatid, mode+str(pricerange)+str(stoploss)+str(tp1)+str(tp2)+str(datetime.timestamp(datetime.now())))
                r = requests.get("https://mhcktr.com/deera.php?signal="+mode+str(pricerange)+str(stoploss)+str(tp1)+str(tp2)+str(datetime.timestamp(datetime.now()))+"&owner=all")
                if r.status_code == 200:
                    sendchat(boschatid,"done boss")
                    # r = requests.get("https://mhcktr.com/mhtrsignal.txt")
                    # sendchat(boschatid, r.text)
                else :
                    sendchat(boschatid,"there is a problem, status code " + str(r.status_code))
            # sendchat(boschatid,mode+pricerange+stoploss+tp1+tp2)
        except Exception as e:
            sendchat(chat_id, str(e) + " " + str(a))
            sendchat(boschatid, "error command gold\n" + str(getattr(e, 'message', repr(e))))
            # sendchat(chat_id, a + str(price))
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "resi":
        try:
            try:
                content1 = str(content).split(' ')[0]
                orderchar = int(len(content1)) + 1
                content2 = content[orderchar:]
            except:
                content1 = content
                content2 = ""
            if content1 == "update":
                # manualcekresi(chat_id)
                updateresi(chat_id)
            elif content1 == "force":
                filejson = open("listresi.json",)
                listresi = json.load(filejson)
                filejson.close()
                listresi["lastchecked"] = 0
                with open('listresi.json', 'w') as outfile:
                    json.dump(listresi, outfile, indent=4)
                # manualcekresi(chat_id)
            elif content1 == "list":
                filejson = open("listresi.json")
                listresi = json.load(filejson)
                filejson.close()
                for resi in listresi["data"]:
                    sendchat(boschatid, str(resi))
                sendchat(boschatid, "all done")
            else:
                filejson = open("listresi.json",)
                listresi = json.load(filejson)
                filejson.close()
                listresi["data"].append({
                    "resi": content1,
                    "chat_id": chat_id,
                    "kurir" : "",
                    "item" : str(content2),
                    "last_history": ""
                })
                listresi["lastchecked"] = 0
                with open('listresi.json', 'w') as outfile:
                    json.dump(listresi, outfile, indent=4)
                sendchat(chat_id, "Resi ditambahkan, ntar dikabarin klo ada update.")
                # updateresi()
                # addresi(content, chat_id)
        except Exception as e:
            sendchat(boschatid, traceback.format_exc())
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "chatid":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        # sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        try:
            sendchat(chat_id, chat_id)
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "ceklimit":
        try:
            sendchat(chat_id, "wait")
            result = ""
            
            for i in range(1000):
                result += "a"
            
            sendchat(chat_id, result)
        except Exception as e:
            sendchat(boschatid, traceback.format_exc())
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "generatealamat":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        # sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        try:
            lat = content.split(",")[0]
            long = content.split(",")[1]
            alamat = generatealamat(lat,long)
            alamat = alamat["results"][0]["formatted_address"]
            sendchat(chat_id, str(alamat))
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # print("wrong mantra")
    elif order == "speed":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        # sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        try:
            sendchat(chat_id, "initiate speedtesting...")
            st = Speedtest()
            servernames = []
            st.get_best_server(servernames)
            pingtime = st.results.ping
            sendchat(chat_id, "Ping : " + str(pingtime) + " ms")
            downloadspeed = st.download() / 1000000
            sendchat(chat_id, "Download : " + str(round(downloadspeed, 2)) + " Mb/s ~ " + str(round(downloadspeed/8, 2)) + " MB/s")
            uploadspeed = st.upload() / 1000000
            sendchat(chat_id, "Upload : " + str(round(uploadspeed, 2)) +
                    " Mb/s ~ " + str(round(uploadspeed/8, 2)) + " MB/s")
            result = json.loads(str(st.results).replace(
                "'", '"').replace("None", "0"))
            sendchat(chat_id, "Server : " +
                    result["server"]["sponsor"] + "\nISP : " + result["client"]["isp"])
        except Exception as e:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # sendchat(chat_id, e)
            # print("wrong mantra")
    elif order == "pvu":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        # sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        try:
            if content == "scan":
                testpvuscan = True
            elif content == "active":
                pvubot = True
                sendchat(chat_id, "scan active")
            elif content == "deactive":
                pvubot = False
                sendchat(chat_id, "scan deactive")
        except Exception as e:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # sendchat(chat_id, e)
            # print("wrong mantra")
    elif order == "restart":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        # sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        try:
            if content == "router":
                sendchat(chat_id, "restarting router...")
                restartrouter()
        except Exception as e:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # sendchat(chat_id, e)
            # print("wrong mantra")
    elif order == "private":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        # sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        try:
            content1 = str(content).split(' ')[0]
            content2 = str(content).split(content1+' ')[1]
            sendchat(content1, content2)
        except Exception as e:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # sendchat(chat_id, e)
            # print("wrong mantra")
    elif order == "download":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        # sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        try:
            if content == "marbot.py":
                files = {'document': open('marbot.py', 'rb')}
                payload = {"chat_id": chat_id}
                r = requests.post(url+'sendDocument', data=payload, files=files)
                # sendchat(boschatid, r.text)
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # sendchat(chat_id, e)
            # print("wrong mantra")
    elif order == "dumpupdate":
        # try:
        #     mycursor = mydb.cursor()
        # except Exception as e:
        #     logger(getattr(e, 'message', repr(e)))
        # sendchat(chat_id, "pencarian nama berdasarkan alamat diproses...")
        try:
            global dumpupdate
            if content == "enable":
                dumpupdate = True
            elif content == "disable":
                dumpupdate = False
            sendchat(boschatid, "ok")
        except Exception as e:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
            # sendchat(chat_id, e)
            # print("wrong mantra")
    elif order == "chatgpt" or order == "cp" or order == "gpt":
        try:
            if content == "reset":
                global marbotGPT
                marbotGPT[chat_id] = []
                sendchat(chat_id, "chat history reset")
                return
            chatGPT(chat_id, content)
        except Exception as e:
            sendchat(boschatid, traceback.format_exc())
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
    elif order == "binggpt" or order == "bing" or order == "bp":
        try:
            global bingGPT
            if chat_id not in bingGPT:
                cookies = [
                            {
                                "domain": ".microsoft.com",
                                "expirationDate": 1680844021,
                                "hostOnly": False,
                                "httpOnly": False,
                                "name": "MSCC",
                                "path": "/",
                                "sameSite": "no_restriction",
                                "secure": True,
                                "session": False,
                                "storeId": None,
                                "value": "NR"
                            },
                            {
                                "domain": "microsoftedge.microsoft.com",
                                "expirationDate": 1712293959.04993,
                                "hostOnly": True,
                                "httpOnly": False,
                                "name": "MicrosoftApplicationsTelemetryDeviceId",
                                "path": "/",
                                "sameSite": "no_restriction",
                                "secure": True,
                                "session": False,
                                "storeId": None,
                                "value": "d9201326-5ef7-4e07-8898-b799a77018e0"
                            },
                            {
                                "domain": ".microsoft.com",
                                "expirationDate": 1712293624,
                                "hostOnly": False,
                                "httpOnly": False,
                                "name": "_clck",
                                "path": "/",
                                "sameSite": None,
                                "secure": False,
                                "session": False,
                                "storeId": None,
                                "value": "16kuu1j|1|faj|0"
                            },
                            {
                                "domain": ".microsoft.com",
                                "expirationDate": 1680759427.222797,
                                "hostOnly": False,
                                "httpOnly": False,
                                "name": "MS0",
                                "path": "/",
                                "sameSite": "no_restriction",
                                "secure": True,
                                "session": False,
                                "storeId": None,
                                "value": "fd4b5b78d5c24729af2c98e35e83bd99"
                            },
                            {
                                "domain": ".microsoft.com",
                                "expirationDate": 1680844025,
                                "hostOnly": False,
                                "httpOnly": False,
                                "name": "_clsk",
                                "path": "/",
                                "sameSite": None,
                                "secure": False,
                                "session": False,
                                "storeId": None,
                                "value": "1350849|1680757625185|1|0|e.clarity.ms/collect"
                            },
                            {
                                "domain": ".microsoft.com",
                                "expirationDate": 1680844023,
                                "hostOnly": False,
                                "httpOnly": False,
                                "name": "_uetsid",
                                "path": "/",
                                "sameSite": None,
                                "secure": False,
                                "session": False,
                                "storeId": None,
                                "value": "de75e140d43811edab1a3b87f9f03edf"
                            },
                            {
                                "domain": ".microsoft.com",
                                "expirationDate": 1714453623,
                                "hostOnly": False,
                                "httpOnly": False,
                                "name": "_uetvid",
                                "path": "/",
                                "sameSite": None,
                                "secure": False,
                                "session": False,
                                "storeId": None,
                                "value": "de766540d43811eda70161c208ed0c2b"
                            },
                            {
                                "domain": ".microsoft.com",
                                "expirationDate": 1680765160.377102,
                                "hostOnly": False,
                                "httpOnly": True,
                                "name": "ak_bmsc",
                                "path": "/",
                                "sameSite": None,
                                "secure": False,
                                "session": False,
                                "storeId": None,
                                "value": "AB08449E2B0BEBD5C345CA5A96C3EFA7~000000000000000000000000000000~YAAQlkZYaBUtKE+HAQAA1S77VBOvV7FygHki6oaCycdO7rRBTAByx98NFDUtmpv8w/t/DA3bNElRcwm86wtLfosdT1J2cqXtON9bD+BKbohAWiIzgf6ZrhNHqXAndM/ohMhe07fCVsLr33vxKVC27C181hBwy5kSqlpYP1xROaZjU0eQMAJYsasC3xvlfoRjtHvED3pJRiehYIYhHwwwCSd7LnvuvzX1BiYHFmXUazUmxrpJQ5XHIchMtyQRKxKU7ymekAnA83BkO0thDlmB0UFyz14B9+bnhaYoxiNitg112/Upq6kyGVa8bs5+FnU/A6gPAU9xoEsl/5wDFtie9PvZ/VjRnOCt1eaC1LOjy3UaWiDRzB4nD0MheQdtLrcszbupMWvotND6xGdpt44="
                            },
                            {
                                "domain": ".microsoft.com",
                                "expirationDate": 1712293627.222692,
                                "hostOnly": False,
                                "httpOnly": False,
                                "name": "MC1",
                                "path": "/",
                                "sameSite": "no_restriction",
                                "secure": True,
                                "session": False,
                                "storeId": None,
                                "value": "GUID=eb733d076c304812903c35f3539a648d&HASH=eb73&LV=202304&V=4&LU=1680757626154"
                            }
                        ]
                bingGPT[chat_id] = Chatbot(cookies=cookies)
            if content == "reset":
                marbotGPT[chat_id] = []
                sendchat(chat_id, "chat history reset")
                return
            asyncio.run(BingGPT(chat_id, content))
        except Exception as e:
            sendchat(boschatid, traceback.format_exc())
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
    elif order in ['putu', 'eko', 'lord', 'jember', 'petani']:
        try:
            if order == "jember":
                if chat_id != boschatid:
                    sendchat(boschatid, str("🗣️ ") + content)
                if chat_id != 200021971:
                    sendchat(200021971, str("🗣️ ") + content)
                if chat_id != 1319466754:
                    sendchat(1319466754, str("🗣️ ") + content)
            else:
                if order == "putu":
                    target = 200021971
                elif order == "eko":
                    target = 1319466754
                elif order == "lord":
                    target = boschatid
                elif order == "petani":
                    target = -491464078
                sendchat(target, content)
        except:
            sendchat(chat_id, "mantranya salah bos, atau coba /restart wkwk")
    else:
        sendchat(chat_id, "lu ngomong apa bre?")


def pvumarketscan():
    global statusgrouppvu, testpvuscan
    ids = []
    while phoenix:
        if pvubot:
            headers = {"authorization": "Bearer Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNBZGRyZXNzIjoiMHhkNTdhNTM2YTM2NzkyZTY2ZjhmMWM3YzAzYjUzNTliZDYwMDljMjBhIiwibG9naW5UaW1lIjoxNjMyNDM2MzI0ODU5LCJjcmVhdGVEYXRlIjoiMjAyMS0wOS0xNiAxNToxOToyMSIsImlhdCI6MTYzMjQzNjMyNH0.SBaTrchtR2MghFgez-BjkFvXtHxL1xRjikaxlCjSA-A"}
            r = requests.get(
                "https://backend-farm.plantvsundead.com/get-plants-filter-v2?rarities=1,2,3&sort=latest&offset=0&limit=10&type=1", headers=headers, timeout=20)
            # sendchat(boschatid,r.text)
            if r.status_code != 200:
                sendchat(boschatid, r.status_code)
            # print(r.text)
            plants = json.loads(r.text)["data"]
            # sendchat(boschatid,plants)
            for plant in plants:
                # sendchat(boschatid,plant)
                id = plant["id"]
                price = plant["endingPrice"]
                element = plant["config"]["stats"]["type"]
                if id not in ids or testpvuscan:
                    if (element in {"fire", "metal", "wind", "electro"} and (price <= 55)) or testpvuscan:
                        # if (((penghasilan >= 10) and (price <= 55) and (element != "metal")) or ((element == "electro") and (price <= 50))) or (testpvuscan):
                        hours = plant["config"]["farm"]["hours"]
                        le = plant["config"]["farm"]["le"]
                        ids.append(id)
                        penghasilan = int(le)/int(hours)
                        physics = plant["config"]["stats"]["damagePhysics"]
                        magic = plant["config"]["stats"]["damageMagic"]
                        pure = plant["config"]["stats"]["damagePure"]
                        hp = plant["config"]["stats"]["damageHpLoss"]
                        raritycode = int(str(id)[6] + str(id)[7])
                        if raritycode == 99:
                            rarity = "Mythic"
                        elif raritycode < 99 and raritycode > 88:
                            rarity = "Rare"
                        elif raritycode > 59 and raritycode < 89:
                            rarity = "Uncommon"
                        else:
                            rarity = "Common"
                        if testpvuscan:
                            sendchat(boschatid, rarity + " - " + element.title() + "\n⚔ " + str(physics) + " ♥️ " + str(hp) + " 🔮 " + str(magic) + " 💉 " + str(pure) + "\n(" + str(le) + "/" + str(hours) + "jam ~ " + str(
                                round(hours/24, 2)) + " hari) = " + str(round(penghasilan, 2)) + "/jam\nHarga : " + str(price) + "\n\nhttps://marketplace.plantvsundead.com/offering/bundle#/plant/" + str(id))
                        else:
                            sendchat(-1001548494323, rarity + " - " + element.title() + "\n⚔ " + str(physics) + " ♥️ " + str(hp) + " 🔮 " + str(magic) + " 💉 " + str(pure) + "\n(" + str(le) + "/" + str(hours) + "jam ~ " + str(
                                round(hours/24, 2)) + " hari) = " + str(round(penghasilan, 2)) + "/jam\nHarga : " + str(price) + "\n\nhttps://marketplace.plantvsundead.com/offering/bundle#/plant/" + str(id))
                    if (price <= 6.59):
                        sendchat(boschatid, "Plant gacor founded!\nElement : " + element + "\nPenghasilan : (" + str(le) + "/" + str(hours) + ") = " + str(
                            penghasilan) + "/jam\nHarga : " + str(price) + "\n\nhttps://marketplace.plantvsundead.com/offering/bundle#/plant/" + str(id))
            if testpvuscan:
                testpvuscan = False
            # try:
            #     r = requests.get("https://backend-farm.plantvsundead.com/farm-status", headers=headers, timeout=20)
            #     if r.status_code != 200:
            #         sendchat(boschatid,r.status_code)
            #     print(r.text)
            #     statusfarm = json.loads(r.text)["data"]
            #     if statusfarm["status"] == 1:
            #         if statusgrouppvu == False:
            #             sendchat(-491464078,"waktunya login para bangsat!\ningat kalian belum balik modal!")
            #             statusgrouppvu = True
            #     else:
            #         if statusgrouppvu == True:
            #             sendchat(-491464078,"waktu habis anak kontol")
            #         statusgrouppvu = False
            # except Exception as e:
            #     sendchat(boschatid,"Error pvureminder()\n" + getattr(e, 'message', repr(e)))
            #     sendchat(boschatid,r.text)
        time.sleep(10)


def kemendagri(chat_id, content):
    
    if ";" in content:
        content = content.split(";")
        payload = {
            "text" : content[0],
            "token" : "af9ec164748d7690c4f58021b6907d8d"
        }
        r = requests.post("https://ropeg.setjen.kemendagri.go.id/restsimpeg/index.php/api/cari_android",data=payload, verify=False)
        simpegResults = json.loads(r.text)["results"]
        del content[0]
        for matcher in content:
            matches = []
            for simpegResult in simpegResults:
                values = ""
                for key, value in simpegResult.items():
                    values += str(value) + " "
                    
                if simpegResult["nip"][14] == "1":
                    values += str("laki-laki pria cowok")
                elif simpegResult["nip"][14] == "2":
                    values += str("wanita perempuan cewek")
                
                if simpegResult["kagama"] == "1":
                    values += str("islam")
                elif simpegResult["kagama"] == "2":
                    values += str("kristen protestan")
                elif simpegResult["kagama"] == "3":
                    values += str("kristen katolik")
                elif simpegResult["kagama"] == "4":
                    values += str("hindu")
                elif simpegResult["kagama"] == "5":
                    values += str("budha")
                elif simpegResult["kagama"] == "6":
                    values += str("konghuchu konghucu")
                    
                if matcher.lower() in values.lower():
                # if values.lower().find(matcher.lower()) >= 0:
                    matches.append(simpegResult)
            simpegResults = matches
        results = simpegResults
        # for match in matches:
        #     prehasil = str(match["nama"]) + " - " + str(match["nip"]) + str("\n") + str(match["njab"]) + str("\n\n")
        #     hasil = str(hasil) + str(prehasil)
    else:
    # if ";" not in content:
        payload = {
            "text" : content,
            "token" : "af9ec164748d7690c4f58021b6907d8d"
        }
        r = requests.post("https://ropeg.setjen.kemendagri.go.id/restsimpeg/index.php/api/cari_android",data=payload, verify=False)
        results = json.loads(r.text)["results"]
    if len(results) > 1:
        hasil = ""
        for i in results:
            prehasil = str(i["nama"]) + " - " + str(i["nip"]) + str("\n") + str(i["njab"]) + str("\n\n")
            hasil = str(hasil) + str(prehasil)
        sendchat(chat_id, str(hasil))
    elif len(results) == 1:
        results = results[0]
        payload = {
            "nip" : results["nip"],
            "token" : "af9ec164748d7690c4f58021b6907d8d"
        }
        r = requests.post("https://ropeg.setjen.kemendagri.go.id/restsimpeg/index.php/api/profile_android",data=payload, verify=False)
        results = json.loads(r.text)["results"]
        hasil = ""
        for k, v in results.items():
            # if k != "foto":
            hasil += str(k) + " : " + str(v) + "\n"
        
        sendchat(chat_id, hasil)
        
        
def queryDatabase(query,dictionary = True):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ktpsurabaya"
    )
    cursor = mydb.cursor(dictionary=dictionary)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return result

def getupdate():
    global update_id, testpvuscan, ipversion, killbot, phoenix
    Thread(target=autoabsen).start()
    Thread(target=updateresi).start()
    # Thread(target=notifdirekturpulang).start()
    if update_id == "":
        r = requests.get(url+'getUpdates?timeout=120', timeout=124)
    else:
        r = requests.get(url+'getUpdates?timeout=120&offset=' + str(update_id), timeout=124)
    respons = json.loads(r.text)
    if respons["result"] != [] and dumpupdate:
        dump("telegram", "-", respons)
    if respons["ok"] and respons["result"] != []:
        for i in respons["result"]:
            start = time.time()
            try:
                update_id = i["update_id"]
                text = i["message"]["text"]
                firstname = i["message"]["chat"]["first_name"]
                try:
                    sender = i["message"]["from"]["username"]
                except:
                    sender = "unknown"
                chat_id = i["message"]["chat"]["id"]
                try:
                    dump(sender, chat_id, text)
                except:
                    dump(firstname, chat_id, text)
                order = str(text).split(' ')[0].lower()
                orderchar = int(len(order)) + 1
                content = text[orderchar:]
                if sender in superAdmin + userJember:
                    if str(text) == "/kill":
                        phoenix = False
                        killbot = True
                        break
                    elif str(text) == "/restart":
                        Thread(target=sendchat, args=(chat_id, "good bye, see u soon.",)).start()
                        phoenix = False
                        break
                    elif str(text) == "/testdatabase":
                        Thread(target=command, args=(chat_id, "name", "aderusman", sender,)).start()
                        break
                    elif str(text) == "/speedtest":
                        Thread(target=command, args=(chat_id, "speed", "test", sender,)).start()
                        break
                if sender in superAdmin:
                    if order not in commandAdmin + commandJember + commandGold + commandAbsen:
                        # Thread(target=sendchat, args=(chat_id, helpTextAdmin,)).start()
                        sendchat(chat_id, helpTextAdmin)
                        extTime = time.time() - start
                        Thread(target=sendchat, args=(chat_id, extTime,)).start()
                        break
                elif sender in userJember + superAdmin:
                    if order not in commandJember:
                        Thread(target=sendchat, args=(chat_id, helpTextJember,)).start()
                        break
                elif sender in userGold:
                    if order not in commandGold:
                        Thread(target=sendchat, args=(chat_id, "mantra salah bre",)).start()
                        break
                elif sender in userAbsen:
                    if order not in commandAbsen:
                        Thread(target=sendchat, args=(chat_id, "lu ngomong apa sih anjing",)).start()
                        break
                elif sender not in zip(superAdmin, userJember, userGold, userAbsen):
                    Thread(target=sendchat, args=(chat_id, str(firstname) + " kontol",)).start()
                    Thread(target=sendvideo, args=(chat_id, "https://c.tenor.com/u9XnPveDa9AAAAAM/rick-rickroll.gif",)).start()
                    break
                Thread(target=command, args=(chat_id, order, content, sender,)).start()
            except:
                try:
                    update_id = i["update_id"]
                    caption = i["message"]["caption"]
                    sender = i["message"]["from"]["username"]
                    chat_id = i["message"]["chat"]["id"]
                    if caption == "update marbot" and sender in ("andimahathir", "yatnosyarifudin"):
                        # sendchat(chat_id, "wait...")
                        messageid = json.loads(sendchat(chat_id, "wait...").text)["result"]["message_id"]
                        file_id = i["message"]["document"]["file_id"]
                        editmessage(chat_id, messageid, "wait...\ngetting file_path...")
                        r = requests.get(url+'getFile?file_id='+file_id)
                        file_path = json.loads(r.text)["result"]["file_path"]
                        editmessage(chat_id, messageid, "wait...\ngetting file_path...\ndownloading file...")
                        # if ipversion == 4:
                        r = requests.get("https://api.telegram.org/file/bot"+botToken+'/'+file_path)
                        # elif ipversion == 6:
                        #     r = requests.get("https://149.154.167.220/file/bot"+botToken+'/'+file_path)
                        editmessage(chat_id, messageid, "wait...\ngetting file_path...\ndownloading file...\nupdating marbot...")
                        with open('marbot.py', 'wb') as f:
                            f.write(r.content)
                        editmessage(chat_id, messageid, "wait...\ngetting file_path...\ndownloading file...\nupdating marbot...\nmarbot restarting...")
                        phoenix = False
                except:
                    pass
        update_id += 1
    else:
        update_id = ""
    time.sleep(1)

try:
    print("MarBot ready...")

    r = requests.get(url+'getUpdates')

    respons = json.loads(r.text)
    if respons["ok"] and respons["result"] != []:
        for i in respons["result"]:
            try:
                update_id = i["update_id"]
                text = i["message"]["text"]
                chat_id = i["message"]["chat"]["id"]
                if str(text) == "/restart":
                    sendchat(chat_id, "hello again mathrfackr\nlast bot modified: %s" % time.ctime(os.path.getmtime("marbot.py")))
                    sendchat(boschatid, "bot restarted")
                    update_id += 1
                    r = requests.get(url+'getUpdates?offset='+str(update_id))
            except:
                update_id = i["update_id"]
                chat_id = i["message"]["chat"]["id"]
                caption = i["message"]["caption"]
                if str(caption) == "update marbot":
                    sendchat(chat_id, "hello again mathrfackr\nlast bot modified: %s" % time.ctime(os.path.getmtime("marbot.py")))
                    sendchat(boschatid, "bot restarted")
                    update_id += 1
                    r = requests.get(url+'getUpdates?offset='+str(update_id))

    # update_id = ""
    while phoenix:
        getupdate()
        time.sleep(1)
    # for thread in enumerate(): 
    #     sendchat(boschatid, thread.name)

except Exception as e:
    chat = str(traceback.format_exc())
    payload = {"chat_id": chat_id, "text": str(chat)}
    requests.post(url+'sendMessage', data=payload)
    payloaddump = {"chat_id": '-355139963', "text": "--- " + str(chat_id) + " ---\n" + str(chat)}
    requests.post(url+'sendMessage', data=payloaddump)
    time.sleep(15)
    r = requests.get(url+'getUpdates?timeout=120', timeout=124)
    respons = json.loads(r.text)
    if respons["ok"] and respons["result"] != []:
        for i in respons["result"]:
            update_id = i["update_id"]
            try:
                caption = i["message"]["caption"]
                sender = i["message"]["from"]["username"]
                chat_id = i["message"]["chat"]["id"]
                if caption == "update marbot" and sender in superAdmin:
                    file_id = i["message"]["document"]["file_id"]
                    r = requests.get(url+'getFile?file_id='+file_id)
                    file_path = json.loads(r.text)["result"]["file_path"]
                    r = requests.get("https://api.telegram.org/file/bot"+botToken+'/'+file_path)
                    with open('marbot.py', 'wb') as f:
                        f.write(r.content)
                    payload = {"chat_id": chat_id, "text": "replacing marbot"}
                    requests.post(url+'sendMessage', data=payload)
            except:
                pass
            r = requests.get(url+'getUpdates?timeout=120&offset=' + str(update_id + 1), timeout=124)
