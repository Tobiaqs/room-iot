import broadlink, netaddr, time
from flask import Flask, jsonify, Response, jsonify, request
from os import environ

app = Flask(__name__)

RM3Device = broadlink.rm((environ["RM3_IP"], int(environ["RM3_PORT"])), netaddr.EUI(environ["RM3_MAC"]))
RM3Device.auth()

commands = {
    "stereo_cd1": "260030001e1c1e1d1d1d3b393b1c1e391e1c3b3a1e1c1e1c1e000b771e1d1e1c1e1c3b393b1c1e3a1d1d3b391e1c1e1c1e000d050000000000000000",
    "stereo_cd2": "26002c001e1c3b393b3a3b1c1e391e1c1e1c3b1c1e1d1e000b941e1c3b3a3b393b1c1e391e1c1e1d3a1d1e1c1e000d05000000000000000000000000",
    "stereo_cd3": "260030001f1c1e1c1f1b3c383c1b1f381f1c1e1c3c1b1f381f000b771e1c1f1b1f1b3c383c1c1e391f1b1f1b3c1b1f381f000d050000000000000000",
    "stereo_tape": "26001a001e1c1e1c1e1c3b1d1d3a3b391e1c1e1c1e1c1e1d1e1c1e000d050000000000000000000000000000",
    "stereo_on_off": "260030001e1c1e1c1e1c3b3a3b1c1e1c1e1c1e391e1d3a1d1e000b941e1d1f1b1f1b3b393b1c201a1e1c20381f1b3b1c1e000d050000000000000000",
    "stereo_vol_up": "26001a001e1c1e1c1e1c3b1c1e1d1e1c1e1c1e393b1c1e1c201b1e000d050000000000000000000000000000",
    "stereo_vol_down": "260018001e1c3b393b1c1e1c1e1c1e1d1e393b1c1e1c1e391e000d05",
    "stereo_stop": "26002c001e1c1d1d1e1c3b373c1e1d3a1e1c3b391e1c3b000b951e1c1e1c1e1c3b3a3a1d1e391e1c3b3a1d1d3b000d05000000000000000000000000",
    "stereo_mute": "260018001d1d3b393b1d1d1d1d1d1e1c1e1c1d3a1e1c3b3a1e000d05",
    "stereo_next": "260018001e1c1e1c201a3b393b1d1d3a3b1c201a1e1c1e1c1e000d05",
    "stereo_prev": "260016001e1c3b3a3b393b1c1e393b1c1e1d1e1c1e391e000d050000",
    "stereo_play": "26002c0021191f1c1e1c3c383c1b1f381f1c3b393c381f000b771f1b1f1b1f1b3c393b1c1f381f1b3c383c391e000d05000000000000000000000000",
    "stereo_shuffle": "260016001e1c3b3a3b393b1c1e1c1e391e1d1e1c3b1c1e000d050000",
    "stereo_sleep": "260030001e1d1d1d1e1c3b1c1e1c1e1c1e393c1c1e391e1c3b000b951e1c1e1d1e1c3b1c1e1c1e1c1e393c1c1e391e1c3b000d050000000000000000",
    "stereo_aux": "260018001e1c3b393b393b3a1f1b1e1c1e1c1e1c1e1c1e1c1e000d05",

    "tv_on_off": "26004800000128931312131213371213131213121312131213371336131313361337133613371336131213131213133613121313121313121336133713361313133613371336133713000d05",
    "tv_mute": "26004800000128931312131313361312131312131312131213351536131213371336133713361337133613131213133613121313131213121312133713351412133713361337133613000d05"
}

for k, v in commands.items():
    commands[k] = bytearray.fromhex(v)

