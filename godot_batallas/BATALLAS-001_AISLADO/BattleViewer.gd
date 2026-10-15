extends Node2D
## BATALLAS-001 (AISLADO, NO VERIFICADO EN GODOT)
## Visor de las 99 alineaciones de combate del SWF I41 sobre su fondo HD de dos capas.
## Sin lógica de combate: solo fondo, personajes originales en sus slots, animaciones y cámara.
##
## Comprobado en el código I41 (ver datos/combates.json y LEEME.txt):
##  - fondo HD: _root.__hdBattleMap[ZoneBG|SkyBG] (frame_42/DoAction_2.as l.39048-39059)
##  - capas cielo/suelo: generadas con las funciones SIN CAMBIOS de i40/fuente/capas.py (SNOW = SNOW-001 píxel a píxel)
##  - alineación: KBR<n>.players[k] -> slot player(k+2); >0 KNU<n>, -2 compañero 1, -1 compañero 2, 0 vacío
##  - colocación: BATTLESCREEN["player"+id].attachMovie(model,"inner",0) en el origen del slot, identidad;
##    MODEL5: escala 0.8 y +10 en y (frame_217/DoAction.as l.19-24)
##  - profundidad de los slots: PlaceObject de frame 217 (player5 40 < player6 80 < player1 120 < player2 160 < player3 200 < player4 240)
## Propuesto (PROV):
##  - objetivo del zoom = origen del slot; la cámara real apunta a la posición del atacante/objetivo del momento.
##  - compañeros y Sonny con apariencia por defecto (en el juego dependen de la partida).

const CameraModel = preload("res://SnowCamera.gd")
const DATA_PATH := "res://datos/combates.json"
const SLOT_ORDER := ["player1", "player2", "player3", "player4", "player5", "player6"]
const SLOT_DEPTH := {"player5": 40, "player6": 80, "player1": 120, "player2": 160, "player3": 200, "player4": 240}

var camera = CameraModel.new()
var accumulator := 0.0
var hd_factor := 0.5
var paused := false
var show_hud := true

var data: Dictionary = {}
var battles: Array = []
var battle_index := 0
var selected_slot := "player1"
var target_local := Vector2.ZERO
var last_action := "—"
var units := {}          # slot -> {"node": Node2D, "anim": AnimationPlayer, "info": Dictionary}
var missing: Array = []

@onready var sky: Sprite2D = $SkyLayer
@onready var ground: Sprite2D = $GroundLayer
@onready var units_layer: Node2D = $GroundLayer/UnitsLayer
@onready var hud: CanvasLayer = $HUD
@onready var status: Label = $HUD/Status


func _ready() -> void:
	units_layer.z_as_relative = true
	_load_data()
	var start := OS.get_environment("BATALLA")
	if start != "":
		for i in battles.size():
			if String(battles[i]["combate"]) == start:
				battle_index = i
	show_battle(battle_index)


