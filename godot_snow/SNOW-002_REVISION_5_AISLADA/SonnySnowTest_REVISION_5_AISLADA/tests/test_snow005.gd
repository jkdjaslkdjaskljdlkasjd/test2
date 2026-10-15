extends SceneTree
## REVISION 5: modelo original en reposo en el slot player1.
## Comprueba: escena cargada, escala (1 u SWF = PX_PER_UNIT px), origen = origen del slot, anclaje del apoyo real
## (pies) pegado al suelo en cada tick de zoom (3 ataques x 2 factores) y de temblor, B oculta solo las guias.

const CameraModel = preload("res://SnowCamera.gd")
const Battle = preload("res://SnowBattleTest.gd")

var scene: Node2D
var failures := 0
var checks := 0

func check(ok: bool, message: String) -> void:
	checks += 1
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

func feet_from_marker() -> Vector2:
	var marker: Node2D = scene.slots_layer.get_node(Battle.REAL_MODEL_SLOT)
	return marker.get_global_transform() * Vector2(0.0, Battle.REAL_FEET_Y_SWF * CameraModel.PX_PER_UNIT)

func feet_from_model() -> Vector2:
	return scene.real_model.get_global_transform() * Vector2(0.0, Battle.REAL_FEET_Y_SWF)

func check_anchor(tag: String) -> void:
	scene.apply_camera()
	var g: Transform2D = scene.ground.get_global_transform()
	var marker: Node2D = scene.slots_layer.get_node(Battle.REAL_MODEL_SLOT)
	check(scene.real_model.global_position.distance_to(g * marker.position) < 0.01, tag + ": origen del modelo = origen del slot")
	check(feet_from_model().distance_to(feet_from_marker()) < 0.01, tag + ": apoyo real del modelo = linea verde")
	var expected_scale: float = g.get_scale().x * CameraModel.PX_PER_UNIT
	check(absf(scene.real_model.get_global_transform().get_scale().x - expected_scale) < 0.0001, tag + ": escala = suelo x PX_PER_UNIT")

func run() -> void:
	scene = load("res://SnowBattleTest.tscn").instantiate()
	root.add_child(scene)
	scene.paused = true
	check(scene.slots_layer.get_child_count() == 6, "Siguen existiendo 6 marcadores")
	check(scene.real_model != null, "Modelo original instanciado")
	if scene.real_model == null:
		print("SNOW005_TESTS checks=", checks, " failures=", failures)
		quit(1)
		return
	check(scene.units_layer.get_parent() == scene.ground, "UnitsLayer cuelga de GroundLayer")
	check(scene.real_model_anim != null and scene.real_model_anim.current_animation == "stand", "Reproduce 'stand'")
	check(absf(scene.real_model.scale.x - CameraModel.PX_PER_UNIT) < 0.0001, "Escala local = PX_PER_UNIT (aliado, sin espejo)")
	check_anchor("reposo")
	var cases := 0
	for factor in [0.5, 1.0]:
		for attack in [KEY_1, KEY_2, KEY_3]:
			key(KEY_R)
			scene.hd_factor = factor
			key(KEY_F1)
			key(attack)
			for t in range(90):
				scene.camera.tick()
				check_anchor("zoom f=%s t=%d" % [factor, t])
			cases += 1
	key(KEY_R)
	key(KEY_S)
	for t in range(60):
		scene.camera.tick()
		check_anchor("temblor t=%d" % t)
	cases += 1
	key(KEY_B)
	check(not scene.slots_layer.visible, "B oculta las guias")
	check(scene.units_layer.is_visible_in_tree(), "B no oculta al personaje")
	key(KEY_B)
	print("SNOW005_TESTS cases=", cases, " checks=", checks, " failures=", failures)
	quit(1 if failures else 0)
