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
    property var initialFreq : {
        return client.getFrequency() / 100000;
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
    }

    Text {
        id: title
        x: 38
        y: 37
        text: qsTr("Radio Tuner")
        font.pixelSize: 32
    }

    Text {
        id: freqText
        x: 108
        y: 197
        text: {
            var dialNumber = initialFreq / 10;
            var dialString = (dialNumber < 100) ? dialNumber.toString().substring(0, 4) : dialNumber.toString().substring(0, 5)
            return "Tuned To: " + dialString
        }

        font.pixelSize: 24
    }
    Connections {
        target: dial
        onMoved: {
            var dialNumber = (dial.value / 10)
            var dialString = (dialNumber < 100) ? dialNumber.toString().substring(0, 4) : dialNumber.toString().substring(0, 5)
            freqText.text = qsTr("Tuned To: " + dialString)
            dialNumber = parseFloat(dialString)
            console.log("The radio then dials to: " + dialNumber + "MHz")
            client.setFrequency((dialNumber * 1000000))

        }
    }
}
