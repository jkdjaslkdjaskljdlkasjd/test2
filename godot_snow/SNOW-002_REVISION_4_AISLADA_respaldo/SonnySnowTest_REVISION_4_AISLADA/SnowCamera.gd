extends RefCounted
## Port of AS2 GridZoomer 3345, GridShaker 3344 and __hdCamSync.
## Coordinates are SWF pixels (not twips), until ground_transform().

const SWF_FPS := 30.0
const SAVER := Vector2(400.0, 294.5)
const PX_PER_UNIT := 1440.0 / 575.0
const LEFT := -1000.0 / 9.0
const ZOOM_TIME := 9
const ZOOM_FACTOR := 70.0
const SCALE_CHANGE := 30.0

var b_position := SAVER
var b_scale := 1.0
var zoom_active := false
var zoom_frame := 1
var zoom_point := 0
var zoom_reverse := 1
var zoom_pause := 0
var zoom_pause_counter := 0
var zoom_delta := Vector2.ZERO
var zoom_scale_delta := 0.0
var shake_active := false
var shake_frame := 1
var shake_value := 8.0
var shake_minus := 0.8

func reset() -> void:
	b_position = SAVER
	b_scale = 1.0
	zoom_active = false
	zoom_frame = 1
	shake_active = false
	shake_frame = 1
	shake_value = 8.0

func start_zoom(kind: String, target_local: Vector2, hd_factor: float) -> bool:
	# Test harness refuses a second trigger while the same clip is running.
	if zoom_active or kind not in ["Melee", "Missile", "Shock"]:
		return false
	var ratio := 0.3 if kind == "Shock" else 0.4
	var destination := Vector2(400, 300) - target_local * ratio
	zoom_delta = (destination - SAVER) / ZOOM_FACTOR * hd_factor
	zoom_scale_delta = SCALE_CHANGE / ZOOM_FACTOR * hd_factor
	zoom_point = ZOOM_TIME
	zoom_reverse = 1
	zoom_pause = 30 if kind == "Melee" else (5 if kind == "Missile" else 1)
	zoom_pause_counter = 0
	zoom_frame = 2
	zoom_active = true
	return true

func start_shake() -> bool:
	if shake_active:
		return false
	shake_active = true
	shake_frame = 1 # GridShaker.play(), unlike zoom's gotoAndPlay(frame 2).
	return true

func tick() -> void:
	# Placement order in frame 217: depth 330 (shake), then 332 (zoom).
	if shake_active:
		shake_frame += 1
		match shake_frame:
			2:
				b_position.y += shake_value / 2.0
			4:
				b_position.y -= shake_value
				shake_value -= shake_minus
			5:
				b_position.y += shake_value
				shake_value -= shake_minus
				if shake_value > 0.0:
					shake_frame = 3 # gotoAndStop("KrinShakeplayHere"); play()
				else:
					shake_value = 8.0
					b_position.y += 0.9000000000000002
					shake_frame = 1
					shake_active = false
	if zoom_active:
		zoom_frame += 1
		match zoom_frame:
			4:
				b_position += zoom_delta * zoom_point * zoom_reverse
				b_scale += zoom_scale_delta * zoom_point * zoom_reverse / 100.0
				zoom_point -= 1
				if zoom_point > 0:
					zoom_frame = 3 # gotoAndStop("KrinZoomPlay"); play()
				elif zoom_reverse == 1:
					zoom_reverse = -1
					zoom_point = ZOOM_TIME
					zoom_pause_counter = 0
					zoom_frame = 5
				else:
					b_position = SAVER
					zoom_frame = 1
					zoom_active = false
			6:
				zoom_pause_counter += 1
				zoom_frame = 3 if zoom_pause_counter == zoom_pause else 5

func ground_transform() -> Transform2D:
	# __hdCamSync with R=1: g=B-SAVER*scale.
	# Then map native x in [-111.111,911.111] to PNG pixels.
	var offset := (b_position - SAVER + (1.0 - b_scale) * (SAVER - Vector2(LEFT, 0.0))) * PX_PER_UNIT
	return Transform2D(Vector2(b_scale, 0), Vector2(0, b_scale), offset)
