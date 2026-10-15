extends SceneTree

var scene: Node2D
var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func key(code: int) -> void:
	var event := InputEventKey.new()
	event.pressed = true
	event.physical_keycode = code
	scene._unhandled_input(event)

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	scene = load("res://SnowBattleTest.tscn").instantiate()
	root.add_child(scene)
	scene.paused = true
	check(scene.slots_layer.get_child_count() == 6, "Six markers exist")
	var fixed_hud: Transform2D = scene.hud_guide.get_global_transform()
	var expects_json := FileAccess.file_exists("res://assets/battle_layout_217.json")
	check(scene.slots_pos_swf == (6 if expects_json else 0), "Slot position provenance")
	check(scene.top_pos_swf == (6 if expects_json else 0), "Top bar position provenance")
	check(scene.bot_pos_swf == (9 if expects_json else 0), "Bottom position provenance")
	for name in ["krinToMove2", "moveSelectBoomer", "__hdSkipX"]:
		check(scene.bottom_panel_data[name]["size_src"] == "PROV", "Null dimensions remain provisional")
		check(scene.format_provenance_badge(scene.bottom_panel_data[name]).contains("tam:PROV"), "Provisional size badge")
	if not expects_json:
		check(scene.bottom_panel_data["combatScript"]["size_src"] == "PROV", "CombatScript fallback size")
	var keys := [KEY_F1, KEY_F2, KEY_F3, KEY_F4, KEY_F5, KEY_F6]
	var count := 0
	for i in range(6):
		for factor in [0.5, 1.0]:
			for attack in [KEY_1, KEY_2, KEY_3]:
				key(KEY_R)
				scene.hd_factor = factor
				key(keys[i])
				check(scene.selected_target_label == "player" + str(i + 1), "F1-F6 selects slot")
				key(attack)
				for tick in range(10): scene.camera.tick()
				scene.apply_camera()
				check(scene.camera.b_scale > 1.0, "Attack scales the floor")
				check(scene.sky.transform == Transform2D.IDENTITY, "Sky stays fixed")
				check(scene.hud_guide.get_global_transform() == fixed_hud, "HUD stays fixed")
				for marker in scene.slots_layer.get_children():
					var expected: Vector2 = scene.ground.get_global_transform() * marker.position
					check(marker.global_position.distance_to(expected) < 0.001, "Marker follows floor")
				for tick in range(80): scene.camera.tick()
				check(not scene.camera.zoom_active and not scene.camera.shake_active, "Effects end")
				count += 1
	key(KEY_B)
	check(not scene.slots_layer.visible and not scene.hud_guide.visible, "B hides guides")
	key(KEY_B)
	check(scene.slots_layer.visible and scene.hud_guide.visible, "B shows guides")
	print("SNOW002_TESTS cases=", count, " failures=", failures)
	print("LAYOUT_COUNTS slots=", scene.slots_pos_swf, " top=", scene.top_pos_swf, " bottom=", scene.bot_pos_swf)
	quit(1 if failures else 0)
