extends Node2D
## SNOW-002 (Basado directamente en SNOW-002_REVISION_3_AISLADA):
## - Usa exactamente SnowCamera.gd (RefCounted) de SNOW-001 sin modificarlo.
## - Los 6 marcadores (player1..player6) cuelgan de $GroundLayer/SlotsLayer y heredan ground.transform.
## - Separa estrictamente la procedencia de Posicion (pos_src), Escala (scale_src) y Dimensiones (size_src).
## - En los 6 slots (DefineSprite_2503), adopta la caja F1 del contenedor (inner2, cid 2462: 65.05 x 99.756,
##   yMin=-54.006, yMax=+45.75) como guia geometrica del contenedor en F1 (sin asumir que (0,0) sea la planta
##   del personaje vestido): dibuja una cruz en el origen (0,0) del slot y una linea en el borde inferior yMax
##   de la caja F1 (+45.75 u SWF).

const CameraModel = preload("res://SnowCamera.gd")

const HD_LAYOUT_S := 0.62
const HD_LAYOUT_AX := 400.0
const HD_LAYOUT_AY := 575.0
const HD_LAYOUT_DY := -12.0

var camera = CameraModel.new()
var accumulator := 0.0
var hd_factor := 0.5
var target_local := Vector2(160.0, -20.0)
var selected_target_label := "Manual"
var paused := false
var view_mode := 0 # 0 layers, 1 original, 2 world map, 3 alpha diagnosis
var show_hud := true
var show_battle_guides := true
var last_attack := "Ninguno"

var slots_pos_swf := 0
var slots_size_swf := 0
var top_pos_swf := 0
var top_size_swf := 0
var bot_pos_swf := 0
var bot_size_swf := 0

