#!/bin/bash

# shamelessly stolen from adi and tweaked a bit for my liking

# Check this out:
# https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes
# Maybe convert everything else to this style too... seems simpler.

getcolors() {
	# Grabs our system colors from xresources.
	# Couldn't get this loop below to work.
	#for (( num=0; num<=15; num++ )) ; do
	#	color$num="$(xrdb -query | grep -P "[^.]color$num:" | awk '{print $NF}')"
	#	echo ${color$num}
	#done
	color0="$(xrdb -query | grep -P "[^.]color0:" | awk '{print $NF}')"
	color1="$(xrdb -query | grep -P "[^.]color1:" | awk '{print $NF}')"
	color2="$(xrdb -query | grep -P "[^.]color2:" | awk '{print $NF}')"
	color3="$(xrdb -query | grep -P "[^.]color3:" | awk '{print $NF}')"
	color4="$(xrdb -query | grep -P "[^.]color4:" | awk '{print $NF}')"
	color5="$(xrdb -query | grep -P "[^.]color5:" | awk '{print $NF}')"
	color6="$(xrdb -query | grep -P "[^.]color6:" | awk '{print $NF}')"
	color7="$(xrdb -query | grep -P "[^.]color7:" | awk '{print $NF}')"
	color8="$(xrdb -query | grep -P "[^.]color8:" | awk '{print $NF}')"
	color9="$(xrdb -query | grep -P "[^.]color9:" | awk '{print $NF}')"
	color10="$(xrdb -query | grep -P "[^.]color10:" | awk '{print $NF}')"
	color11="$(xrdb -query | grep -P "[^.]color11:" | awk '{print $NF}')"
	color12="$(xrdb -query | grep -P "[^.]color12:" | awk '{print $NF}')"
	color13="$(xrdb -query | grep -P "[^.]color13:" | awk '{print $NF}')"
	color14="$(xrdb -query | grep -P "[^.]color14:" | awk '{print $NF}')"
	color15="$(xrdb -query | grep -P "[^.]color15:" | awk '{print $NF}')"

}

# Check if tint2 folder exists.
check_files_exist () {
	if [ ! -d "$HOME/.config/tint2/" ]; then
		mkdir ~/.config/tint2/
	fi
}