colors = {"w": "2600500000012991151113111411121312121411131212131337133612371436141015351436143514361336143514111313131114111312131114111411133713361436133614351400053b0001294814000d050000000000000000", "b1": "26004800000128921312131114111213121314111312121214361237143514361411143613361336131213121237141213111411121313111436143514121237133614361336143514000d05", "b2": "26004800000128921312131214111213131114111312131115351436133614341610153514361336141113121212153513121411131213111436123714361411133614361435163414000d05", "b3": "26004800000127921411141114111213131114111312131115351436143513371311143613361436121313121336133614111312131115111138133713111411123714361237143614000d05", "b4": "26004c000001289213121311141113121311141112131311143614351436133713111436133613361510131213121411123714111312121214361237133613381311143613361336140009fc0a000d05000000000000000000000000", "b5": "26004800000127921213131114111312121214111312131114361336143515351510143612371336141113121336131213361312131114111336143614111436131114361336133614000d05", "r1": "26004800000127921411131114111312121314111212121315351336133614361311143613361435143615101436131114111312131114111312133613121237143515351337143514000d05", "r2": "26004800000127921312131114111312131115101312131214351337133614361311143613361435143713111411123714111312131114111312133614351412123713371336133614000d05", "r3": "26004800000127921412121215101312131114111312131115351336143514361411143613351436143613111436143612131212141113121311143612121411133613371436133614000d05", "r4": "2600500000012892131212121312131213121411131213111436133613361336151114361336133614361311141113121238131213111411131213361336143614111436123713361400053b0001274914000d050000000000000000", "r5": "2600480000012892141112131411131213111411131213111436133613361436151015341535133614361410143613111535150f141113121213143515101535141015351435143514000d05", "g1": "26004800000127921312131114111312131114121213121214361336133614361410153514361336141113361434161014111312131214111235161113121336123715351436133614000d05", "g2": "260048000001269314111212141113121311151012141212143613361336143614101436143612371411123714111237141113121312160f1237131213361411123713371435143613000d05", "g3": "26004800000128921312131114111312131114111312141114361336133613371311143415371336141113361436143513121411141113121336131213111411133614361337133614000d05", "g4": "26004800000127921312121214111312121214111213131114361237133614361510143514361336131213361411131213361312131115101336141113371337131115351336133614000d05", "g5": "26004800000127921510131214111213121214111312131115351336133614361312153513361336141113361436141114361311141113121336131213111535141114361336133614000d05", "fading_snake": "2600500000012792131213121411121313111411131213111436133614351437131114361336133614361336131214111436131114111312121214111336143614111436133613361400053b0001274913000d050000000000000000", "rgb_snake": "2600500000012892141113111511121312121411131213111436133515351535141114361336133614361336143514121336141113121212141113121212153514111436143513361400053b0001274913000d050000000000000000", "fading": "2600500000012792141112121510121314111411131212121436133613341636141015351436133613371336133614361311151012131213141112131212141113361337133613361400053b0001274913000d050000000000000000", "colorful_snake": "26004800000127921312131114111312131213121213121214361336133614361311143614351435163513361312133613121311141113121311141113361411133713371336133614000d05"}

for k, v in colors.items():
    colors[k] = bytearray.fromhex(v)

turn_on = bytearray.fromhex("260050000001289113121411141112131212160f13121311143613361335153614111436133613361436133615101311160f14111510151012131212133714351336143614351336160005390001294714000d050000000000000000")
turn_off = bytearray.fromhex("2600500000012892151014101411131213111411151013111535143513371337131115351435133614111336141113121312151011141113143614101535133614351436143514351400053b0001284814000d050000000000000000")

current_color = None
currently_on = False

def check_cookie():
    return request.cookies.get("secret") == environ["SECRET"]

