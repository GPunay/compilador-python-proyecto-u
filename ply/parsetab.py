
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '727D47BC26545E4F16879A816B988A76'
    
_lr_action_items = {'TIPO':([0,2,3,4,5,6,16,26,40,41,46,47,48,51,52,65,66,67,68,69,75,76,77,78,79,89,90,91,92,93,],[7,-1,-2,-3,-4,-5,-13,7,-18,-14,-15,-16,-17,7,-6,-12,-8,-9,-10,-11,-29,-7,-44,-45,-46,7,-37,-30,7,-32,]),'RESERV':([0,2,3,4,5,6,16,26,40,41,46,47,48,51,52,65,66,67,68,69,75,76,77,78,79,89,90,91,92,93,],[9,-1,-2,-3,-4,-5,-13,9,-18,-14,-15,-16,-17,9,-6,-12,-8,-9,-10,-11,84,-7,-44,-45,-46,9,-37,-30,9,-32,]),'VAR':([0,2,3,4,5,6,7,11,13,15,16,24,26,27,40,41,42,43,44,45,46,47,48,51,52,58,59,60,61,62,63,64,65,66,67,68,69,75,76,77,78,79,80,89,90,91,92,93,],[8,-1,-2,-3,-4,-5,10,17,34,35,-13,34,8,34,-18,-14,34,34,34,34,-15,-16,-17,8,-6,34,-38,-39,-40,-41,-42,-43,-12,-8,-9,-10,-11,-29,-7,-44,-45,-46,34,8,-37,-30,8,-32,]),'$end':([1,2,3,4,5,6,16,40,41,46,47,48,65,66,67,68,69,75,77,78,79,90,91,93,],[0,-1,-2,-3,-4,-5,-13,-18,-14,-15,-16,-17,-12,-8,-9,-10,-11,-29,-44,-45,-46,-37,-30,-32,]),'LLLAVE':([2,3,4,5,6,16,40,41,46,47,48,50,51,52,65,66,67,68,69,75,76,77,78,79,90,91,92,93,],[-1,-2,-3,-4,-5,-13,-18,-14,-15,-16,-17,75,-31,-6,-12,-8,-9,-10,-11,-29,-7,-44,-45,-46,-37,-30,93,-32,]),'EQUAL':([8,10,],[11,15,]),'LPAREN':([9,11,13,15,24,27,42,43,44,45,56,57,58,59,60,61,62,63,64,80,],[13,24,27,24,24,24,24,24,24,24,80,80,24,-38,-39,-40,-41,-42,-43,24,]),'POINTCOMA':([10,17,18,19,20,21,22,23,25,33,34,35,36,37,38,39,53,54,55,70,71,72,73,74,84,],[16,40,41,46,47,48,-23,-24,-26,-27,-28,65,66,67,68,69,77,78,79,-19,-20,-21,-22,-25,90,]),'CHAR':([11,13,15,],[19,29,37,]),'STRING':([11,13,15,],[20,28,38,]),'BOOL':([11,13,15,24,27,42,43,44,45,58,59,60,61,62,63,64,80,],[21,33,39,33,33,33,33,33,33,33,-38,-39,-40,-41,-42,-43,33,]),'NUMBER':([11,13,15,24,27,42,43,44,45,58,59,60,61,62,63,64,80,],[23,23,23,23,23,23,23,23,23,23,-38,-39,-40,-41,-42,-43,23,]),'FLOAT':([11,13,15,24,27,42,43,44,45,58,59,60,61,62,63,64,80,],[25,25,25,25,25,25,25,25,25,25,-38,-39,-40,-41,-42,-43,25,]),'RLLAVE':([12,14,84,86,87,88,],[26,-33,89,-34,-35,-36,]),'SUM':([17,18,21,22,23,25,30,32,33,34,35,36,39,49,70,71,72,73,74,],[-28,42,-27,-23,-24,-26,42,-23,-27,-28,-28,42,-27,42,-19,-20,-21,-22,-25,]),'REST':([17,18,21,22,23,25,30,32,33,34,35,36,39,49,70,71,72,73,74,],[-28,43,-27,-23,-24,-26,43,-23,-27,-28,-28,43,-27,43,-19,-20,-21,-22,-25,]),'MULT':([17,18,21,22,23,25,30,32,33,34,35,36,39,49,70,71,72,73,74,],[-28,44,-27,-23,-24,-26,44,-23,-27,-28,-28,44,-27,44,44,44,-21,-22,-25,]),'DIV':([17,18,21,22,23,25,30,32,33,34,35,36,39,49,70,71,72,73,74,],[-28,45,-27,-23,-24,-26,45,-23,-27,-28,-28,45,-27,45,45,45,-21,-22,-25,]),'RPAREN':([22,23,25,28,29,30,32,33,34,49,70,71,72,73,74,81,82,83,88,],[-23,-24,-26,53,54,55,-23,-27,-28,74,-19,-20,-21,-22,-25,86,87,88,-36,]),'MAYOR':([23,25,32,33,34,74,85,],[-24,-26,59,-27,-28,-25,59,]),'MENOR':([23,25,32,33,34,74,85,],[-24,-26,60,-27,-28,-25,60,]),'MAEQUAL':([23,25,32,33,34,74,85,],[-24,-26,61,-27,-28,-25,61,]),'MEEQUAL':([23,25,32,33,34,74,85,],[-24,-26,62,-27,-28,-25,62,]),'DOBLEEQUAL':([23,25,32,33,34,74,85,],[-24,-26,63,-27,-28,-25,63,]),'DIF':([23,25,32,33,34,74,85,],[-24,-26,64,-27,-28,-25,64,]),'AND':([31,88,],[56,-36,]),'OR':([31,88,],[57,-36,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'bloque':([0,26,51,89,92,],[1,52,76,52,76,]),'declaracion':([0,26,51,89,92,],[2,2,2,2,2,]),'condicional':([0,26,51,89,92,],[3,3,3,3,3,]),'ciclo':([0,26,51,89,92,],[4,4,4,4,4,]),'imprimir':([0,26,51,89,92,],[5,5,5,5,5,]),'asignacion':([0,26,51,89,92,],[6,6,6,6,6,]),'condiciones':([9,],[12,]),'logica':([9,13,56,57,],[14,31,81,82,]),'expresion':([11,13,15,24,27,42,43,44,45,],[18,30,36,49,49,70,71,72,73,]),'factor':([11,13,15,24,27,42,43,44,45,58,80,],[22,32,22,22,32,22,22,22,22,83,85,]),'fin_con':([26,],[50,]),'bloques':([26,89,],[51,92,]),'op_log':([32,85,],[58,58,]),'fin_con_else':([89,],[91,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> bloque","S'",1,None,None,None),
  ('bloque -> declaracion','bloque',1,'p_bloque','analisis_semantico_operadores.py',97),
  ('bloque -> condicional','bloque',1,'p_bloque','analisis_semantico_operadores.py',98),
  ('bloque -> ciclo','bloque',1,'p_bloque','analisis_semantico_operadores.py',99),
  ('bloque -> imprimir','bloque',1,'p_bloque','analisis_semantico_operadores.py',100),
  ('bloque -> asignacion','bloque',1,'p_bloque','analisis_semantico_operadores.py',101),
  ('bloques -> bloque','bloques',1,'p_bloques','analisis_semantico_operadores.py',108),
  ('bloques -> bloques bloque','bloques',2,'p_bloques_mult','analisis_semantico_operadores.py',115),
  ('declaracion -> TIPO VAR EQUAL expresion POINTCOMA','declaracion',5,'p_declaracion','analisis_semantico_operadores.py',122),
  ('declaracion -> TIPO VAR EQUAL CHAR POINTCOMA','declaracion',5,'p_declaracion','analisis_semantico_operadores.py',123),
  ('declaracion -> TIPO VAR EQUAL STRING POINTCOMA','declaracion',5,'p_declaracion','analisis_semantico_operadores.py',124),
  ('declaracion -> TIPO VAR EQUAL BOOL POINTCOMA','declaracion',5,'p_declaracion','analisis_semantico_operadores.py',125),
  ('declaracion -> TIPO VAR EQUAL VAR POINTCOMA','declaracion',5,'p_declaracion','analisis_semantico_operadores.py',126),
  ('declaracion -> TIPO VAR POINTCOMA','declaracion',3,'p_declaracion','analisis_semantico_operadores.py',127),
  ('asignacion -> VAR EQUAL expresion POINTCOMA','asignacion',4,'p_asignacion','analisis_semantico_operadores.py',196),
  ('asignacion -> VAR EQUAL CHAR POINTCOMA','asignacion',4,'p_asignacion','analisis_semantico_operadores.py',197),
  ('asignacion -> VAR EQUAL STRING POINTCOMA','asignacion',4,'p_asignacion','analisis_semantico_operadores.py',198),
  ('asignacion -> VAR EQUAL BOOL POINTCOMA','asignacion',4,'p_asignacion','analisis_semantico_operadores.py',199),
  ('asignacion -> VAR EQUAL VAR POINTCOMA','asignacion',4,'p_asignacion','analisis_semantico_operadores.py',200),
  ('expresion -> expresion SUM expresion','expresion',3,'p_expresion','analisis_semantico_operadores.py',276),
  ('expresion -> expresion REST expresion','expresion',3,'p_expresion','analisis_semantico_operadores.py',277),
  ('expresion -> expresion MULT expresion','expresion',3,'p_expresion','analisis_semantico_operadores.py',278),
  ('expresion -> expresion DIV expresion','expresion',3,'p_expresion','analisis_semantico_operadores.py',279),
  ('expresion -> factor','expresion',1,'p_exp_factor','analisis_semantico_operadores.py',304),
  ('factor -> NUMBER','factor',1,'p_factor_int','analisis_semantico_operadores.py',310),
  ('factor -> LPAREN expresion RPAREN','factor',3,'p_facto_exp','analisis_semantico_operadores.py',314),
  ('factor -> FLOAT','factor',1,'p_factor_float','analisis_semantico_operadores.py',318),
  ('factor -> BOOL','factor',1,'p_factor_bool','analisis_semantico_operadores.py',322),
  ('factor -> VAR','factor',1,'p_factor_var','analisis_semantico_operadores.py',327),
  ('condicional -> RESERV condiciones RLLAVE fin_con LLLAVE','condicional',5,'p_condicional','analisis_semantico_operadores.py',341),
  ('condicional -> RESERV condiciones RLLAVE fin_con LLLAVE RESERV RLLAVE fin_con_else','condicional',8,'p_condicional','analisis_semantico_operadores.py',342),
  ('fin_con -> bloques','fin_con',1,'p_fin_condi','analisis_semantico_operadores.py',360),
  ('fin_con_else -> bloques LLLAVE','fin_con_else',2,'p_fin_condi_else','analisis_semantico_operadores.py',365),
  ('condiciones -> logica','condiciones',1,'p_codiciones','analisis_semantico_operadores.py',369),
  ('condiciones -> LPAREN logica AND logica RPAREN','condiciones',5,'p_codiciones','analisis_semantico_operadores.py',370),
  ('condiciones -> LPAREN logica OR logica RPAREN','condiciones',5,'p_codiciones','analisis_semantico_operadores.py',371),
  ('logica -> LPAREN factor op_log factor RPAREN','logica',5,'p_operacion_logica','analisis_semantico_operadores.py',376),
  ('ciclo -> RESERV condiciones RLLAVE fin_con LLLAVE RESERV POINTCOMA','ciclo',7,'p_while','analisis_semantico_operadores.py',420),
  ('op_log -> MAYOR','op_log',1,'p_op_logico','analisis_semantico_operadores.py',436),
  ('op_log -> MENOR','op_log',1,'p_op_logico','analisis_semantico_operadores.py',437),
  ('op_log -> MAEQUAL','op_log',1,'p_op_logico','analisis_semantico_operadores.py',438),
  ('op_log -> MEEQUAL','op_log',1,'p_op_logico','analisis_semantico_operadores.py',439),
  ('op_log -> DOBLEEQUAL','op_log',1,'p_op_logico','analisis_semantico_operadores.py',440),
  ('op_log -> DIF','op_log',1,'p_op_logico','analisis_semantico_operadores.py',441),
  ('imprimir -> RESERV LPAREN STRING RPAREN POINTCOMA','imprimir',5,'p_print','analisis_semantico_operadores.py',448),
  ('imprimir -> RESERV LPAREN CHAR RPAREN POINTCOMA','imprimir',5,'p_print','analisis_semantico_operadores.py',449),
  ('imprimir -> RESERV LPAREN expresion RPAREN POINTCOMA','imprimir',5,'p_print','analisis_semantico_operadores.py',450),
]
