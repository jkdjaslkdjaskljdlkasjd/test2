extends SceneTree
## Test sin ventana (NO EJECUTADO todavía): godot --headless --path . -s res://tests/test_batallas001.gd
## Recorre los 99 combates y comprueba: fondo HD cargado, una unidad por slot ocupado, escala y espejo,
## animación 'stand' en reproducción, y que las unidades siguen la transformación del suelo en zoom y temblor.
const CameraModel = preload("res://SnowCamera.gd")

func _init() -> void:
	var fails := 0
	var checks := 0
	var viewer = load("res://BattleViewer.tscn").instantiate()
	root.add_child(viewer)
	await process_frame
	var n: int = viewer.battles.size()
	if n != 99:
		print("FALLO: combates=", n, " (esperado 99)"); fails += 1
	for i in n:
		viewer.show_battle(i)
		var b: Dictionary = viewer.battles[i]
		checks += 1
		if viewer.sky.texture == null or viewer.ground.texture == null:
			print("FALLO ", b["combate"], ": fondo sin textura"); fails += 1
		for slot in viewer.SLOT_ORDER:
			var info: Dictionary = b["slots"][slot]
			var e: Dictionary = viewer.units[slot]
			checks += 1
			if String(info["escena"]) == "":
				if e["node"] != null:
					print("FALLO ", b["combate"], " ", slot, ": debería estar vacío"); fails += 1
				continue
			var u: Node2D = e["node"]
			if u == null:
				print("FALLO ", b["combate"], " ", slot, ": falta ", info["escena"]); fails += 1
				continue
			var k := CameraModel.PX_PER_UNIT * (0.8 if String(info["model"]) == "MODEL5" else 1.0)
			var sx := float(viewer.data["slots"][slot]["xscale"])
			if absf(u.scale.x - k * sx) > 1e-4 or absf(u.scale.y - k) > 1e-4:
				print("FALLO ", b["combate"], " ", slot, ": escala ", u.scale); fails += 1
			var ap: AnimationPlayer = e["anim"]
			if ap == null or ap.current_animation != "stand":
				print("FALLO ", b["combate"], " ", slot, ": no reproduce stand"); fails += 1
	# anclaje al suelo durante zoom + temblor (combate 0, slot player1)
	viewer.show_battle(0)
	viewer.select_slot("player1")
	viewer.trigger("Shock")
	for t in 120:
		viewer.camera.tick()
		viewer.apply_camera()
		var holder: Node2D = viewer.units["player1"]["holder"]
		var expected: Vector2 = viewer.camera.ground_transform() * viewer.stage_to_px(viewer.slot_stage("player1"))
		checks += 1
		if holder.global_position.distance_to(expected) > 0.01:
			print("FALLO tick ", t, ": ", holder.global_position, " != ", expected); fails += 1
	print("BATALLAS-001: %d comprobaciones, %d fallos" % [checks, fails])
	quit(1 if fails else 0)