def flash(color, flashes):
    global current_color

    timeout = 0.05

    if not currently_on:
        RM3Device.send_data(turn_on)
        RM3Device.send_data(turn_on)
        time.sleep(timeout)
    if current_color != color:
        RM3Device.send_data(color)
        RM3Device.send_data(color)
        time.sleep(timeout)

    RM3Device.send_data(turn_off)
    time.sleep(timeout)

    for i in range(flashes - 2):
        RM3Device.send_data(turn_on)
        time.sleep(timeout)
        RM3Device.send_data(turn_off)
        time.sleep(timeout)

    RM3Device.send_data(turn_on)
    time.sleep(timeout)

    if not currently_on:
        current_color = color
        RM3Device.send_data(turn_off)
        RM3Device.send_data(turn_off)
        time.sleep(timeout)
    elif current_color != color and current_color != None:
        RM3Device.send_data(current_color)
        RM3Device.send_data(current_color)
        time.sleep(timeout)

@app.route("/set_color/<color>", methods=["GET"])
def set_color(color):
    if not check_cookie():
        return Response("go away", mimetype="text/plain")

    global current_color, currently_on

    if color == "off":
        currently_on = False
        RM3Device.send_data(turn_off)
        return Response("done", mimetype="text/plain")
    elif color in colors:
        if not currently_on:
            currently_on = True
            RM3Device.send_data(turn_on)
        if current_color != colors[color]:
            current_color = colors[color]
            RM3Device.send_data(current_color)
    else:
        return Response("???", mimetype="text/plain")

    return Response("done", mimetype="text/plain")

@app.route("/colors", methods=["GET"])
def get_colors():
    if not check_cookie():
        return Response("go away", mimetype="text/plain")

    return jsonify(list(colors.keys()))
    
@app.route("/set_main_lights/<mode>", methods=["GET"])
def set_main_lights():
    if not check_cookie():
        return Response("go away", mimetype="text/plain")

@app.route("/special_command/stereo_set_vol/<volume>", methods=["GET"])
def stereo_vol_min(volume):
    if not check_cookie():
        return Response("go away", mimetype="text/plain")

    try:
        volume = int(volume)
    except:
        return Response("volume is not a number", mimetype="text/plain")

    volume = min(40, volume)
    volume = max(0, volume)

    # Make sure volume is down
    for i in range(42):
        RM3Device.send_data(commands["stereo_vol_down"])

    for i in range(volume):
        RM3Device.send_data(commands["stereo_vol_up"])

    return Response("done", mimetype="text/plain")

@app.route("/commands", methods=["GET"])
def get_commands():
    if not check_cookie():
        return Response("go away", mimetype="text/plain")

    return jsonify(list(commands.keys()))

@app.route("/send_command/<command>", methods=["GET"])
def send_command(command):
    if not check_cookie():
        return Response("go away", mimetype="text/plain")

    if not command in commands:
        return Response("???", mimetype="text/plain")
    
    RM3Device.send_data(commands[command])

    return Response("done", mimetype="text/plain")

@app.route("/notify_color/<color>/<flashes>", methods=["GET"])
def notify_color(color, flashes):
    if not check_cookie():
        return Response("go away", mimetype="text/plain")

    try:
        flashes = int(flashes)
    except:
        return Response("flashes is not a number", mimetype="text/plain")

    flashes = min(10, flashes)
    flashes = max(2, flashes)

    if color in colors:
        flash(colors[color], int(flashes))
        return Response("done", mimetype="text/plain")
    
    return Response("???", mimetype="text/plain")

@app.route("/notify/<thing>", methods=["GET"])
def notify(thing):
    if not check_cookie() and thing != "naomi":
        return Response("go away", mimetype="text/plain")

    if thing == "whatsapp":
        flash(colors["g1"], 2)
    elif thing == "signal":
        flash(colors["b1"], 2)
    elif thing == "naomi":
        flash(colors["r1"], 2)
    return Response("done", mimetype="text/plain")

@app.route("/wakemydyno.txt", methods=["GET"])
def wake_my_dyno():
    return Response("hello!", mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=("DEBUG" in environ), port=(int(environ["PORT"]) if "PORT" in environ else 5000), host="0.0.0.0")
