/**
 * DroneScript.g4 - Gramática ANTLR para DroneScript
 * 
 * Especificación formal del lenguaje DroneScript.
 * 
 * FASE 1: Análisis Léxico (Lexer)
 * Este archivo define los tokens del lenguaje.
 * 
 * FASES FUTURAS: 
 * - Parser para análisis sintáctico
 * - Parser para construcción de AST
 * - Transpilador a Python
 * 
 * @author Proyecto Integrador - Programacion de sistemas de base 1
 * @version 1.0.0
 */

lexer grammar DroneScript;

// ===== CANALES (Skipear automáticamente) =====
channels {
    WHITESPACE_CHANNEL,
    COMMENTS_CHANNEL
}

// ===== WHITESPACE - Se ignora automáticamente =====
WS: [ \t\r\n]+ -> channel(HIDDEN);

// ===== COMENTARIOS =====
LINE_COMMENT: '//' ~[\r\n]* -> channel(HIDDEN);
BLOCK_COMMENT: '/*' .*? '*/' -> channel(HIDDEN);

// ===== PALABRAS CLAVE - CONTROL GENERAL =====
KW_DESPEGAR: 'despegar';
KW_ATERRIZAR: 'aterrizar';
KW_INICIAR_MISION: 'iniciar_mision';
KW_FINALIZAR_MISION: 'finalizar_mision';
KW_PAUSAR_MISION: 'pausar_mision';
KW_REANUDAR_MISION: 'reanudar_mision';
KW_REGRESAR_BASE: 'regresar_base';
KW_APAGAR: 'apagar';
KW_REINICIAR: 'reiniciar';
KW_DETENER: 'detener';
KW_EMERGENCIA: 'emergencia';

// ===== PALABRAS CLAVE - MOVIMIENTO =====
KW_MOVER: 'mover';
KW_AVANZAR: 'avanzar';
KW_RETROCEDER: 'retroceder';
KW_SUBIR: 'subir';
KW_BAJAR: 'bajar';
KW_ROTAR: 'rotar';
KW_ACELERAR: 'acelerar';
KW_FRENAR: 'frenar';
KW_MANTENER_ALTURA: 'mantener_altura';
KW_ORBITAR: 'orbitar';
KW_SEGUIR_OBJETIVO: 'seguir_objetivo';

// ===== PALABRAS CLAVE - DIRECCIONES =====
KW_NORTE: 'norte';
KW_SUR: 'sur';
KW_ESTE: 'este';
KW_OESTE: 'oeste';
KW_NORESTE: 'noreste';
KW_NOROESTE: 'noroeste';
KW_SURESTE: 'sureste';
KW_SUROESTE: 'suroeste';
KW_ARRIBA: 'arriba';
KW_ABAJO: 'abajo';
KW_IZQUIERDA: 'izquierda';
KW_DERECHA: 'derecha';

// ===== PALABRAS CLAVE - GPS Y NAVEGACIÓN =====
KW_COORDENADA: 'coordenada';
KW_GPS: 'gps';
KW_LATITUD: 'latitud';
KW_LONGITUD: 'longitud';
KW_DESTINO: 'destino';
KW_RUTA: 'ruta';
KW_WAYPOINT: 'waypoint';
KW_NAVEGAR: 'navegar';
KW_IR_A: 'ir_a';
KW_GUARDAR_RUTA: 'guardar_ruta';
KW_CARGAR_RUTA: 'cargar_ruta';

// ===== PALABRAS CLAVE - SENSORES =====
KW_ESCANEAR: 'escanear';
KW_SENSOR_DISTANCIA: 'sensor_distancia';
KW_SENSOR_TEMPERATURA: 'sensor_temperatura';
KW_SENSOR_HUMEDAD: 'sensor_humedad';
KW_SENSOR_GAS: 'sensor_gas';
KW_SENSOR_ULTRASONICO: 'sensor_ultrasonico';
KW_SENSOR_PROXIMIDAD: 'sensor_proximidad';
KW_SENSOR_LUZ: 'sensor_luz';
KW_LIDAR: 'lidar';
KW_CAMARA_TERMICA: 'camara_termica';
KW_GIROSCOPIO: 'giroscopio';
KW_ACELEROMETRO: 'acelerometro';

// ===== PALABRAS CLAVE - CÁMARA Y VISIÓN =====
KW_ACTIVAR_CAMARA: 'activar_camara';
KW_DESACTIVAR_CAMARA: 'desactivar_camara';
KW_TOMAR_FOTO: 'tomar_foto';
KW_GRABAR_VIDEO: 'grabar_video';
KW_DETENER_VIDEO: 'detener_video';
KW_ZOOM: 'zoom';
KW_ENFOCAR: 'enfocar';
KW_RECONOCER_OBJETO: 'reconocer_objeto';
KW_DETECTAR_PERSONA: 'detectar_persona';
KW_SEGUIR_MOVIMIENTO: 'seguir_movimiento';

