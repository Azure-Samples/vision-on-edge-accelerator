#!/bin/bash
url="https://evermeet.cx/ffmpeg/ffmpeg-5.1.zip"
zip_file_name=ffmpeg-5.1.zip
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

check_for_packages()
{
    echo "Checking if wget is installed..."
    if test ! "$(which wget)"; then
        echo ">> No wget found. Please install package wget to run this script..."
        exit 1
    else
        echo "Installed. Ok"
    fi
}

write_config_file()
{
    {
       echo ""
       echo cam_index="$1"
       echo resolution="$2"
       echo frame_rate="$3" 
    } >> $env_file_path
}

capture_user_input()
{
    echo $zip_file_name already present!
    echo listing available camera devices...
    ./$tmp_dir/ffmpeg -f avfoundation -list_devices true -i ''
    echo ">> Please type in the index of the desired camera and press enter..."
    read -r cam_index
    cam_index_no_whitespace="${cam_index//[[:space:]]/}"
    echo ">> You have selected $cam_index_no_whitespace..."
    echo ">> Fetching camera resolutions..."
    ./$tmp_dir/ffmpeg -f avfoundation -i "$cam_index_no_whitespace"
    echo ">> Please type in the appropriate resolution (e.g. 640x480) and press enter..."
    read -r res
    res_no_whitespace="${res//[[:space:]]/}"
    echo ">> Please type in the associated framerate (e.g. 30) with this resolution and press enter..."
    read -r frate
    framerate_no_whitespace="${frate//[[:space:]]/}"
    echo ">> You have selected Camera:$cam_index_no_whitespace Resolution:$res_no_whitespace Framerate:$framerate_no_whitespace"
    write_config_file "$cam_index_no_whitespace" "$res_no_whitespace" "$framerate_no_whitespace"
}

start_streaming()
{
    echo ">> Loading configurations..."
    set -o allexport
    # shellcheck source=/dev/null
    source $env_file_path
    set +o allexport
    # shellcheck disable=SC2154
    echo ">> Selected Camera:$cam_index Resolution:$resolution Framerate:$frame_rate"
    read -r -p ">> Press enter to start streaming..." </dev/tty
    ./$tmp_dir/ffmpeg -pix_fmt yuyv422 -probesize 6M -s "$resolution" \
    -f avfoundation -framerate "$frame_rate" -i "$cam_index" -c:v libx264 -preset ultrafast \
    -tune zerolatency -rtsp_transport tcp -f rtsp rtsp://localhost:8554/stream
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
    check_for_packages
    mkdir -p $tmp_dir
    echo ">> Downloading $url"
    wget -nc $url -O ./$tmp_dir/$zip_file_name
    echo Unzipping $zip_file_name...
    unzip -o ./$tmp_dir/$zip_file_name -d ./$tmp_dir/
    capture_user_input
    start_streaming
fi