# Slots (player1..player6).
# Coordenadas de respaldo en caso de correr sin battle_layout_217.json: todas inician con pos_src="PROV",
# scale_src="PROV" y size_src="PROV" hasta que _load_extracted_layout_if_available() cargue el JSON.
var slots_data := {
	"player1": {"x": 160.9, "y": 297.4, "xscale": 100.0,  "yscale": 100.0, "xMin": -32.95, "yMin": -54.006, "w": 65.05, "h": 99.756, "team": "ally",  "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"player3": {"x": 220.9, "y": 371.0, "xscale": 100.0,  "yscale": 100.0, "xMin": -32.95, "yMin": -54.006, "w": 65.05, "h": 99.756, "team": "ally",  "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"player5": {"x": 220.9, "y": 218.5, "xscale": 100.0,  "yscale": 100.0, "xMin": -32.95, "yMin": -54.006, "w": 65.05, "h": 99.756, "team": "ally",  "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"player2": {"x": 637.9, "y": 297.4, "xscale": -100.0, "yscale": 100.0, "xMin": -32.10, "yMin": -54.006, "w": 65.05, "h": 99.756, "team": "enemy", "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"player4": {"x": 577.9, "y": 371.0, "xscale": -100.0, "yscale": 100.0, "xMin": -32.10, "yMin": -54.006, "w": 65.05, "h": 99.756, "team": "enemy", "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"player6": {"x": 577.9, "y": 218.5, "xscale": -100.0, "yscale": 100.0, "xMin": -32.10, "yMin": -54.006, "w": 65.05, "h": 99.756, "team": "enemy", "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
}

# Barras superiores fijas al 100% (profundidades 342, 360, 378, 396, 414, 432 en PlaceObject3)
var top_bars_data := {
	"p1BAR": {"x": -95.0, "y": 10.0, "xscale": 100.0, "yscale": 100.0, "xMin": 0.0, "yMin": 0.0, "w": 235.0, "h": 26.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"p3BAR": {"x": -95.0, "y": 40.0, "xscale": 100.0, "yscale": 100.0, "xMin": 0.0, "yMin": 0.0, "w": 215.0, "h": 24.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"p5BAR": {"x": -95.0, "y": 68.0, "xscale": 100.0, "yscale": 100.0, "xMin": 0.0, "yMin": 0.0, "w": 215.0, "h": 24.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"p2BAR": {"x": 660.0, "y": 10.0, "xscale": 100.0, "yscale": 100.0, "xMin": 0.0, "yMin": 0.0, "w": 235.0, "h": 26.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"p4BAR": {"x": 680.0, "y": 40.0, "xscale": 100.0, "yscale": 100.0, "xMin": 0.0, "yMin": 0.0, "w": 215.0, "h": 24.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
	"p6BAR": {"x": 680.0, "y": 68.0, "xscale": 100.0, "yscale": 100.0, "xMin": 0.0, "yMin": 0.0, "w": 215.0, "h": 24.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV"},
}

# Las 9 piezas del panel inferior ANTES de aplicar __hdBattleLayout (s=0.62, ax=400, ay=575, dy=-12).
# Sin JSON, todas las dimensiones se marcan como "PROV" (krinToMove2, moveSelectBoomer y __hdSkipX mantienen
# size_src="PROV" incluso con JSON porque su fotograma 1 en el SWF no tiene bounds geometricos).
var bottom_panel_data := {
	"UI_BAR":           {"x": 0.0,    "y": 476.0,  "xscale": 100.0,   "yscale": 100.0,   "xMin": 0.0,   "yMin": 0.0,   "w": 800.0, "h": 99.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV", "color": Color(0.12, 0.14, 0.18, 0.78)},
	"depth_65":         {"x": 400.0,  "y": 507.9,  "xscale": 100.0,   "yscale": 100.0,   "xMin": -15.0, "yMin": -15.0, "w": 30.0,  "h": 30.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV", "color": Color(0.16, 0.18, 0.22, 0.55)},
	"battleClocker":    {"x": 400.0,  "y": 507.25, "xscale": 100.0,   "yscale": 100.0,   "xMin": -31.8, "yMin": -31.8, "w": 63.6,  "h": 63.6, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV", "color": Color(0.30, 0.26, 0.16, 0.85)},
	"krinToMove":       {"x": 400.0,  "y": 507.5,  "xscale": 122.948, "yscale": 122.948, "xMin": -14.1, "yMin": -14.1, "w": 28.3,  "h": 28.3, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV", "color": Color(0.22, 0.25, 0.30, 0.85)},
	"krinToMove2":      {"x": 400.0,  "y": 507.75, "xscale": 142.963, "yscale": 142.963, "xMin": -20.0, "yMin": -20.0, "w": 40.0,  "h": 40.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV", "color": Color(0.25, 0.28, 0.35, 0.75)},
	"moveSelectBoomer": {"x": 400.0,  "y": 508.1,  "xscale": 100.0,   "yscale": 100.0,   "xMin": -16.0, "yMin": -16.0, "w": 32.0,  "h": 32.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV", "color": Color(0.28, 0.22, 0.32, 0.70)},
	"combatScript":     {"x": 473.05, "y": 460.55, "xscale": 100.0,   "yscale": 100.0,   "xMin": 0.0,   "yMin": 0.0,   "w": 305.0, "h": 32.0, "pos_src": "CODE", "scale_src": "CODE", "size_src": "PROV", "color": Color(0.18, 0.32, 0.22, 0.70)},
	"__hdSkipX":        {"x": 435.85, "y": 464.15, "xscale": 100.0,   "yscale": 100.0,   "xMin": 0.0,   "yMin": 0.0,   "w": 18.0,  "h": 18.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV", "color": Color(0.65, 0.15, 0.15, 0.85)},
	"__hdSkipXbg":      {"x": 0.0,    "y": 0.0,    "xscale": 100.0,   "yscale": 100.0,   "xMin": 435.85,"yMin": 464.15,"w": 18.0,  "h": 18.0, "pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV", "color": Color(0.45, 0.10, 0.10, 0.75)},
}

@onready var sky: Sprite2D = $SkyLayer
@onready var ground: Sprite2D = $GroundLayer
@onready var slots_layer: Node2D = $GroundLayer/SlotsLayer
@onready var original: Sprite2D = $Original
@onready var village: Sprite2D = $Village
@onready var hud: CanvasLayer = $HUD
@onready var hud_guide: Control = $HUD/BattleHudGuide
@onready var status: Label = $HUD/Status


func _ready() -> void:
	_load_extracted_layout_if_available()
	_recount_provenance()
	_rebuild_slot_markers()
	hud_guide.draw.connect(_on_draw_hud_guide)
	apply_camera()


func stage_to_px(stage_pt: Vector2) -> Vector2:
	return (stage_pt - Vector2(CameraModel.LEFT, 0.0)) * CameraModel.PX_PER_UNIT


func apply_hd_bottom_point(stage_pt: Vector2) -> Vector2:
	return Vector2(
		HD_LAYOUT_AX + (stage_pt.x - HD_LAYOUT_AX) * HD_LAYOUT_S,
		HD_LAYOUT_AY + HD_LAYOUT_DY + (stage_pt.y - HD_LAYOUT_AY) * HD_LAYOUT_S
	)


func format_provenance_badge(item: Dictionary) -> String:
	var p_src: String = item.get("pos_src", "PROV")
	var sz_src: String = item.get("size_src", "PROV")
	if p_src == "SWF" and sz_src == "SWF_F1":
		return "[SWF]"
	if p_src == "SWF" and sz_src == "SWF_POSE":
		return "[pos:SWF | tam:SWF_POSE]"
	return "[pos:%s | tam:%s]" % [p_src, sz_src]


func _apply_json_bounds_to_entry(dest: Dictionary, src_item: Dictionary, origin_in_parent: Vector2) -> void:
	var b_f1 = src_item.get("bounds_in_parent")
	if typeof(b_f1) == TYPE_DICTIONARY and (float(b_f1.get("w", 0.0)) > 0.0 or float(b_f1.get("h", 0.0)) > 0.0):
		dest["xMin"] = float(b_f1["xMin"]) - origin_in_parent.x
		dest["yMin"] = float(b_f1["yMin"]) - origin_in_parent.y
		dest["w"] = float(b_f1["w"])
		dest["h"] = float(b_f1["h"])
		dest["size_src"] = "SWF_F1"
		return

	var b_pose = src_item.get("reference_pose_in_parent")
	if typeof(b_pose) == TYPE_DICTIONARY and (float(b_pose.get("w", 0.0)) > 0.0 or float(b_pose.get("h", 0.0)) > 0.0):
		dest["xMin"] = float(b_pose["xMin"]) - origin_in_parent.x
		dest["yMin"] = float(b_pose["yMin"]) - origin_in_parent.y
		dest["w"] = float(b_pose["w"])
		dest["h"] = float(b_pose["h"])
		dest["size_src"] = "SWF_POSE"
		return

	# Si bounds_in_parent y reference_pose_in_parent son null, conserva el tamano provisional y size_src = "PROV"
	dest["size_src"] = "PROV"


func _load_extracted_layout_if_available() -> void:
	var path := "res://assets/battle_layout_217.json"
	if not FileAccess.file_exists(path):
		return
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return

	var bs: Dictionary = parsed.get("battlescreen_d89", {})
	var bs_mat: Dictionary = bs.get("matrix", {
		"a": 1.0, "b": 0.0, "c": 0.0, "d": 1.0,
		"tx": float(bs.get("x", CameraModel.SAVER.x)),
		"ty": float(bs.get("y", CameraModel.SAVER.y))
	})

	# 1. Cargar slots player1..player6 separando posicion/escala de dimensiones
	var p_dict: Dictionary = parsed.get("players", {})
	for pname in p_dict.keys():
		if not slots_data.has(pname):
			continue
		var p: Dictionary = p_dict[pname]
		var px_local := float(p.get("x", 0.0))
		var py_local := float(p.get("y", 0.0))
		var stage_x: float = float(bs_mat["a"]) * px_local + float(bs_mat["c"]) * py_local + float(bs_mat["tx"])
		var stage_y: float = float(bs_mat["b"]) * px_local + float(bs_mat["d"]) * py_local + float(bs_mat["ty"])
		slots_data[pname]["x"] = stage_x
		slots_data[pname]["y"] = stage_y
		slots_data[pname]["xscale"] = float(p.get("xscale", 100.0))
		slots_data[pname]["yscale"] = float(p.get("yscale", 100.0))
		slots_data[pname]["pos_src"] = "SWF"
		slots_data[pname]["scale_src"] = "SWF"
		_apply_json_bounds_to_entry(slots_data[pname], p, Vector2(px_local, py_local))

	# 2. Cargar barras superiores p1BAR..p6BAR
	var tb_dict: Dictionary = parsed.get("top_bars", {})
	for bname in tb_dict.keys():
		if not top_bars_data.has(bname):
			continue
		var item: Dictionary = tb_dict[bname]
		var bx := float(item.get("x", top_bars_data[bname]["x"]))
		var by := float(item.get("y", top_bars_data[bname]["y"]))
		top_bars_data[bname]["x"] = bx
		top_bars_data[bname]["y"] = by
		top_bars_data[bname]["xscale"] = float(item.get("xscale", 100.0))
		top_bars_data[bname]["yscale"] = float(item.get("yscale", 100.0))
		top_bars_data[bname]["pos_src"] = "SWF"
		top_bars_data[bname]["scale_src"] = "SWF"
		_apply_json_bounds_to_entry(top_bars_data[bname], item, Vector2(bx, by))

	# 3. Cargar las 9 piezas del panel inferior
	var bp_dict: Dictionary = parsed.get("bottom_panel", {})
	for k in bp_dict.keys():
		var item: Dictionary = bp_dict[k]
		if not bottom_panel_data.has(k):
			bottom_panel_data[k] = {
				"x": 0.0, "y": 0.0, "xscale": 100.0, "yscale": 100.0,
				"xMin": -16.0, "yMin": -16.0, "w": 32.0, "h": 32.0,
				"pos_src": "PROV", "scale_src": "PROV", "size_src": "PROV",
				"color": Color(0.20, 0.24, 0.30, 0.75)
			}
		var bx := float(item.get("x", bottom_panel_data[k]["x"]))
		var by := float(item.get("y", bottom_panel_data[k]["y"]))
		bottom_panel_data[k]["x"] = bx
		bottom_panel_data[k]["y"] = by
		bottom_panel_data[k]["xscale"] = float(item.get("xscale", 100.0))
		bottom_panel_data[k]["yscale"] = float(item.get("yscale", 100.0))
		bottom_panel_data[k]["pos_src"] = "SWF"
		bottom_panel_data[k]["scale_src"] = "SWF"
		_apply_json_bounds_to_entry(bottom_panel_data[k], item, Vector2(bx, by))


func _recount_provenance() -> void:
	slots_pos_swf = 0
	slots_size_swf = 0
	for s in slots_data.values():
		if s["pos_src"] == "SWF":
			slots_pos_swf += 1
		if s["size_src"].begins_with("SWF"):
			slots_size_swf += 1

	top_pos_swf = 0
	top_size_swf = 0
	for b in top_bars_data.values():
		if b["pos_src"] == "SWF":
			top_pos_swf += 1
		if b["size_src"].begins_with("SWF"):
			top_size_swf += 1

	bot_pos_swf = 0
	bot_size_swf = 0
	for p in bottom_panel_data.values():
		if p["pos_src"] == "SWF":
			bot_pos_swf += 1
		if p["size_src"].begins_with("SWF"):
			bot_size_swf += 1


func _rebuild_slot_markers() -> void:
	for child in slots_layer.get_children():
		child.queue_free()

	for key in ["player1", "player3", "player5", "player2", "player4", "player6"]:
		var s: Dictionary = slots_data[key]
		var origin_px: Vector2 = stage_to_px(Vector2(s["x"], s["y"]))
		var rect_pos_px: Vector2 = Vector2(s["xMin"], s["yMin"]) * CameraModel.PX_PER_UNIT
		var rect_size_px: Vector2 = Vector2(s["w"], s["h"]) * CameraModel.PX_PER_UNIT
		var base_f1_y_px: float = rect_pos_px.y + rect_size_px.y
		var is_ally: bool = (s["team"] == "ally")
		var badge: String = format_provenance_badge(s)

		var col_fill := Color(0.15, 0.65, 1.0, 0.24) if is_ally else Color(1.0, 0.25, 0.25, 0.24)
		var col_edge := Color(0.35, 0.85, 1.0, 0.95) if is_ally else Color(1.0, 0.45, 0.45, 0.95)

		var holder := Node2D.new()
		holder.name = key
		holder.position = origin_px
		slots_layer.add_child(holder)

		# 1. Caja F1 del contenedor DefineSprite_2503 (inner2, cid 2462)
		var body := ColorRect.new()
		body.position = rect_pos_px
		body.size = rect_size_px
		body.color = col_fill
		body.mouse_filter = Control.MOUSE_FILTER_IGNORE
		holder.add_child(body)

		# 2. Cruz amarilla en (0, 0): origen de registro del slot 2503 en BATTLESCREEN
		var origin_h := ColorRect.new()
		origin_h.position = Vector2(-14.0, -1.5)
		origin_h.size = Vector2(28.0, 3.0)
		origin_h.color = Color(1.0, 0.95, 0.35, 0.95)
		origin_h.mouse_filter = Control.MOUSE_FILTER_IGNORE
		holder.add_child(origin_h)

		var origin_v := ColorRect.new()
		origin_v.position = Vector2(-1.5, -14.0)
		origin_v.size = Vector2(3.0, 28.0)
		origin_v.color = Color(1.0, 0.95, 0.35, 0.95)
		origin_v.mouse_filter = Control.MOUSE_FILTER_IGNORE
		holder.add_child(origin_v)

		# 3. Linea en yMax (+45.75 u SWF): borde inferior de la caja F1 del contenedor 2503
		var f1_bottom_line := ColorRect.new()
		f1_bottom_line.position = Vector2(rect_pos_px.x - 10.0, base_f1_y_px - 3.0)
		f1_bottom_line.size = Vector2(rect_size_px.x + 20.0, 6.0)
		f1_bottom_line.color = col_edge
		f1_bottom_line.mouse_filter = Control.MOUSE_FILTER_IGNORE
		holder.add_child(f1_bottom_line)

		var y_f1_bottom: float = float(s["y"]) + float(s["yMin"]) + float(s["h"])
		var lbl := Label.new()
		lbl.position = Vector2(rect_pos_px.x - 10.0, rect_pos_px.y - 54.0)
		lbl.add_theme_font_size_override("font_size", 16)
		lbl.modulate = col_edge
		lbl.text = "%s %s\norig=(%.1f, %.1f) baseF1=%.1f" % [
			key, badge, s["x"], s["y"], y_f1_bottom
		]
		holder.add_child(lbl)


func _process(delta: float) -> void:
	if not paused:
		accumulator += delta
		while accumulator >= 1.0 / CameraModel.SWF_FPS:
			camera.tick()
			accumulator -= 1.0 / CameraModel.SWF_FPS
		apply_camera()


func trigger(kind: String) -> void:
	if camera.start_zoom(kind, target_local, hd_factor):
		last_attack = kind
		if kind == "Shock":
			camera.start_shake()
		apply_camera()


func select_slot_target(slot_key: String) -> void:
	if not slots_data.has(slot_key):
		return
	var s: Dictionary = slots_data[slot_key]
	var target_stage: Vector2
	if String(s["size_src"]).begins_with("SWF"):
		target_stage = Vector2(s["x"] + s["xMin"] + s["w"] * 0.5, s["y"] + s["yMin"] + s["h"] * 0.5)
	else:
		target_stage = Vector2(s["x"], s["y"])
	target_local = target_stage - CameraModel.SAVER
	selected_target_label = slot_key
	apply_camera()


func apply_camera() -> void:
	ground.transform = camera.ground_transform()
	sky.visible = view_mode == 0
	ground.visible = view_mode == 0 or view_mode == 3
	slots_layer.visible = show_battle_guides and (view_mode == 0 or view_mode == 3)
	original.visible = view_mode == 1
	village.visible = view_mode == 2
	hud.visible = show_hud
	hud_guide.visible = show_battle_guides and (view_mode == 0 or view_mode == 3)

	var modes := ["Dos capas", "Original inmóvil", "Mapa VILLAGE", "Alfa sobre magenta"]
	var ver_summary := "Slots pos:%d/6 tam:%d/6 | Sup pos:%d/6 tam:%d/6 | Inf pos:%d/%d tam:%d/%d" % [
		slots_pos_swf, slots_size_swf,
		top_pos_swf, top_size_swf,
		bot_pos_swf, bottom_panel_data.size(), bot_size_swf, bottom_panel_data.size()
	]
	status.text = "%s | %s · factor %.1f · escala %.6f · obj %s (%.1f, %.1f) · %s\n[%s]" % [
		modes[view_mode], last_attack, hd_factor, camera.b_scale,
		selected_target_label, target_local.x, target_local.y,
		"PAUSA" if paused else "30 Hz SWF", ver_summary
	]
	hud_guide.queue_redraw()
	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if view_mode == 0 or view_mode == 3:
			var source_pixel: Vector2 = ground.to_local(get_global_mouse_position())
			target_local = source_pixel / CameraModel.PX_PER_UNIT + Vector2(CameraModel.LEFT, 0.0) - CameraModel.SAVER
			selected_target_label = "Manual"
			apply_camera()
	if event is InputEventKey and event.pressed and not event.echo:
		match event.physical_keycode:
			KEY_1: trigger("Melee")
			KEY_2: trigger("Missile")
			KEY_3: trigger("Shock")
			KEY_S: camera.start_shake()
			KEY_R:
				camera.reset()
				accumulator = 0.0
			KEY_C:
				hd_factor = 1.0 if hd_factor == 0.5 else 0.5
				camera.reset()
				accumulator = 0.0
			KEY_O: view_mode = 0 if view_mode == 1 else 1
			KEY_V: view_mode = 0 if view_mode == 2 else 2
			KEY_G: view_mode = 0 if view_mode == 3 else 3
			KEY_SPACE:
				paused = not paused
				accumulator = 0.0
			KEY_N:
				if paused:
					camera.tick()
			KEY_H: show_hud = not show_hud
			KEY_B: show_battle_guides = not show_battle_guides
			KEY_F1: select_slot_target("player1")
			KEY_F2: select_slot_target("player2")
			KEY_F3: select_slot_target("player3")
			KEY_F4: select_slot_target("player4")
			KEY_F5: select_slot_target("player5")
			KEY_F6: select_slot_target("player6")
			KEY_ESCAPE: get_tree().quit()
		apply_camera()


func _on_draw_hud_guide() -> void:
	if not show_battle_guides or (view_mode != 0 and view_mode != 3):
		return
	var font: Font = ThemeDB.fallback_font

	# 1. Barras superiores fijas al 100% (NO reciben el 62%)
	for bname in top_bars_data.keys():
		var b: Dictionary = top_bars_data[bname]
		var top_left_stage := Vector2(b["x"] + b["xMin"], b["y"] + b["yMin"])
		var p0: Vector2 = stage_to_px(top_left_stage)
		var sz: Vector2 = Vector2(b["w"], b["h"]) * CameraModel.PX_PER_UNIT
		var badge: String = format_provenance_badge(b)
		var rect := Rect2(p0, sz)
		hud_guide.draw_rect(rect, Color(0.08, 0.10, 0.12, 0.72), true)
		hud_guide.draw_rect(rect, Color(0.45, 0.85, 0.45, 0.92), false, 2.0)
		hud_guide.draw_string(font, p0 + Vector2(8, sz.y * 0.68), "%s %s (100%%)" % [bname, badge], HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color(0.85, 1.0, 0.85))

	# 2. Las 9 piezas del panel inferior transformadas al 62% con ancla (400, 575) y dy = -12 (__hdBattleLayout)
	var center_stack_idx := 0
	for pname in bottom_panel_data.keys():
		var item: Dictionary = bottom_panel_data[pname]
		var raw_p0 := Vector2(item["x"] + item["xMin"], item["y"] + item["yMin"])
		var raw_sz := Vector2(item["w"], item["h"])
		var hd_p0: Vector2 = apply_hd_bottom_point(raw_p0)
		var hd_sz: Vector2 = raw_sz * HD_LAYOUT_S
		var px_p0: Vector2 = stage_to_px(hd_p0)
		var px_sz: Vector2 = hd_sz * CameraModel.PX_PER_UNIT
		var badge: String = format_provenance_badge(item)
		var rect := Rect2(px_p0, px_sz)
		hud_guide.draw_rect(rect, item["color"], true)
		hud_guide.draw_rect(rect, Color(0.95, 0.80, 0.30, 0.92), false, 2.0)

		var label_pos := px_p0 + Vector2(8, 18)
		if absf(float(item["x"]) - 400.0) < 1.0 and float(item["w"]) < 200.0:
			label_pos = px_p0 + Vector2(px_sz.x + 10.0, 12.0 + center_stack_idx * 18.0)
			center_stack_idx += 1
		hud_guide.draw_string(font, label_pos, "%s %s [62%%]" % [pname, badge], HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color(1.0, 0.95, 0.75))


func _draw() -> void:
	if show_hud and (view_mode == 0 or view_mode == 3):
		var pixel := (target_local + CameraModel.SAVER - Vector2(CameraModel.LEFT, 0.0)) * CameraModel.PX_PER_UNIT
		var marker: Vector2 = camera.ground_transform() * pixel
		draw_arc(marker, 14, 0, TAU, 32, Color.WHITE, 2.0)
		draw_line(marker - Vector2(22, 0), marker + Vector2(22, 0), Color.WHITE, 2.0)
		draw_line(marker - Vector2(0, 22), marker + Vector2(0, 22), Color.WHITE, 2.0)

