# g32-cloudfree
Prototype for receiving temperature-data via wlan without needing the otto-wilde-cloud

## Prequisites

You need to be able to manipulate dns-records within your network. Create an entry that resolves `socket.ottowilde.de` to the local machine or server where the listener will run.

*Be aware that the official app will not work anymore after creating a custom dns-record.*

## Implementation

The listener was based on the bluetooth-based esp32-implementation. Luckily the same data is send to the cloud via wifi.

This is an early experimental version, that just prints the received temperatures to the shell.

## Contribution
Thanks to JBecker for reverse-enginieering and sharing it on [grillsportverein.de](https://www.grillsportverein.de/forum/threads/otto-wilde-g32-smarthome.369079/#post-5837150).