deploytint2 () {
	# This saves the text of our tint2 config file to the temporary
	# sys variable tint2rc. The main function then echoes it to the
	# tint2 config file.
	read -d '' tint2rc <<- EOF
	# DON'T EDIT THIS FILE. IT WILL BE OVERWRITTEN WHENEVER
	# wal-script IS CALLED. INSTEAD, EDIT THE tint2 FILE IN
	# ~/wal-extended
	# See https://gitlab.com/o9000/tint2/wikis/Configure for
	# full documentation of the configuration options.
	#-------------------------------------
	# Gradients
	#-------------------------------------
	# Backgrounds
	# Background 1: Panel
	rounded = 0
	border_width = 0
	border_sides = TBLR
	background_color = ${color0} 100
	border_color = #00ff00 30
	background_color_hover = #00ff00 60
	border_color_hover = #00ff00 30
	background_color_pressed = #00ff00 60
	border_color_pressed = #000000 30

	# Background 2: Default task, Iconified task
	rounded = 12
	border_width = 2
	border_sides = TBLR
	background_color = ${color1} 100
	border_color = ${color3} 100
	background_color_hover = ${color2} 100
	border_color_hover = ${color5} 100
	background_color_pressed = #00ff00 4
	border_color_pressed = #eaeaea 44

	# Background 3: Active task
	rounded = 12
	border_width = 2
	border_sides = TBLR
	background_color = ${color3} 100
	border_color = ${color1} 100
	background_color_hover = ${color2} 100
	border_color_hover = ${color5} 100
	background_color_pressed = #555555 4
	border_color_pressed = #eaeaea 44

	# Background 4: Urgent task
	rounded = 0
	border_width = 1
	border_sides = TBLR
	background_color = #aa4400 100
	border_color = #aa7733 100
	background_color_hover = #cc7700 100
	border_color_hover = #aa7733 100
	background_color_pressed = #555555 4
	border_color_pressed = #aa7733 100

	# Background 5: Tooltip
	rounded = 1
	border_width = 1
	border_sides = TBLR
	background_color = ${color2} 100
	border_color = ${color4} 100
	background_color_hover = #ffffaa 100
	border_color_hover = #000000 100
	background_color_pressed = #ffffaa 100
	border_color_pressed = #000000 100

	#-------------------------------------
	# Panel
	panel_items = TS
	panel_size = 100% 30
	panel_margin = 0 0
	panel_padding = 2 0 2
	panel_background_id = 1
	wm_menu = 1
	panel_dock = 0
	panel_position = bottom center horizontal
	panel_layer = top
	panel_monitor = all
	panel_shrink = 0
	autohide = 0
	autohide_show_timeout = 0
	autohide_hide_timeout = 1
	autohide_height = 2
	strut_policy = follow_size
	panel_window_name = tint2
	disable_transparency = 1
	mouse_effects = 1
	font_shadow = 0
	mouse_hover_icon_asb = 100 0 10
	mouse_pressed_icon_asb = 100 0 0

	#-------------------------------------
	# Taskbar
	taskbar_mode = single_desktop
	taskbar_hide_if_empty = 1
	taskbar_padding = 0 0 2
	taskbar_background_id = 0
	taskbar_active_background_id = 0
	taskbar_name = 0
	taskbar_hide_inactive_tasks = 0
	taskbar_hide_different_monitor = 0
	taskbar_hide_different_desktop = 0
	taskbar_always_show_all_desktop_tasks = 0
	taskbar_name_padding = 4 2
	taskbar_name_background_id = 0
	taskbar_name_active_background_id = 0
	taskbar_name_font_color = ${color0} 100
	taskbar_name_active_font_color = ${color0} 100
	taskbar_distribute_size = 0
	taskbar_sort_order = none
	task_align = left

	#-------------------------------------
	# Task
	task_text = 1
	task_icon = 1
	task_centered = 1
	urgent_nb_of_blink = 100000
	task_maximum_size = 150 35
	task_padding = 2 2 4
	task_tooltip = 1
	task_thumbnail = 0
	task_thumbnail_size = 210
	task_font_color = ${color7} 100
	task_background_id = 2
	task_active_background_id = 3
	task_urgent_background_id = 4
	task_iconified_background_id = 2
	mouse_left = toggle_iconify
	mouse_middle = none
	mouse_right = close
	mouse_scroll_up = toggle
	mouse_scroll_down = iconify

	#-------------------------------------
	# System tray (notification area)
	systray_padding = 0 4 2
	systray_background_id = 0
	systray_sort = ascending
	systray_icon_size = 24
	systray_icon_asb = 100 0 0
	systray_monitor = 1
	systray_name_filter = 

	#-------------------------------------
	# Launcher
	launcher_padding = 2 4 2
	launcher_background_id = 0
	launcher_icon_background_id = 0
	launcher_icon_size = 24
	launcher_icon_asb = 100 0 0
	launcher_icon_theme_override = 0
	startup_notifications = 1
	launcher_tooltip = 1
	launcher_item_app = tint2conf.desktop

	#-------------------------------------
	# Clock
	time1_format = %H:%M
	time2_format = %A %d %B
	time1_timezone = 
	time2_timezone = 
	clock_font_color = #ffffff 100
	clock_padding = 2 0
	clock_background_id = 0
	clock_tooltip = 
	clock_tooltip_timezone = 
	clock_lclick_command = 
	clock_rclick_command = orage
	clock_mclick_command = 
	clock_uwheel_command = 
	clock_dwheel_command = 

	#-------------------------------------
	# Battery
	battery_tooltip = 1
	battery_low_status = 10
	battery_low_cmd = xmessage 'tint2: Battery low!'
	battery_full_cmd = 
	battery_font_color = #ffffff 100
	bat1_format = 
	bat2_format = 
	battery_padding = 1 0
	battery_background_id = 0
	battery_hide = 101
	battery_lclick_command = 
	battery_rclick_command = 
	battery_mclick_command = 
	battery_uwheel_command = 
	battery_dwheel_command = 
	ac_connected_cmd = 
	ac_disconnected_cmd = 

	#-------------------------------------
	# Tooltip
	tooltip_show_timeout = 0.5
	tooltip_hide_timeout = 0.1
	tooltip_padding = 4 4
	tooltip_background_id = 5
	tooltip_font_color = ${color1} 100

	EOF
}

main() {
	check_files_exist
	killall tint2
	getcolors
	deploytint2
	echo "$tint2rc" > ~/.config/tint2/tint2rc
	tint2 &
}

main
