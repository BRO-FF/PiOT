import os, os.path
import random
import string
import time
import cherrypy
import sys
sys.path.insert(1, '/opt/projetmaster-master/')
import mac.APImysql as mac
import ip.scan_asset as scan
import ip.scan_asset_network as scanet
import ip.sendMail as mail
import graph.connexion.checkpassword as passwd
from jinja2 import Template

class Webpage(object):

    @cherrypy.expose
    def index2(self):
        html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def indexwithoutuser(self):
        html = open('connexion/indexwithoutuser.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def wrongpassword(self):
        html = open('connexion/passwdincorrect.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def login(self,username=None,password=None):
        response = passwd.checkpass(username,password)
        ipUser = cherrypy.request.remote.ip
        html = """
        <script type="text/javascript">
        setTimeout("CallButton()",5)
        function CallButton()
        {
           document.getElementById("button").click();
        }
        </script>"""
        if response == "emptyDB":
            html += '<form action="indexwithoutuser" method="post"><button hidden="hidden" id="button"></button></form>'
        elif response == False:
            html += '<form action="wrongpassword" method="post"><button hidden="hidden" id="button"></button></form>'
        elif response == True:
            passwd.setCookie(ipUser)
            html += '<form action="index" method="post"><button hidden="hidden" id="button"></button></form>'
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def enroll(self,username=None,password=None):
        response = passwd.enrollement(username,password)
        html = """
        <script type="text/javascript">
        setTimeout("CallButton()",5)
        function CallButton()
        {
           document.getElementById("button").click();
        }
        </script>"""

        if response == False:
            html += '''
            <form action="indexwithoutuser" method="post">
                <button hidden="hidden" id="button"></button>
            </form>'''
        elif response == True:
            html += '''
            <form action="index" method="post">
                <button hidden="hidden" id="button"></button>
            </form>'''
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def index(self):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            html = open('begin-connected.html','r').read()
        else:
            html = open('begin.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def scan_all(self):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            scan.scan_asset()
            scanet.scan_asset_network()
            runManage = "/opt/projetmaster-master/bash/runManage.sh"
            os.system(runManage)

            report = open('/opt/projetmaster-master/logs/report','r').read()
            report = report.splitlines()
            html = open('html.html','r').read()
            html += '''
        <section class="p-10 md-p-l5">

            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="red opacity-70 no-underline">
                                    <th scope="col">
                                    <h3>Scan Report</h3>
                                    </th>
                                </tr>
                            </thead>
                        </table>
                    </div>
                </div>
            </div>

            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="red opacity-70 no-underline">
                                    <form action="scan_all" method="post">
                                        <button class="button">Scan Asset</button>
                                    </form>
                                </tr>
                            </thead>
                        </table>
                    </div>
                </div>
            </div>

            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center content-box">
                        <div class="indigo-lightest fw-600 fs-m1">Report<br>
                            <span class="opacity-30">
                                <p>'''
            for line in report:
                html += line + "<br>"
            html += '''
                                <p>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    </body>
</html>'''
            html += "</br>"
            # html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def Scan(self, length=8):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            report = open('/opt/projetmaster-master/logs/report','r').read()
            report = report.splitlines()
            html = open('html.html','r').read()
            html += '''
        <section class="p-10 md-p-l5">
            
            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="red opacity-70 no-underline">
                                    <th scope="col">
                                    <h3>Scan Report</h3>
                                    </th>
                                </tr>
                            </thead>
                        </table>
                    </div>
                </div>
            </div>

            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="red opacity-70 no-underline">
                                    <form action="scan_all" method="post">
                                        <button class="button">Scan Asset</button>
                                    </form>
                                </tr>
                            </thead>
                        </table>
                    </div>
                </div>
            </div>

            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center content-box">
                        <div class="indigo-lightest fw-600 fs-m1">Report<br>
                            <span class="opacity-30">
                                <p>'''
            for line in report:
                html += line + "<br>"
            html += '''
                                <p>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    </body>
</html>'''
            html += "</br>"
            # html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def Manage(self):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            html = open('html.html','r').read()
            table_mac = mac.display_base('all')
            autIp = mac.authorized_ip()
            extIp = mac.display_ip()
            banIp = mac.display_ban()
            # table_mac = table_mac.replace("(","")
            # table_mac = table_mac.split("),")
            html += """
    <section id="home" class="p-10 md-p-l5">

          <div id="slider-2">
              <div class="px-1">
                <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                    <table class="table table-dark table-bordered" width="100%">
                        <thead class="thead-light">
                            <tr class="red opacity-70 no-underline">
                                <th scope="col">
                                    <h3>Authorized Devices </h3>
                                </th>
                            </tr>
                        </thead>
                    </table>
                </div>
            </div>
        </div>

          <div id="slider-2">
              <div class="px-1">
                <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                    <table class="table table-dark table-bordered" width="100%">
                        <thead class="thead-light">
                            <tr class="blue opacity-70 no-underline">
                                <th scope="col">ID</th>
                                <th scope="col">Device</th>
                                <th scope="col">Brand</th>
                                <th scope="col">IP Address</th>
                                <th scope="col">Mac Address</th>
                                <th scope="col">Up</th>
                                <th scope="col">Supprimer</th>
                            </tr>
                        </thead>
                        <tbody>"""
            for objets in table_mac:
                html += "<tr>"
                # for values in objets:
                html += '<td class="white opacity-70 no-underline">'
                html += str(objets[0])
                html += '</td>'
                html += '<td class="white opacity-70 no-underline">'
                html += str(objets[1])
                html += '</td>'
                html += '<td class="white opacity-70 no-underline">'
                html += str(objets[2])
                html += '</td>'
                html += '<td class="white opacity-70 no-underline">'
                html += str(objets[3])
                html += '</td>'
                html += '<td class="white opacity-70 no-underline">'
                html += str(objets[4])
                html += '</td>'

                try:
                    if objets[5] == 1:
                        html += '''
    <td>
        <span class="glyphicon glyphicon-trash">
            <img class="max-h-l2 w-auto" src="img/check.png">
        </span>
    </td>'''
                    else:
                        html += '''
<td>
        <span class="glyphicon glyphicon-trash">
            <img class="max-h-l2 w-auto" src="img/uncheck.png">
        </span>
</td>'''
                    html += '''
<td>
    <form action="deletemac" method="POST">
            <input type="hidden" name="name" value="''' + str(objets[0]) + '''" />
            <button><i class="fa fa-trash"></i> Trash</button>
    </form>
</td>'''
                    pass
                except Exception as e:
                    print(e)
                    pass
                html += "</tr>"
            #lien pour ajouter une mac :
            html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

          <div id="slider-2">
              <div class="px-1">
                <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                    <table class="table table-dark table-bordered" width="100%">
                        <thead class="thead-light">
                            <tr class="blue opacity-70 no-underline">
                                <th scope="col">Scan For Device</th>
                                <th scope="col">Add Device Manually</th>
                                <th scope="col">Add Mail Info</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th>
                                    <form action="scans" method="GET">
                                        <button class="button bg-white black fw-600 no-underline mx-5" type="submit">Scan</button>
                                    </form>
                                </th>
                                <th>
                                    <form action="AddMacInput" method="GET">
                                        <button class="button bg-white black fw-600 no-underline mx-5" type="submit">Manual</button>
                                    </form>
                                </th>
                                <th>
                                    <form action="AddMail" method="GET">
                                        <button class="button bg-white black fw-600 no-underline mx-5" type="submit">Email</button>
                                    </form>
                                </th>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>"""



            html += """
            <div>
            <a class="black">padding</a>
            <div>
            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="red opacity-70 no-underline">
                                    <th scope="col">
                                        <h3>External Authorization</h3>
                                    </th>
                                </tr>
                            </thead>
                        </table>
                    </div>
                </div>
            </div>
              <div id="slider-2">
                  <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                    <table class="table table-dark table-bordered" width="100%">
                        <thead class="thead-light">
                          <tr class="blue opacity-70 no-underline">
                            <th scope="col">Authorized Ip</th>
                            <th scope="col">Supprimer</th>
                          </tr>
                        </thead>
                        <tbody>"""
            for ipAdd in autIp:
                html += "<tr>"
                # for values in objets:
                html += '<td class="white opacity-70 no-underline">'
                html += str(ipAdd[1].decode('utf-8'))
                html += '</td>'

                html += '''
<td>
    <form action="delIpExt" method="POST">
            <input type="hidden" name="name" value="''' + str(ipAdd[0]) + '''" />
            <button><i class="fa fa-trash"></i> Trash</button>
    </form>
</td>'''
                html += "</tr>"
            html += "</tbody></table></div></div></div>"
            html += """
            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="blue opacity-70 no-underline">
                                    <th scope="col">Add New External Public Ip</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th>
                                        <form action="AddIp" method="GET">
                                            <button class="button bg-white black fw-600 no-underline mx-5" type="submit">Add</button>
                                        </form>
                                    </th>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div>
            <a class="black">padding</a>
            <div>"""

            if banIp != False:
                ## Ban Access
                html += """
            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="red opacity-70 no-underline">
                                    <th scope="col">
                                        <h3>Ban External Ip</h3>
                                    </th>
                                </tr>
                            </thead>
                        </table>
                    </div>
                </div>
            </div>
            <div id="slider-2">
                <div class="px-1">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="blue opacity-70 no-underline">
                                    <th scope="col">External Ip Connection</th>
                                    <th scope="col">Status</th>
                                    <th scope="col">Referer</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                        <tbody>"""
                
                for banAddr in banIp:
                    html += "<tr>"
                    # for values in objets:
                    html += '<td class="white opacity-70 no-underline">'
                    html += str(banAddr[1].decode('utf-8'))
                    html += '</td>'
                    html += '<td class="white opacity-70 no-underline">'
                    html += str(banAddr[2].decode('utf-8'))
                    html += '</td>'
                    html += '<td class="white opacity-70 no-underline">'
                    html += str(banAddr[3].decode('utf-8'))
                    html += '</td>'

                    html += '''
            <td>
            <form action="unBlockIpExt" method="POST">
                <input type="hidden" name="IP" value="''' + str(banAddr[1].decode('utf-8')) + '''" />
                <button><i class="fa fa-trash"></i> Unban</button>
            </form>
            </td>'''

                html += "</tbody></table></div></div></div>"
            ## External access
            html += """
                  <div id="slider-2">
                      <div class="px-1">
                        <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                            <table class="table table-dark table-bordered" width="100%">
                                <thead class="thead-light">
                                    <tr class="blue opacity-70 no-underline">
                                        <th scope="col">External Ip Connection</th>
                                        <th scope="col">Status</th>
                                        <th scope="col">Referer</th>
                                        <th scope="col">Action</th>
                                    </tr>
                                </thead>
                                <tbody>"""
            if extIp != False:
                for extAddr in extIp:
                    if extAddr[2].decode('utf-8') != "Harmless":
                        html += "<tr>"
                        # for values in objets:
                        html += '<td class="white opacity-70 no-underline">'
                        html += str(extAddr[1].decode('utf-8'))
                        html += '</td>'
                        html += '<td class="white opacity-70 no-underline">'
                        html += str(extAddr[2].decode('utf-8'))
                        html += '</td>'
                        html += '<td class="white opacity-70 no-underline">'
                        html += str(extAddr[3].decode('utf-8'))
                        html += '</td>'

                        html += '''
            <td>
            <form action="blockIpExt" method="POST">
                <input type="hidden" name="IP" value="''' + str(extAddr[1].decode('utf-8')) + '''" />
                <button><i class="fa fa-trash"></i> Block</button>
            </form>
            </td>'''
            html += "</tr>"
            html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>
        <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    </body>
</html>"""
            # html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()


    @cherrypy.expose
    def deletemac(self, name=None):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            mac.delete_mac(name)
            html = open('html.html','r').read()
            html += "<h1 class='white opacity-70 no-underline'>Adresse supprimé</h1>"
            html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def delIpExt(self, name=None):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            mac.delete_ip(name)
            html = open('html.html','r').read()
            html += "<h1 class='white opacity-70 no-underline'>Adresse supprimé</h1>"
            html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()
   
    @cherrypy.expose
    def blockIpExt(self, IP=None):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            html = open('html.html','r').read()
            if mac.block_ip(IP):
                html += "<h1 class='white opacity-70 no-underline'>Adresse blocked</h1>"
                html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
                html += open('footer.html','r').read()
            else:
                html += "<h1 class='white opacity-70 no-underline'>ERROR " + IP + " </h1>"
                html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
                html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def unBlockIpExt(self, IP=None):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            html = open('html.html','r').read()
            if mac.unblock_ip(IP):
                html += "<h1 class='white opacity-70 no-underline'>Adresse unblocked</h1>"
                html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
                html += open('footer.html','r').read()
            else:
                html += "<h1 class='white opacity-70 no-underline'>ERROR " + IP + " </h1>"
                html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
                html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()


    @cherrypy.expose
    def AddIp(self, Add=None):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            html = open('html.html','r').read()
            html +=  open('Manage/AddIP.html','r').read()
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def addIPExt(self, IP=None):
        #mac.delete_mac(name)
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            mac.authorize_ip(IP)
            html = open('html.html','r').read()
            html += '<form action="index" method="post"><button type="Submit">retour à l\'accueil</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def AddMail(self):
        #mac.delete_mac(name)
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            html = open('html.html','r').read()
            html += open('Manage/AddMail.html','r').read()
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def AddMac(self, MAC=None):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            mac.add_mac(MAC)
            html = open('html.html','r').read()
            html += "<h2 class='white opacity-70 no-underline' >La machine avec l'adresse mac : "+MAC+" à bien été ajoutée</h2>"
            html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def AddMacInput(self):
        #mac.delete_mac(name)
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            html = open('html.html','r').read()
            html += open('Manage/FormAddMac.html','r').read()
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def AddIp2(self, IP=None):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            mac.add_ip(IP)
            html = open('html.html','r').read()
            html += "<h2 class='white opacity-70 no-underline' >La machine avec l'adresse mac : "+IP+" à bien été ajoutée</h2>"
            html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def config_mail(self,mailFrom=None,mailTo=None,appPass=None,shodanPass=None):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            mac.setup_send_mail(mailFrom, mailTo, appPass, shodanPass)
            html = open('html.html','r').read()
            html += "<h2 class='white opacity-70 no-underline' >L'adresse mail à bien été ajoutée</h2>"
            html += '<form action="Manage" method="post"><button type="Submit">retour</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def scans(self):
        ipUser = cherrypy.request.remote.ip
        if passwd.readCookie(ipUser):
            html = open('html.html','r').read()
            table_mac = mac.display_base('mac')

            command = "zgrep DHCPACK /var/log/dhcpd.log | cut -d ' ' -f11 | sort -u | grep -i '[0-9A-F]\{2\}\(:[0-9A-F]\{2\}\)\{5\}'"
            
            list_mac = os.popen(command).read()
            list_mac = list_mac.split('\n')
            del list_mac[-1]

            result = list(set(list_mac) - set(table_mac))

            # result = [i for i, j in zip(list_mac, base_mac) if i != j]

            html += """
        <section id="home" class="p-10 md-p-l5">

            <div id="slider-2">
                <div class="px-3">
                    <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center content-box">
                        <table class="table table-dark table-bordered" width="100%">
                            <thead class="thead-light">
                                <tr class="blue opacity-70 no-underline">
                                <th scope="col">Device</th>
                                <th scope="col">Mac Address</th>
                                <th scope="col">Ajouter</th>
                                </tr>"""

            for addrMac in result:
                command2 = "zgrep 'DHCPACK' /var/log/dhcpd.log | grep '" + addrMac + "' | awk '{print $11}' | sort -u | head -1 | tr -d \"\n\" | tr -d '()'"
                device = os.popen(command2).read()
                html += "<tr>"
                # for values in objets:
                html += '<td class="white opacity-70 no-underline">'
                html += str(device) + '<br>'
                html += '</td>'
                html += '<td class="white opacity-70 no-underline">'
                html += str(addrMac) + '<br>'
                html += '</td>'
                html += '''
<td>
    <form action="AddMac" method="POST">
            <input type="hidden" name="MAC" value="''' + str(addrMac) + '''" />
            <button class="btn"><i class="fa fa-trash"></i> Add Mac</button>
    </form>
</td>'''
                html += '</td>'
                html += '</thead><tbody>'

            out = os.popen('ip neigh').read().splitlines()
            for line in out:
                ip = line.split(' ')[0]
                mac2 = line.split(' ')[4]
                h = os.popen('host {}'.format(ip)).read()
                hostname = h.split(' ')[-1]
                size = len(hostname)
                hostname = hostname[:size - 2]
                if hostname != "3(NXDOMAIN":
                    html += "<tr>"
                    # for values in objets:
                    html += '<td class="white opacity-70 no-underline">'
                    html += str(hostname) + '<br>'
                    html += '</td>'
                    html += '<td class="white opacity-70 no-underline">'
                    html += str(mac2) + '<br>'
                    html += '</td>'
                    html += '''
    <td>
        <form action="AddMac" method="POST">
                <input type="hidden" name="MAC" value="''' + str(mac2) + '''" />
                <button class="btn"><i class="fa fa-trash"></i> Add Mac</button>
        </form>
    </td>'''
                    html += '</td><tr>'
                    html += '</thead></tbody>'
                    html += """    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
</body>
</html>"""
            # html += open('footer.html','r').read()
        else:
            html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on':'True',
            'tools.staticdir.dir':'static'
        },
        '/img':{
            'tools.staticdir.on':'True',
            'tools.staticdir.dir':'img'
                }
    }
    server_config={
        'server.socket_host': '192.168.1.38'
        #'server.socket_port':443,
        #'server.ssl_module':'builtin',
        #'server.ssl_certificate':'/root/keys/cert.pem',
        #'server.ssl_private_key':'/root/keys/privkey.pem'
    }
    cherrypy.config.update(server_config)
    webapp = Webpage()
    cherrypy.quickstart(webapp, '/', conf)
