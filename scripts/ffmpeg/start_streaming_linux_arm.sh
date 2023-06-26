#!/bin/bash

url="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz"
zip_file_name=ffmpeg-5.1.tar.xz
tmp_dir="temp"
env_file_path="./$tmp_dir/ffmpeg_config.env"

## Usage
usage() {
    echo ""
    echo ""
    echo "  -c: bool: Delete temp folder and rerun script"
    echo "  -h: bool: Show this help (nonmandatory)"
    echo ""
    exit 1
}

check_v4l_package()
{
        REQUIRED_PKG=("wget" "v4l-utils")
        for PKG in "${REQUIRED_PKG[@]}"; do
            echo ">> Checking for $PKG"
            if ! dpkg -s "${PKG}" >/dev/null 2>&1; then
                echo ">> No $PKG found. Please install package $PKG to run this script..."
                exit 1
            else
                echo ">> ok. $PKG is installed."
            fi
        done
}

write_config_file()
{
    {
       echo ""
       echo cam_path="$1"
       echo resolution="$2"
       echo frame_rate="$3" 
    } >> $env_file_path
}

capture_user_input()
{
    echo listing available camera devices...
    v4l2-ctl --list-devices
    echo ">> Please type in the path of the desired camera and press enter..."
    read -r cam_path
    cam_path_no_whitespace="$(echo "${cam_path}" | tr -d '[:space:]')"
    echo ">> You have selected $cam_path_no_whitespace..."
    echo ">> Fetching supported resolutions for this device..."
    ./$tmp_dir/ffmpeg -f v4l2 -list_formats all -i "$cam_path_no_whitespace"
    echo ">> Please type in the appropriate RAW resolution (e.g. 640x480) and press enter..."
    read -r res
    res_no_whitespace="$(echo "${res}" | tr -d '[:space:]')"
    echo ">> Fetching supported framerate for this device..."
    v4l2-ctl --list-formats-ext -d "$cam_path_no_whitespace"
    echo ">> Please type in the highest framerate (e.g. 30) associated with this resolution and press enter..."
    read -r frate
    framerate_no_whitespace="$(echo "${frate}" | tr -d '[:space:]')"
    echo ">> You have selected Camera:$cam_path_no_whitespace Resolution:$res_no_whitespace Framerate:$framerate_no_whitespace"
    write_config_file "$cam_path_no_whitespace" "$res_no_whitespace" "$framerate_no_whitespace"
}

start_streaming()
{
    echo ">> Loading configurations..."
    set -o allexport
   # shellcheck source=/dev/null
    . $env_file_path
    set +o allexport
    # shellcheck disable=SC2154
    echo ">> Selected Camera:$cam_path Resolution:$resolution Framerate:$frame_rate"
    read -r -p ">> Press enter to start streaming..." </dev/tty
    ./$tmp_dir/ffmpeg -f v4l2 -framerate "$frame_rate" -s "$resolution" -i "$cam_path" \
    -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -probesize 6M \
    -f rtsp -rtsp_transport tcp rtsp://localhost:8554/stream
}


delete_temp="false"
while getopts "ch" OPTKEY; do
  case $OPTKEY in
    c)
        delete_temp="true"
        ;;
    h)
        usage
        ;;
    \?)
        logger "ERROR: Invalid option: -$OPTARG" >&2
        usage
        ;;
  esac
done

if [ "$delete_temp" = "true" ];
then
    echo ">> Cleaning up existing $tmp_dir folder..."
    rm -rf "$tmp_dir"
fi

if [ -e ./$tmp_dir/ffmpeg ] && [ -e $env_file_path ]
then
    start_streaming
else
    mkdir -p $tmp_dir
    check_v4l_package
    echo downloading $url
    wget -nc $url -O ./$tmp_dir/$zip_file_name
    echo Unzipping $zip_file_name...
    tar -xf ./$tmp_dir/$zip_file_name -C ./$tmp_dir/ --strip-components 1
    capture_user_input
    start_streaming
fi
