# conky-toggl-button
A toggl button for my i3-bar running with conky
![Screenshot of the bar](/screenshot.png)
# Run via crontab
```
*/1 * * * * python togglconky.py
```

# Json for i3bar
```
 {"full_text":" ","color":"\#24708A","separator":false,"separator_block_width":6, "name": "toggl"},
 {"full_text":"${exec cat ~/.config/conky/toggl_running}","color":"\#808080", "separator_block_width":16, "name": "toggl_descr"},
 {"full_text":"${exec cat ~/.config/conky/toggl_project}","color":"\#808080", "name": "toggl_project"},
```

# Sample conkystart file
```
#!/bin/sh

# Send the header so that i3bar knows we want to use JSON:
echo '{"version":1, "click_events": true }'

# Begin the endless array.
echo '['

# We send an empty first array of blocks to make the loop simpler:
echo '[],'

# Now send blocks with information forever:
conky -d -c conkyFileWithJson

# For catchig mouse events on the bar
IFS="}"
while read;do
  IFS=" "
  STR=`echo $REPLY | sed -e s/[{}]//g -e "s/ \"/\"/g" | awk '{n=split($0,a,","); for (i=1; i<=n; i++) {m=split(a[i],b,":"); if (b[1] == "\"name\"") {NAME=b[2]} if (b[1] =="\"x\"") {X=b[2]} if (b[1] =="\"y\"") {Y=b[2]} } print NAME " " X " " Y}'`
  read NAME X Y <<< $STR
  X=$(($X-200))
  Y=$(($Y-82))
  case "${NAME}" in
    \"toggl\")
      python toggl_toggl.py
      python togglconky.py
      ;;
    \"toggl_descr\")
      python toggl_change_name.py $X 1700
      python togglconky.py
      ;;
    \"toggl_project\")
      python toggl_change_project.py $X 1320
      python togglconky.py
      ;;
    *)
      ;;
  esac
  IFS="}"
done
```

