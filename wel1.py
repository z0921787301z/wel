# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse

botStart = time.time()
cl = LINE("oagdaoke@itymail.com","djry9420")
print("機器壹登入成功")
print("[ 登錄系統 ]成功(  -᷄ω-᷅ )")
print("登入所花時間為"+str(format_timespan(time.time())))

gp = json.load(codecs.open("group.json","r","utf-8"))
read = json.load(codecs.open("read.json","r","utf-8"))
settings = json.load(codecs.open("temp.json","r","utf-8"))
ban = json.load(codecs.open("ban.json","r","utf-8"))
print("機器壹登入成功")
print("[ 登錄系統 ]成功(  -᷄ω-᷅ )")
print("登入所花時間為"+str(format_timespan(time.time())))
print("機器壹登入成功")
#------------------------------------------------------------------------------------------------------------------------------------------
def restartBot():
    print ("[ 提醒 ] 機器重啟中")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        json.dump(gp, codecs.open('group.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(settings, codecs.open('temp.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(read, codecs.open('read.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)                                  
    except Exception as error:
        logError(error)
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
#------------------------------------------------------------------------------------------------------------------------------------------
def helpmessage():
    helpMessage = """🔥  〘弑神 戰爭〙   🔥
🔥add_wc 新增歡迎詞
🔥del_wc 刪除歡迎詞
🔥wc 看歡迎詞
🔥sn 新增已讀點
🔥r 查詢已讀
🔥tag@數量 重複標記
🔥 mid@ 記查詢mid
🔥 test 看機器
🔥 sp 詢速度
🔥 踢@ 標踢人
🔥 歡迎退 機器退出群組"""
    return helpMessage
wait = {
    "op": False
}
def lineBot(op):
    try:
        if op.type == 5:
            cl.findAndAddContactsByMid(op.param1) #自動加好友
            cl.sendMessage(op.param1, "你好 {} 謝謝你加我為好友 ε٩(๑> ₃ <)۶з \n此機器為歡迎機器人 \n有興趣可以私以下友資購買".format(str(cl.getContact(op.param1).displayName)))
            cl.sendMessage(op.param1, None, contentMetadata={'mid': 'u56d30ff9392a9dddbe7fcdec518d1894'}, contentType=13)
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            if clMID in op.param3:
                if op.param2 in ban["owners"] or op.param2 in ban["admin"]:
                    cl.acceptGroupInvitation(op.param1)
        if op.type == 60:
            if op.param2 not in ban['bot']:
                if op.param1 not in ban['wel']:
                    try:
                        arrData = ""
                        text = "%s " %('你好~~')
                        arr = []
                        mention = "@x "
                        slen = str(len(text))
                        elen = str(len(text) + len(mention) - 1)
                        arrData = {'S':slen, 'E':elen, 'M':op.param2}
                        arr.append(arrData)
                        text += mention + '!!歡迎加入群組!!!!'
                        cl.sendMessage(op.param1,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                    except Exception as error:
                        print(str(error))
                else:
                    cl.sendMessage(op.param1, "@bug"+ban['wel'][op.param1],contentMetadata={'MENTION':'{"MENTIONEES":['+'{"S":"0","E":"4","M":'+json.dumps(op.param2)+'}'+']}'})
        if op.type == 24:
            print ("[ 24 ] 離開群組")
            if clMID in op.param3:
                cl.leaveRoom(op.param1)
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
            if msg.contentType == 13:
                if wait["op"] == True:
                    msg.contentType = 0
                    contact = cl.getContact(msg.contentMetadata["mid"])
                    game = (msg.contentMetadata["mid"])
                    midd = (msg.contentMetadata["mid"])
                    ret_ = "使用者名稱 ：{}".format(contact.displayName)
                    ret_ += "\n使用者MId : {}".format(msg.contentMetadata["mid"])
                    cl.sendMessage(msg.to, str(ret_))
            if sender in ban["admin"] or sender in ban["owners"]:
                if text.lower() =='test':
                    cl.sendMessage(to,"運行中......")
                elif text.lower() == 'speed':
                    start = time.time()
                    cl.sendMessage(to, "計算中...")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)))
                elif text.lower () == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                elif text.lower() =='歡迎退':
                    cl.leaveGroup(msg.to)
                elif text.lower().startswith("踢 "):
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        if target in ban["owners"]:
                            pass
                        else:
                            try:
                                cl.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += "" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("add_wc"):
                    list_ = msg.text.split(":")
                    if to not in ban['wel']:
                        try:
                            ban['wel'][to] = list_[1]
                            with open('ban.json', 'w') as fp:
                                json.dump(ban, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[提示]\n成功設置群組歡迎訊息\n歡迎訊息: " + list_[1])
                        except:
                            cl.sendMessage(to, "[ERROR]\n設置群組歡迎訊息失敗!!!")
                    else:
                        cl.sendMessage(to, "[ERROR]\n群組歡迎訊息已存在!!!")
                elif msg.text.lower().startswith("renew_wc"):
                    list_ = msg.text.split(":")
                    if to in ban['wel']:
                        try:
                            del ban['wel'][to]
                            ban['wel'][to] = list_[1]
                            with open('ban.json', 'w') as fp:
                                json.dump(ban, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[提示]\n成功更新群組歡迎訊息\n歡迎訊息: " + list_[1])
                        except:
                            cl.sendMessage(to, "[ERROR]\n更新群組歡迎訊息失敗!!!")
                    else:
                        cl.sendMessage(to, "[ERROR]\n你正在更新不存在的歡迎訊息!!!")
                elif text.lower() == ("del_wc"):
                    if to in ban['wel']:
                        try:
                            del ban['wel'][to]
                            with open('ban.json', 'w') as fp:
                                json.dump(ban, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[提示]\n成功刪除群組歡迎訊息")
                        except:
                            cl.sendMessage(to, "[ERROR]\n刪除群組歡迎訊息失敗!!!")
                    else:
                        cl.sendMessage(to, "[ERROR]\n你正在刪除不存在的歡迎訊息!!!")
                elif text.lower() == 'wc':
                    if to in ban['wel']:
                        cl.sendMessage(to, ban['wel'][to])
                    else:
                        cl.sendMessage(to, "[提示]\n使用預設群組歡迎訊息中!!!")
                elif text.lower() == 'sn':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                cl.sendMessage(msg.to,"已讀點已開始")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            cl.sendMessage(msg.to, "設定已讀點:\n" + readTime)
                elif text.lower() == 'sf':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        cl.sendMessage(msg.to,"已讀點已經關閉")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                                pass
                        cl.sendMessage(msg.to, "刪除已讀點:\n" + readTime)
                elif text.lower() == 'sr':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        cl.sendMessage(msg.to, "重置已讀點:\n" + readTime)
                    else:
                        cl.sendMessage(msg.to, "已讀點未設定")
                elif text.lower() == 'r':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            cl.sendMessage(receiver,"[ 已讀者 ]:\n沒有")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = cl.getContacts(chiya)
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ 已讀者 ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ 已讀時間 ]: \n" + readTime
                        try:
                            cl.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (str(error))
                        pass
                    else:
                        cl.sendMessage(receiver,"已讀點未設定")
                elif msg.text.lower().startswith("tag "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    c  = msg.text.split(" ")
                    try:
                        c = int(c[-1])
                        for c in range(c):
                            sendMessageWithMention(to, inkey)
                    except:
                        sendMessageWithMention(to, inkey)
                elif text.lower().startswith("joinall:https://line.me/r/ti/g/"):
                    ticket_id = text[31:]
                    group = cl.findGroupByTicket(ticket_id)
                    cl.acceptGroupInvitationByTicket(group.id,ticket_id)
                    cl.updateGroup(group)
                    cl.sendMessage(to,"機器成功進入 {} !!".format(group.name))
                elif text.lower().startswith("gjoin "):
                    try:
                        gid = cl.getGroupIdsJoined()[int(text[6:])-1]
                    except:
                        cl.sendMessage(to,"無法正常執行")
                        return
                    try:
                        G = cl.getGroupWithoutMembers(gid)
                        if G.preventedJoinByTicket == True:
                            G.preventedJoinByTicket = False
                            cl.updateGroup(G)
                        cl.sendMessage(to,"https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(gid))))
                    except:
                        cl.sendMessage(to,"未找到群組")
                elif text.lower() == 'lg':
                        groups = cl.getGroupIdsJoined()
                        ret_ = "[群組列表]"
                        no = 0 + 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n[總共 {} 個群組]".format(str(len(groups)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower().startswith("add "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey not in ban["admin"]:
                        ban["admin"].append(str(inkey))
                        cl.sendMessage(to, "已獲得權限！")
                    else:
                        cl.sendMessage(to,"already")
                elif text.lower().startswith("del "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey in ban["admin"]:
                        ban["admin"].remove(str(inkey))
                        cl.sendMessage(to, "已取消權限！")
                    else:
                    	cl.sendMessage(to,"user is not in admin")
                elif text.lower() == 'rebot':
                    cl.sendMessage(to, "重新啟動中...")
                    cl.sendMessage(to, "重啟成功")
                    restartBot()
                elif msg.text.lower().startswith("gbc:"):
                    bctxt = text.replace("gbc:","")
                    n = cl.getGroupIdsJoined()
                    for manusia in n:
                        cl.sendMessage(manusia,bctxt)
        if op.type == 55:
            print ("[ 55 ] 通知讀取消息")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                    pass
            except:
                pass
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                        cl.log()
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = cl.getContact(sender)
                                    sendMessageWithMention(to, contact.mid)
                                    cl.sendMessage(to, "安安你好,我是歡迎機器人,有事請找主人")
                                    time.sleep(0.5)
                                    cl.sendContact(op.param1, "u56d30ff9392a9dddbe7fcdec518d1894")
                                break
    except Exception as error:
        logError(error)
def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
