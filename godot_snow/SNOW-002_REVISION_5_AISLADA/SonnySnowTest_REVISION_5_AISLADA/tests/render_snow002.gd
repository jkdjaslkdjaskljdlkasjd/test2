extends SceneTree
var scene: Node2D
func _initialize() -> void:
	call_deferred("run")
func capture(label: String) -> void:
	scene.apply_camera()
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var img = root.get_texture().get_image()
	img.save_png("res://validation/revision4/" + label + ".png")
func run() -> void:
	DirAccess.make_dir_recursive_absolute("res://validation/revision4")
	scene = load("res://SnowBattleTest.tscn").instantiate()
	root.add_child(scene)
	scene.paused = true
	await process_frame
	await process_frame
	var help: Label = scene.get_node("HUD/Panel/Help")
	for bname in scene.top_bars_data:
		var b: Dictionary = scene.top_bars_data[bname]
		var bar_rect := Rect2(scene.stage_to_px(Vector2(b["x"] + b["xMin"], b["y"] + b["yMin"])),Vector2(b["w"],b["h"]) * scene.CameraModel.PX_PER_UNIT)
		print("HUD_INTERSECTION ",bname," panel=",bar_rect.intersects(scene.get_node("HUD/Panel").get_global_rect())," help=",bar_rect.intersects(help.get_global_rect())," status=",bar_rect.intersects(scene.status.get_global_rect()))
	print("HELP_RECT ",help.get_global_rect()," MIN=",help.get_minimum_size())
	for holder in scene.slots_layer.get_children():
		var d: Dictionary = scene.slots_data[holder.name]
		var expected_y: float = (d["yMin"]+d["h"]) * scene.CameraModel.PX_PER_UNIT
		var line: ColorRect = holder.get_child(3)
		assert(absf(line.position.y + line.size.y/2.0 - expected_y) < 0.001)
	print("F1_BOTTOM_LINES 6 correctas")
	await capture("01_interfaz")
	scene.get_node("HUD/Panel").hide()
	scene.get_node("HUD/Status").hide()
	await capture("02_guias")
	for factor in [0.5, 1.0]:
		scene.camera.reset()
		scene.hd_factor = factor
		scene.select_slot_target("player3")
		scene.trigger("Shock")
		for i in range(10): scene.camera.tick()
		await capture("03_shock_" + str(factor))
	print("RENDER_REVISION3 captures=4")
	quit()