func _load_data() -> void:
	var f := FileAccess.open(DATA_PATH, FileAccess.READ)
	if f == null:
		push_error("No se encontró " + DATA_PATH)
		return
	var parsed = JSON.parse_string(f.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("JSON inválido: " + DATA_PATH)
		return
	data = parsed
	battles = data.get("combates", [])


static func stage_to_px(stage_pt: Vector2) -> Vector2:
	return (stage_pt - Vector2(CameraModel.LEFT, 0.0)) * CameraModel.PX_PER_UNIT


func slot_stage(slot: String) -> Vector2:
	var s: Dictionary = data["slots"][slot]
	return Vector2(float(s["x_stage"]), float(s["y_stage"]))


func show_battle(i: int) -> void:
	if battles.is_empty():
		return
	battle_index = posmod(i, battles.size())
	var b: Dictionary = battles[battle_index]
	var zona := String(b["zona_hd"])
	sky.texture = load("res://assets/zonas/%s_sky.png" % zona)
	ground.texture = load("res://assets/zonas/%s_ground.png" % zona)
	camera.reset()
	accumulator = 0.0
	for c in units_layer.get_children():
		units_layer.remove_child(c)
		c.queue_free()
	units.clear()
	missing.clear()
	for slot in SLOT_ORDER:
		var info: Dictionary = b["slots"].get(slot, {})
		var holder := Node2D.new()
		holder.name = slot
		holder.position = stage_to_px(slot_stage(slot))
		holder.z_index = int(SLOT_DEPTH[slot])
		units_layer.add_child(holder)
		var entry := {"node": null, "anim": null, "info": info, "holder": holder}
		var path := String(info.get("escena", ""))
		if path != "":
			if ResourceLoader.exists(path):
				var unit: Node2D = (load(path) as PackedScene).instantiate()
				var sx := float(data["slots"][slot]["xscale"])
				var k := CameraModel.PX_PER_UNIT
				if String(info.get("model", "")) == "MODEL5":
					unit.scale = Vector2(0.8 * k * sx, 0.8 * k)
					unit.position = Vector2(0.0, 10.0 * k)
				else:
					unit.scale = Vector2(k * sx, k)
				holder.add_child(unit)
				entry["node"] = unit
				var ap: AnimationPlayer = unit.get_node_or_null("AnimationPlayer")
				entry["anim"] = ap
				if ap and ap.has_animation("stand"):
					ap.play("stand")
			else:
				missing.append(path)
		units[slot] = entry
	if not units.has(selected_slot) or units[selected_slot]["node"] == null:
		selected_slot = "player1"
	select_slot(selected_slot)
	last_action = "—"
	queue_redraw()
	apply_camera()


func select_slot(slot: String) -> void:
	selected_slot = slot
	target_local = slot_stage(slot) - CameraModel.SAVER   # PROV: origen del slot
	queue_redraw()


func play_on_selected(candidates: Array) -> void:
	var e: Dictionary = units.get(selected_slot, {})
	var ap: AnimationPlayer = e.get("anim")
	if ap == null:
		last_action = "%s vacío" % selected_slot
		return
	for n in candidates:
		if ap.has_animation(n):
			ap.play(n)
			if n != "stand" and ap.get_animation(n).loop_mode == Animation.LOOP_NONE:
				ap.queue("stand")
			last_action = "%s: %s" % [selected_slot, n]
			return
	last_action = "%s: sin %s" % [selected_slot, "/".join(candidates)]


func cycle_animation() -> void:
	var e: Dictionary = units.get(selected_slot, {})
	var ap: AnimationPlayer = e.get("anim")
	if ap == null:
		return
	var names: PackedStringArray = ap.get_animation_list()
	if names.has("RESET"):
		names.remove_at(names.find("RESET"))
	if names.is_empty():
		return
	var cur := names.find(ap.current_animation)
	var nxt := names[(cur + 1) % names.size()]
	ap.play(nxt)
	last_action = "%s: %s" % [selected_slot, nxt]


func trigger(kind: String) -> void:
	if camera.start_zoom(kind, target_local, hd_factor):
		last_action = "cámara %s → %s" % [kind, selected_slot]
		if kind == "Shock":
			camera.start_shake()


func _process(delta: float) -> void:
	for e in units.values():
		if e["anim"]:
			e["anim"].speed_scale = 0.0 if paused else 1.0
	if not paused:
		accumulator += delta
		while accumulator >= 1.0 / CameraModel.SWF_FPS:
			camera.tick()
			accumulator -= 1.0 / CameraModel.SWF_FPS
	apply_camera()


func apply_camera() -> void:
	ground.transform = camera.ground_transform()
	hud.visible = show_hud
	if battles.is_empty():
		status.text = "Sin datos: " + DATA_PATH
		return
	var b: Dictionary = battles[battle_index]
	var lines := PackedStringArray()
	lines.append("%s  (%d/%d)  ·  fondo HD %s  (ZoneBG %s | SkyBG %s)  ·  factor %.1f  ·  %s" % [
		b["combate"], battle_index + 1, battles.size(), b["zona_hd"], b["ZoneBG"], b["SkyBG"], hd_factor,
		"PAUSA" if paused else "30 Hz SWF"])
	var row := PackedStringArray()
	for slot in SLOT_ORDER:
		var info: Dictionary = units[slot]["info"] if units.has(slot) else {}
		var ap_name := String(info.get("apariencia", ""))
		var mark := "▶" if slot == selected_slot else " "
		row.append("%s%s %s" % [mark, slot.replace("player", "F"), ap_name if ap_name != "" else "—"])
	lines.append("  ".join(row))
	var sel: Dictionary = units.get(selected_slot, {}).get("info", {})
	lines.append("Seleccionado: %s · %s · %s  ·  última acción: %s" % [
		selected_slot, String(sel.get("nombre", "")), String(sel.get("model", "")), last_action])
	if not missing.is_empty():
		lines.append("FALTAN escenas: " + ", ".join(missing))
	status.text = "\n".join(lines)


func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed and not event.echo):
		return
	match event.physical_keycode:
		KEY_RIGHT: show_battle(battle_index + 1)
		KEY_LEFT: show_battle(battle_index - 1)
		KEY_HOME: show_battle(0)
		KEY_END: show_battle(battles.size() - 1)
		KEY_F1: select_slot("player1")
		KEY_F2: select_slot("player2")
		KEY_F3: select_slot("player3")
		KEY_F4: select_slot("player4")
		KEY_F5: select_slot("player5")
		KEY_F6: select_slot("player6")
		KEY_A: play_on_selected(["Attack", "attack2", "Attack_Stab", "Attack_Upper"])
		KEY_Q: play_on_selected(["cast", "Cast"])
		KEY_W: play_on_selected(["hit", "Hit"])
		KEY_E: play_on_selected(["dead", "Dead"])
		KEY_T: play_on_selected(["stand"])
		KEY_Y: cycle_animation()
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
		KEY_SPACE:
			paused = not paused
			accumulator = 0.0
		KEY_H: show_hud = not show_hud
		KEY_ESCAPE: get_tree().quit()
	apply_camera()
