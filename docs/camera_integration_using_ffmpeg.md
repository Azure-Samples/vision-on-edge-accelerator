# Camera integration using FFmpeg for Linux, Mac and Windows

All the scripts can be accessed from the [scripts/ffmpeg](../scripts/ffmpeg) folder. This guide mentions the steps to install, run and configure ffmpeg for all the 3 platforms mentioned in the title, which forwards the camera stream to the configured rtsp server.

The script takes in 3 input from the user:
  1. Camera path to be used by ffmpeg
  2. resolution of the selected camera
  3. frame rate associated with the live streaming.

It then runs ffmpeg to start the live streaming. All the inputs are stored in a `.env` file which along with the other configurations is stored in a `temp` folder. Each category listed below talks about the script and the input syntax in more details.

## FFmpeg script for Linux

### Dependencies
```bash
wget
v4-utils
```
If the above dependencies are not present, the script throws an error and exits immediately. Admin privileges may be needed to install these dependencies on the host machine.

### Usage
```bash
usage:
  For AMD CPU architecture:
          ./start_streaming_linux.sh [-c] [-h]
  For ARM CPU architecture:
          ./start_streaming_linux_arm.sh [-c] [-h]


configurations:
  -c            Delete the temp folder and rerun the script.
  -h            Show this help (nonmandatory) and exit.
```

### Execution

1. Open a terminal in the `scripts/ffmpeg` folder.
2. Run the script using the above mentioned `Usage` guide.

### Input Format

#### Camera Path
The script lists the available cameras. The user can select the camera by entering the corresponding name of the camera.
Example of the list of Cameras:
```bash
listing available camera devices...
bcm2835-codec-decode (platform:bcm2835-codec):
    /dev/video10
    /dev/video11
    /dev/video12
    /dev/video18
    /dev/media2

HD Webcam C525 (usb-0000:01:00.0-1.4):
    /dev/video0
    /dev/video1
    /dev/media3
```
#### Resolution

The script lists the available resolutions for the selected camera. The user can select the resolution by entering the corresponding name. The script then uses the resolution to run the ffmpeg command.
Example of the list of Resolutions:
```bash
[video4linux2,v4l2 @ 0x1f4401c0] Raw       :     yuyv422 :           YUYV 4:2:2 : 640x480 160x120 176x144 320x176 320x240 432x240 352x288 544x288 640x360 752x416 800x448 864x480 960x544 1024x576 800x600 1184x656 960x720 1280x720 1392x768 1504x832 1600x896 1280x960 1712x960 1792x1008 1920x1080
```
The `x` in the input is case sensitive which means 640x480 is correct, 640X480 is not.

#### Frame Rate

Then the script asks for the frame rate. Example of the list of Frame Rates:
```bash
[0]: 'YUYV' (YUYV 4:2:2)
        Size: Discrete 640x480
            Interval: Discrete 0.033s (30.000 fps)
            Interval: Discrete 0.042s (24.000 fps)
```

## FFmpeg script for Mac

### Dependencies
```bash
wget
```
The script checks if `wget` is installed in the system, throws an error if it's not and exits immediately.

### Usage
```bash
usage:          ./start_streaming_mac.sh [-c] [-h]


configurations:
  -c            Delete the temp folder and rerun the script.
  -h            Show this help (nonmandatory) and exit.
```
### Execution

1. Open the terminal in the `scripts/ffmpeg` folder.
2. Run the script using the above mentioned `Usage` guide.

### Input Format

#### Camera Path
The script lists the available cameras under the AVFoundation video group. The user can select the camera by entering the corresponding index. Example of the list of cameras:
```bash
[AVFoundation indev @ 0x7ff34b006a80] AVFoundation video devices:
[AVFoundation indev @ 0x7ff34b006a80] [0] FaceTime HD Camera
[AVFoundation indev @ 0x7ff34b006a80] [1] Capture screen 0
```

> **_NOTE:_**  Unlike the windows script, the input here will be the index of the camera i.e 0, 1 and not the name itself.

#### Resolution

The script lists the available resolutions for the selected camera. The user can select the resolution by entering the corresponding name. The script then uses the resolution to run the ffmpeg command. Example of the list of resolutions:
```bash
[avfoundation @ 0x7fb7de906300] Supported modes:
[avfoundation @ 0x7fb7de906300]   1920x1080@[1.000000 30.000000]fps
[avfoundation @ 0x7fb7de906300]   1280x720@[1.000000 30.000000]fps
[avfoundation @ 0x7fb7de906300]   1080x1920@[1.000000 30.000000]fps
[avfoundation @ 0x7fb7de906300]   1760x1328@[1.000000 30.000000]fps
[avfoundation @ 0x7fb7de906300]   640x480@[1.000000 30.000000]fps

```
The `x` in the input is case sensitive which means 640x480 is correct, 640X480 is not.
Note that each resolution has atleast one frame rate associated with it. The user can only input one of those frame rates in the next step.

