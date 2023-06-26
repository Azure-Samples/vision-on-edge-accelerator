@echo off

set url=https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-5.1.2-essentials_build.zip
set zip_file_name=ffmpeg-5.1.zip
set binary_name=ffmpeg.exe
set tmp_dir=temp
set env_file_name=ffmpeg_config.env
set env_file_path=./%tmp_dir%/%env_file_name%
Set delete_temp=false
Set rtsp_server=localhost
Set opts_arguement=false

if not "%1" == "" ( call :get_options %1 %2 )
SHIFT
if %opts_arguement%==true ( 
    SHIFT
    opts_arguement=false
)
if not "%1" == "" ( call :get_options %1 %2 )
SHIFT
if %opts_arguement%==true ( 
    SHIFT
    opts_arguement=false
)
if  "%delete_temp%"=="true" (
    echo ">> Cleaning up existing %tmp_dir% folder..."
    if exist %tmp_dir% rmdir /s /q %tmp_dir%
 )


SET run_streaming=false
IF EXIST "./%tmp_dir%/%binary_name%" IF EXIST %env_file_path% SET run_streaming=true
IF "%run_streaming%"=="true" (
   CALL :start_streaming 
) else (
if not exist %tmp_dir% mkdir %tmp_dir%
echo ">> Downloading %url% to ./%tmp_dir%/%zip_file_name%"
curl %url% > ./%tmp_dir%/%zip_file_name%
echo Unzipping ./%tmp_dir%/%zip_file_name%...
tar -xf ./%tmp_dir%/%zip_file_name% -C ./%tmp_dir%/ --strip-components=1
move .\%tmp_dir%\bin\%binary_name% .\%tmp_dir%\%binary_name%
CALL :capture_user_input
CALL :start_streaming)
goto :eof

:capture_user_input
    echo ">> listing available camera devices..."
    .\%tmp_dir%\%binary_name% -list_devices true -f dshow -i dummy
    echo ">> Please type in the name (e.g. Integrated Camera) of the desired camera and press enter..."
    set /p camera_name=""
    call :trim cam_path_no_white_space %camera_name%
    echo ">> You have selected %cam_path_no_white_space%..."
    echo ">> Fetching camera resolutions..."
    echo ">> Please type in the appropriate resolution (e.g. 640x480) and press enter..."
    .\%tmp_dir%\%binary_name% -f dshow -list_options true -i video="%cam_path_no_white_space%"
    set /p res=""  
    call :trim res_no_whitespace %res%
    echo ">> Please type in the associated framerate (e.g. 30) with this resolution and press enter..."
    set /p frate=""
    call :trim framerate_no_whitespace %frate%
    echo ">> You have selected Camera:%cam_path_no_white_space% Resolution:%res_no_whitespace% Framerate:%framerate_no_whitespace%"
    CALL :write_config_file "%cam_path_no_white_space%" "%res_no_whitespace%" "%framerate_no_whitespace%" "%rtsp_server%"
    CALL :start_streaming
    exit /b

:write_config_file
    echo cam_name=%~1> %env_file_path%
    echo resolution=%~2>> %env_file_path%
    echo frame_rate=%~3>> %env_file_path%
    echo rtsp_server=%~4>> %env_file_path%
    exit /b


:start_streaming
    FOR /F "tokens=*" %%i in ('type .\%tmp_dir%\%env_file_name%') do SET %%i
    echo ">> Selected Camera:%cam_name% Resolution:%resolution% Framerate:%frame_rate% RTSPServer:%rtsp_server%"
    pause
    .\%tmp_dir%\%binary_name% -f dshow -thread_queue_size 5096 -rtbufsize 500M -i video="%cam_name%" -framerate %frame_rate% -s %resolution% -tune zerolatency -c:v libx264 -preset ultrafast -b:v 2M -rtsp_transport tcp -f rtsp rtsp://%rtsp_server%:8554/stream
    exit /b

:get_options
    if /I "%1"=="-h" goto help
    if /I "%1"=="-c" (
        set delete_temp=true
    )
    if /I "%1"=="-a" (
        set rtsp_server=%2
        set opts_arguement=true
    )
    exit /b

:help
    echo ""
    echo ""
    echo "  -c: bool: Delete temp folder and rerun script"
    echo "  -a: string: RTSP server address, default is localhost (nonmandatory)"
    echo "  -h: bool: Show this help (nonmandatory)"
    echo ""
    exit 1

:trim
    SetLocal EnableDelayedExpansion
    set Params=%*
    for /f "tokens=1*" %%a in ("!Params!") do EndLocal & set %1=%%b
    exit /b