// ===== PALABRAS CLAVE - BATERÍA Y ENERGÍA =====
KW_BATERIA: 'bateria';
KW_ENERGIA: 'energia';
KW_CARGAR: 'cargar';
KW_NIVEL_BATERIA: 'nivel_bateria';
KW_AHORRO_ENERGIA: 'ahorro_energia';
KW_TEMPERATURA_MOTOR: 'temperatura_motor';

// ===== PALABRAS CLAVE - CONDICIONALES Y CICLOS =====
KW_SI: 'si';
KW_ENTONCES: 'entonces';
KW_SINO: 'sino';
KW_FIN: 'fin';
KW_MIENTRAS: 'mientras';
KW_HACER: 'hacer';
KW_REPETIR: 'repetir';
KW_VECES: 'veces';
KW_PARA: 'para';
KW_DESDE: 'desde';
KW_HASTA: 'hasta';
KW_INCREMENTAR: 'incrementar';

// ===== PALABRAS CLAVE - COMUNICACIÓN =====
KW_CONECTAR: 'conectar';
KW_DESCONECTAR: 'desconectar';
KW_TRANSMITIR: 'transmitir';
KW_RECIBIR: 'recibir';
KW_ENVIAR_DATOS: 'enviar_datos';
KW_RECIBIR_DATOS: 'recibir_datos';
KW_WIFI: 'wifi';
KW_BLUETOOTH: 'bluetooth';
KW_RADIO: 'radio';

// ===== PALABRAS CLAVE - SEGURIDAD =====
KW_AUTENTICAR: 'autenticar';
KW_BLOQUEAR: 'bloquear';
KW_DESBLOQUEAR: 'desbloquear';
KW_ACTIVAR_ALARMA: 'activar_alarma';
KW_DESACTIVAR_ALARMA: 'desactivar_alarma';
KW_ZONA_SEGURA: 'zona_segura';
KW_EVITAR_COLISION: 'evitar_colision';

// ===== PALABRAS CLAVE - CLIMA Y ENTORNO =====
KW_VIENTO: 'viento';
KW_LLUVIA: 'lluvia';
KW_TEMPERATURA: 'temperatura';
KW_HUMEDAD: 'humedad';
KW_PRESION: 'presion';
KW_DETECTAR_OBSTACULO: 'detectar_obstaculo';

// ===== PALABRAS CLAVE - IA Y AUTONOMÍA =====
KW_MODO_AUTONOMO: 'modo_autonomo';
KW_APRENDIZAJE: 'aprendizaje';
KW_OBJETIVO: 'objetivo';
KW_PATRULLAR: 'patrullar';
KW_EXPLORAR: 'explorar';
KW_MAPEAR: 'mapear';
KW_RECONOCER_ROSTRO: 'reconocer_rostro';

// ===== PALABRAS CLAVE - TIPOS DE DATOS =====
KW_ENTERO: 'entero';
KW_DECIMAL: 'decimal';
KW_TEXTO: 'texto';
KW_BOOLEANO: 'booleano';
KW_VERDADERO: 'verdadero';
KW_FALSO: 'falso';

// ===== PALABRAS CLAVE - EVENTOS =====
KW_AL_DETECTAR: 'al_detectar';
KW_AL_COLISIONAR: 'al_colisionar';
KW_AL_BATERIA_BAJA: 'al_bateria_baja';
KW_AL_PERDER_SENAL: 'al_perder_senal';
KW_AL_INICIAR: 'al_iniciar';
KW_AL_ATERRIZAR: 'al_aterrizar';

// ===== OPERADORES ARITMÉTICOS =====
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
MOD: '%';

// ===== OPERADORES DE COMPARACIÓN =====
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';
EQ: '==';
NE: '!=';

// ===== OPERADORES LÓGICOS =====
AND: '&&';
OR: '||';
NOT: '!';

// ===== OPERADOR DE ASIGNACIÓN =====
ASSIGN: '=';

// ===== DELIMITADORES =====
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACKET: '[';
RBRACKET: ']';
SEMICOLON: ';';
COMMA: ',';
COLON: ':';

// ===== LITERALES =====
// Strings entre comillas dobles
STRING: '"' (~["\\\r\n] | '\\' .)* '"';

// Números flotantes (debe estar antes de INTEGER)
FLOAT: [0-9]+ '.' [0-9]+;

// Números enteros
INTEGER: [0-9]+;

// Identificadores (deve estar después de keywords)
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;

// Carácter desconocido
UNKNOWN: .;
