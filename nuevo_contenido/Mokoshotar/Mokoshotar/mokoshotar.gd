extends Node2D
## Mokoshotar (I41, rig MODEL5) con animaciones y sonidos nuevos.
## - atacar(critico): "Attack_Moko" (Mordisco Glacial). Sonido aleatorio entre 2 (SonidoAtaque) en el fotograma 7;
##   el mordisco impacta en el fotograma 13. Si es crítico, suena el aullido (SonidoCritico) en el impacto.
## - lanzar_hechizo(critico): "cast_Moko" (Aullido de Escarcha). Sonido aleatorio entre 2 (SonidoHechizo) en el
##   fotograma 9; la escarcha se libera en el fotograma 16.
## Al terminar, ambas vuelven a "stand". Teclas de prueba: 1 ataque, 2 ataque crítico, 3 hechizo, 4 hechizo crítico.

const FPS := 30.0
const IMPACTO_ATAQUE := 13.0 / FPS
const LIBERACION_HECHIZO := 16.0 / FPS

signal impacto(critico: bool)

@onready var anim: AnimationPlayer = $AnimationPlayer
@onready var sonido_critico: AudioStreamPlayer2D = $SonidoCritico

func _ready() -> void:
	anim.animation_finished.connect(_al_terminar)
	anim.play("stand")

func atacar(critico: bool = false) -> void:
	anim.play("Attack_Moko")
	await get_tree().create_timer(IMPACTO_ATAQUE).timeout
	impacto.emit(critico)
	if critico:
		sonido_critico.play()

func lanzar_hechizo(critico: bool = false) -> void:
	anim.play("cast_Moko")
	await get_tree().create_timer(LIBERACION_HECHIZO).timeout
	impacto.emit(critico)
	if critico:
		sonido_critico.play()

func _al_terminar(nombre: StringName) -> void:
	if nombre in [&"Attack_Moko", &"cast_Moko", &"runback", &"hit", &"cast", &"outofstun"]:
		anim.play("stand")

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: atacar(false)
			KEY_2: atacar(true)
			KEY_3: lanzar_hechizo(false)
			KEY_4: lanzar_hechizo(true)
