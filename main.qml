import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.3

Window {
    visible: true
    width: 640
    height: 480
    property alias freqText: freqText
    property alias dial: dial
    title: qsTr("Radio Tuner")
    property var initialFreq : 0

    Connections {
        target: dial
        onMoved: {
            var dialNumber = (dial.value / 10)
            var dialString = (dialNumber < 100) ? dialNumber.toString().substring(0, 4) : dialNumber.toString().substring(0, 5)
            if (client.isConnected()) {
                freqText.text = qsTr("Tuned To: " + dialString)
                dialNumber = parseFloat(dialString)
                console.log("The radio then dials to: " + dialNumber + "MHz")
                client.setFrequency((dialNumber * 1000000))

            }
        }
    }

    Text {
        id: title
        x: 38
        y: 37
        text: qsTr("Radio Tuner")
        font.pixelSize: 32
    }



    TextField {
        id: hostname
        x: 66
        y: 112
        text: qsTr("Host Name / IP Address of Radio")
    }

    TextField {
        id: port
        x: 66
        y: 158
        text: qsTr("Port")
    }

    Button {
        id: connectBtn
        x: 66
        y: 214
        text: qsTr("Connect")
        onClicked: {
            connDetails.text = "";
            connDetails.visible = false;
            var hostnameVal = hostname.text;
            var portVal = parseInt(port.text);
            if (Number.isNaN(portVal) && portVal > 0) {
                connDetails.text = "Port value must be a positive number.";
                connDetails.visible = true;
                return;
            }
            client.connect(qsTr(hostnameVal), portVal);
            // Ideally we would check for success here... But for now assume
            hostname.visible = false; port.visible = false; connectBtn.visible = false;
            dial.visible = true; freqText.visible = true;

            // Display initial frequency
            initialFreq = client.getFrequency() / 100000;
            var dialNumber = initialFreq / 10;
            var dialString = (dialNumber < 100) ? dialNumber.toString().substring(0, 4) : dialNumber.toString().substring(0, 5);
            freqText.text =  "Tuned To: " + dialString;
            dial.value = initialFreq;
        }
    }


    Text {
        id: connDetails
        x: 66
        y: 271
        width: 116
        height: 27
        text: qsTr("Connection Details")
        font.pixelSize: 12
        visible: false
    }


    Text {
        id: freqText
        x: 108
        y: 197
        text: ""
        font.pixelSize: 24
        visible: false
    }



    Dial {
        id: dial
        x: 74
        y: 248
        font.pointSize: 10
        stepSize: 1
        to: 1080
        from: 875
        value: initialFreq
        visible: false
    }



}
