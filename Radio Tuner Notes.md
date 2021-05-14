# Radio Tuner Notes

This is how frequencies in the FM spectrum are delegated

| Label     | Frequency |
| --------- | --------- |
| Min       | 87.5 MHz  |
| Max       | 108.0 MHz |
| Step Size | 100 KHz   |

Since we cannot represent these values in the UI (using the dial element), we will instead use these values and multiply by $10^5$

| Label     | Frequency |
| --------- | --------- |
| Min       | 875       |
| Max       | 1080      |
| Step Size | 1         |

## Message Format
I think I would like to implement the GNU-Radio Script as a client server application that binds to some `localhost` port and can operate with the following messages

| Message Format | Description                                                |
| -------------- | ---------------------------------------------------------- |
| ?VER;          | Outputs the current version of the server                  |
| ?STATUS;       | Gets the status of the program                             |
| ?FREQ;         | Queries the frequency that the program is currently set at |
| :FREQ=%f;      | Sets the frequency according to the float %f               |
| :QUIT;         | Shuts down the server                                      |

To test out the server

```bash
telnet localhost 65432
```



## BUGS/ENHANCEMENTS`

**Bug Fix:** Investigate different event handlers because the one that's currently used will send too many frequency set messages over to the server. (Maybe one that's like "when you release the dial...")

**Feature Request:** Favorite radio stations section

**Enhancement:** Listen again once the client closes the connection **[FIXED]**

**Enhancement:** Allow multiple connections to the socket and have the server handle it appropriately

**Enhancement:** Probably should more intelligently receive the number of bytes as opposed to setting it to an arbitrarily high number.

**Enhancement:** Maybe use local sockets? (Nah, this will prevent me from having the Pi contain the radio and controlling from my laptop) **[INVALID]**

**Bug Fix:** Send out full number instead of scientific notation. **[Not Needed]**

**Bug Fix:** Include appropriate error messages for when the client can't connect.

**Bug Fix:** Kick the client back to the connect screen when it disconnects.

## Connect Screen

In this screen the user can input the `IP address` and `Port` that the SDR server is hosted on.

From there, it will confirm if it can connect successfully and if so, it will present the dial screen.

There should be some sort of notification if the client loses connection. Maybe popping them back up into the connect screen.

## Sending Audio Over the Network

This requires the UDP Sink box in GNU Radio. Make sure you set the type to `float`.

To hear the output do the following command:

```bash
netcat -ul address port | aplay -c num_channels -t raw -r sample_rate -f FLOAT_LE -
```

This tells netcat to listen to UDP on localhost:port and play it with ALSA with the above settings

My current configuration

| Name               | Value         |
| ------------------ | ------------- |
| Address            | x.x.x.x       |
| Port               | 7654          |
| Number of Channels | 1             |
| Sample Rate        | 48000         |
| Sample Type        | Float         |
| Endiness           | Little Endian |

### Compressing Audio

Command to convert the raw input stream into a ogg stream in standard output with a bitrate limited to 32 kb/s

```bash
ffmpeg -f f32le -ar 48k -ac 1 -i pipe:0 -f ogg -ab 32k pipe:1
```



## TODO

So we should have the GNURadio program still act as a server to be able to change channels, but this time write the raw audio to a file descriptor from which ffmpeg grabs and compresses it to an ogg stream that gets transmitted over the network.

Current command:

```bash
ffmpeg -f f32le -ar 48k -ac  1 -i pipe:0 -f ogg -ab 32k pipe:1 < raw_audio_pipe | nc -l 127.0.0.1 6003
```

Grab audio from named pipe that gnuradio is outputting to, then convert it to ogg and compress it with a 32k bitrate and then send that audio over the network.



**TODO:** Convert the gnuradio blocks program to be a server again