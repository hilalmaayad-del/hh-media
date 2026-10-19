#!/bin/bash
# Rendert alle video's uit build/planning.json naar out/
cd "$(dirname "$0")/.."
mkdir -p out
job(){ slug=$1; eng=$2
  [ -s out/$slug.mp4 ] && return
  case $eng in
    interactie) python3 tools/render_js.py tools/interactie.html build/$slug.json out/$slug.mp4 ;;
    rekenmee)   python3 tools/render_js.py tools/rekenmee.html build/$slug.json out/$slug.mp4 ;;
    fout)       python3 tools/render_js.py tools/fout.html build/$slug.json out/$slug.mp4 ;;
    telmachine) python3 tools/make_video.py contentplan.json $slug out/$slug.mp4 fonts ;;
  esac > out/$slug.log 2>&1 && echo "OK $slug" || echo "FOUT $slug"
}
export -f job
python3 -c "import json;[print(p['slug'],p['engine']) for p in json.load(open('build/planning.json'))]" | xargs -P ${P:-4} -n 2 bash -c 'job "$0" "$1"'
echo KLAAR