#### Frame Rate

Input the frame rate as mentioned in the above step.

## FFmpeg script for Windows

### Usage
```bash
usage:          ./start_streaming_windows.bat [-c] [-h] [-a]


configurations:
  -c            Delete the temp folder and rerun the script.
  -h            Show this help (nonmandatory) and exit.
  -a            string: RTSP server address, default is localhost while running this in simulation mode and while running in eflow mode RTSP server address can be found using the PowerShell command Get-EflowVmAddr (nonmandatory).

```
### Execution

1. Open the PowerShell terminal in the `scripts/ffmpeg` folder.
2. Run the script using the above mentioned `Usage` guide.

### Input Format

#### Camera Path

The script lists the available cameras. The user can select the camera by entering the corresponding name(the camera devices have a prefix(video)). The script then uses this camera for ffmpeg. Example of the list of cameras:

```bash
[dshow @ 00000209d522b980] "Microsoft Camera Front" (video)
[dshow @ 00000209d522b980]   Alternative name "@device_pnp_\\?\display#int3470#4&1aaa636&0&uid13424#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\{bf89b5a5-61f7-4127-a279-e187013d7caf}"
[dshow @ 00000209d522b980] "Microsoft Camera Rear" (video)
[dshow @ 00000209d522b980]   Alternative name "@device_pnp_\\?\display#int3470#4&1aaa636&0&uid13424#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\{7c9bbcea-909c-47b3-8cf9-2aa8237e1d4b}"
[dshow @ 00000209d522b980] "OBS Virtual Camera" (video)
[dshow @ 00000209d522b980]   Alternative name "@device_sw_{860BB310-5D01-11D0-BD3B-00A0C911CE86}\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}"
```

The name of the camera should be given as it is shown in the options without the suffix (video). Its important to note that this input is case sensitive which means _Windows Front Camera_ is not the same as _windows front Camera_ also the script automatically trims the spaces at the beginning and end of the name but not in between words.

#### Resolution

The script lists the available resolutions for the selected camera. The user can type in the selected resolution. The script then uses this resolution in the ffmpeg command. Example of the list of resolutions:

```bash
[dshow @ 0000022caf9eb940]   pixel_format=yuyv422  min s=1920x1080 fps=15 max s=1920x1080 fps=30
[dshow @ 0000022caf9eb940]   pixel_format=nv12  min s=1920x1080 fps=15 max s=1920x1080 fps=30
[dshow @ 0000022caf9eb940]   pixel_format=yuyv422  min s=640x360 fps=15 max s=640x360 fps=30
[dshow @ 0000022caf9eb940]   pixel_format=nv12  min s=640x360 fps=15 max s=640x360 fps=30
[dshow @ 0000022caf9eb940]   pixel_format=yuyv422  min s=640x480 fps=15 max s=640x480 fps=30
[dshow @ 0000022caf9eb940]   pixel_format=nv12  min s=640x480 fps=15 max s=640x480 fps=30
[dshow @ 0000022caf9eb940]   pixel_format=yuyv422  min s=640x640 fps=15 max s=640x640 fps=30
[dshow @ 0000022caf9eb940]   pixel_format=nv12  min s=640x640 fps=15 max s=640x640 fps=30
```

The `x` in the input is case sensitive which means 640x480 is correct, 640X480 is not.
Note that each resolution has atleast one frame rate associated with it. The user can only input one of those frame rates in the next step.

#### Frame Rate

Input the frame rate as mentioned in the above step.


## Troubleshooting Guide

- If we select very high resolution for streaming, then based on the machine performance we may see ffmpeg throwing errors of frames getting dropped (put a screen shot). In this scenario, select a lower resolution and try again.
- If we selected an audio device instead of video, then script will throw error and exit. So we'll need to restart the process and select the right camera.
- If script exits due to the following error, then ensure that the solution is running (rtsp server) before the script is executed.
```bash
Connection to tcp://localhost:8554?timeout=0 failed: Connection refused
Could not write header for output file #0 (incorrect codec parameters ?): Connection refused
Error initializing output stream 0:0 --"
```