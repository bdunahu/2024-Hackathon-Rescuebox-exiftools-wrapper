#!/bin/sh

err() { echo "Usage:
      extract [OPTIONS] directory
Options:
	-d: turns on process reporting.
	-o: name of the output file. Defaults to out.json" && exit 1;}

debug=1
out="out.json"
while getopts "do:" opt; do case "${opt}" in
			    d) debug=0 ;;
			    o) out="${OPTARG}" ;;
			    *) printf "Invalid option: -%s\\n" "$OPTARG" && err ;;
			esac done

shift $((OPTIND -1))

dir="$1"

[ -d "${dir}" ] &&
    # you can request certain fields by passing flags to exiftool. No flags gives everything!
    ( exiftool -r -json -T "${dir}" >> "${out}" &
      exif_pid=$!

      # cpu, memory, virtual memory size, resident set size, thread count, time
      [ $debug == "0" ] && echo '%CPU %MEM    VSZ   RSS WCHARS THCNT    TIME'
      while [ $debug  == "0" ] && kill -0 "${exif_pid}" 2>/dev/null;
      do
	  ps -p $exif_pid -o %cpu,%mem,vsz,rss,wchars,thcount,time | sed '1d'
	  sleep 0.05
      done
      wait "${exif_pid}"
      printf "Output to %s\\n" "${out}"
    ) || ( printf "%s is not a directory, or exiftool was interrupted.\\n" "${dir}" && err )
