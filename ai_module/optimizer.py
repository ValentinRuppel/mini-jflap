import sys
import json
import random
import copy
import math
import warnings
import time

warnings.filterwarnings("ignore")

class AutomataOracle:
    def __init__(self, definicion):
        self.tipo = definicion.get('tipo', 'DFA').upper()
        self.transiciones = definicion.get('transiciones', {})
        self.estado_inicial = definicion.get('estado_inicial', '')
        self.estados_finales = set(definicion.get('estados_finales', []))
        self.alfabeto = definicion.get('alfabeto', ['0', '1']) 

    def simular(self, cadena):
        if self.tipo in ['AP', 'PDA']: return self.simular_pila(cadena)
        return self.simular_finito(cadena)

    def simular_finito(self, cadena):
        estados_actuales = {self.estado_inicial}
        for simbolo in cadena:
            proximos = set()
            for est in estados_actuales:
                if est not in self.transiciones: continue
                rules = self.transiciones[est]
                dests = []
                if isinstance(rules, dict): dests = rules.get(simbolo, [])
                elif isinstance(rules, list):
                    try: 
                        idx = self.alfabeto.index(simbolo)
                        if idx < len(rules): dests = rules[idx]
                    except: pass
                if not isinstance(dests, list): dests = [dests]
                for d in dests:
                    if isinstance(d, str): proximos.add(d)
            estados_actuales = proximos
            if not estados_actuales: break 
        for est in estados_actuales:
            if est in self.estados_finales: return True
        return False

    def simular_pila(self, cadena):
        configuraciones = {(self.estado_inicial, ())} 
        for simbolo in cadena:
            nuevas = set()
            try: idx = self.alfabeto.index(simbolo)
            except: return False
            for est, pila in configuraciones:
                if est not in self.transiciones: continue
                rules = self.transiciones[est]
                if idx >= len(rules): continue
                moves = rules[idx]
                if not isinstance(moves, list): continue
                for mov in moves:
                    if not isinstance(mov, dict): continue
                    pila_new = list(pila)
                    if mov.get('pop') != 'λ':
                        if not pila_new or pila_new[-1] != mov['pop']: continue
                        pila_new.pop()
                    if mov.get('push') != 'λ': pila_new.append(mov['push'])
                    if len(pila_new) < 20: nuevas.add((mov['dest'], tuple(pila_new)))
            configuraciones = nuevas
            if not configuraciones: return False
        for est, _ in configuraciones:
            if est in self.estados_finales: return True
        return False

    def generar_dataset(self, cantidad=100):
        data = []
        data.append({'input': "", 'label': self.simular("")})
        for c in self.alfabeto: data.append({'input': c, 'label': self.simular(c)})
        intentos = 0
        while len(data) < cantidad and intentos < cantidad * 5:
            l = random.randint(1, 10)
            s = "".join(random.choice(self.alfabeto) for _ in range(l))
            if not any(d['input'] == s for d in data):
                data.append({'input': s, 'label': self.simular(s)})
            intentos += 1
        return data

class BaseOptimizer:
    def __init__(self, original):
        # 1. Normalizamos el autómata antes de hacer cualquier cosa
        self.original = self.normalizar_transiciones(original)
        
        # 2. Iniciamos el Oráculo con la versión ya normalizada
        self.oracle = AutomataOracle(self.original)
        self.dataset = self.oracle.generar_dataset(300)

    def fitness(self, candidato):
        """
        Función Monoobjetivo: f(A) = Cantidad de estados.
        Restricción rígida: El lenguaje debe ser idéntico.
        """
        if not self.validar(candidato):
            return 999999  # Penalización masiva (Infinito práctico)
        return len(candidato['estados'])

    def validar(self, candidato):
        cand_oracle = AutomataOracle(candidato)
        for caso in self.dataset:
            if cand_oracle.simular(caso['input']) != caso['label']:
                return False
        return True

    def mutar_fusion(self, automata):
        """ Movimiento de mejora: reduce estados. """
        if len(automata['estados']) < 2: return automata
        q1, q2 = random.sample(automata['estados'], 2)
        return self.fusionar_estados(automata, q1, q2)

    def mutar_split(self, automata):
        """ Movimiento de exploración: aumenta estados (para SA). """
        nuevo = copy.deepcopy(automata)
        if not nuevo['estados']: return nuevo
        q_target = random.choice(nuevo['estados'])
        nuevo_nombre = f"s{len(nuevo['estados'])}n"
        nuevo['estados'].append(nuevo_nombre)
        # Copiamos transiciones del original al nuevo para mantener coherencia inicial
        if q_target in nuevo['transiciones']:
            nuevo['transiciones'][nuevo_nombre] = copy.deepcopy(nuevo['transiciones'][q_target])
        return nuevo

    def fusionar_estados(self, automata, q1, q2):
        # ... (Tu lógica de fusión original optimizada)
        nuevo = copy.deepcopy(automata)
        trans = nuevo['transiciones']
        
        def replace_state(obj):
            if isinstance(obj, list): return [replace_state(x) for x in obj]
            if isinstance(obj, dict): return {k: replace_state(v) for k,v in obj.items()}
            return q1 if obj == q2 else obj

        for k in list(trans.keys()):
            trans[k] = replace_state(trans[k])
        
        if nuevo['estado_inicial'] == q2: nuevo['estado_inicial'] = q1
        if q2 in nuevo['estados_finales']:
            if q1 not in nuevo['estados_finales']: nuevo['estados_finales'].append(q1)
            nuevo['estados_finales'].remove(q2)
        
        if q2 in nuevo['estados']: nuevo['estados'].remove(q2)
        if q2 in trans:
            # Transferir transiciones de q2 a q1 si q1 no las tenía (importante para NFA/AP)
            del trans[q2]
        return nuevo
    
    def mutar_cruce(self, padre1, padre2):
        """
        Operador de Crossover: Combina la topología del padre1 con las 
        transiciones del padre2, asegurando coherencia estructural.
        """
        hijo = copy.deepcopy(padre1)
        estados_p1 = hijo['estados']
        estados_p2 = padre2['estados']

        # 1. Intercambio de material genético (Transiciones)
        for estado in estados_p1:
            # Si el estado existe en ambos padres, 50% de prob de heredar la lógica del Padre 2
            if estado in estados_p2 and random.random() > 0.5:
                if estado in padre2['transiciones']:
                    hijo['transiciones'][estado] = copy.deepcopy(padre2['transiciones'][estado])
                    
                    # Limpieza táctica: Evitar transiciones duplicadas ("doble el A")
                    if isinstance(hijo['transiciones'][estado], dict):
                        for simbolo, destinos in hijo['transiciones'][estado].items():
                            if isinstance(destinos, list):
                                hijo['transiciones'][estado][simbolo] = list(set(destinos))

        # 2. Fase de Reparación (Crucial para no romper el programa)
        # Si el Padre 2 introdujo una transición hacia un estado que el Hijo no tiene,
        # reescribimos ese destino hacia un "estado seguro" (ej: el estado actual o el inicial).
        for origen, reglas in list(hijo['transiciones'].items()):
            if isinstance(reglas, dict):
                for simbolo, destinos in list(reglas.items()):
                    if isinstance(destinos, list):
                        destinos_validos = [d for d in destinos if d in estados_p1]
                        hijo['transiciones'][origen][simbolo] = destinos_validos
                    elif isinstance(destinos, str) and destinos not in estados_p1:
                        hijo['transiciones'][origen][simbolo] = origen # Loop local seguro

        return hijo
    def normalizar_transiciones(self, automata):
        """
        Convierte cualquier formato de transiciones (listas por índice o diccionarios parciales)
        en un contrato estricto: { estado_origen: { simbolo: [estado_destino_1, ...] } }
        """
        norm_automata = copy.deepcopy(automata)
        trans_originales = norm_automata.get('transiciones', {})
        alfabeto = norm_automata.get('alfabeto', [])
        
        trans_normalizadas = {}
        
        for estado, reglas in trans_originales.items():
            trans_normalizadas[estado] = {}
            
            # Si viene del frontend como diccionario
            if isinstance(reglas, dict):
                for simbolo, destinos in reglas.items():
                    if not isinstance(destinos, list): destinos = [destinos]
                    trans_normalizadas[estado][simbolo] = destinos
                    
            # Si viene del frontend como array (lista de listas/strings indexada por el alfabeto)
            elif isinstance(reglas, list):
                for idx, destinos in enumerate(reglas):
                    if idx < len(alfabeto):
                        simbolo = alfabeto[idx]
                        if not isinstance(destinos, list): destinos = [destinos]
                        # Filtramos vacíos
                        destinos_validos = [d for d in destinos if d] 
                        if destinos_validos:
                            trans_normalizadas[estado][simbolo] = destinos_validos

        norm_automata['transiciones'] = trans_normalizadas
        return norm_automata
    
    def limpiar_duplicados(self, automata):
        """
        Elimina destinos redundantes para que el frontend no dibuje etiquetas dobles.
        """
        limpio = copy.deepcopy(automata)
        transiciones = limpio.get('transiciones', {})
        
        for estado, reglas in transiciones.items():
            if isinstance(reglas, dict):
                for simbolo, destinos in reglas.items():
                    if isinstance(destinos, list):
                        # Solo procesamos si los destinos son strings (nombres de estados)
                        if all(isinstance(x, str) for x in destinos):
                            # list(set()) elimina los duplicados automáticamente
                            transiciones[estado][simbolo] = sorted(list(set(destinos)))
                            
        return limpio

# --- TRAYECTORIA: SIMULATED ANNEALING ---
class AnnealingOptimizer(BaseOptimizer):
    def ejecutar(self):
        actual = self.original
        mejor = self.original
        t = 100.0
        alfa = 0.95

        while t > 0.1:
            # En SA, el vecino puede ser mejor O peor
            tipo_mutacion = random.random()
            if tipo_mutacion > 0.3:
                vecino = self.mutar_fusion(actual)
            else:
                vecino = self.mutar_split(actual)
            
            f_actual = self.fitness(actual)
            f_vecino = self.fitness(vecino)
            
            delta = f_vecino - f_actual

            # Si mejora (delta < 0) o por probabilidad de Boltzmann
            if delta < 0 or random.random() < math.exp(-delta / t):
                actual = vecino
                if self.fitness(actual) < self.fitness(mejor):
                    mejor = actual
            
            t *= alfa
        mejor = self.limpiar_duplicados(mejor)
        return mejor

# --- POBLACIONAL: ALGORITMO GENÉTICO ---
class GeneticOptimizer(BaseOptimizer):
    def ejecutar(self):
        poblacion = [copy.deepcopy(self.original) for _ in range(10)]
        mejor_global = self.original
        
        for gen in range(20):
            # 1. Evaluación y Ordenamiento
            poblacion.sort(key=lambda x: self.fitness(x))
            
            if self.fitness(poblacion[0]) < self.fitness(mejor_global):
                mejor_global = poblacion[0]

            # 2. Selección y Nueva Generación (Elitismo)
            nueva_gen = poblacion[:2] 
            
            # 3. Cruzamiento y Mutación
            while len(nueva_gen) < 10:
                padreA = random.choice(poblacion[:5]) # Torneo simple: elegimos de los mejores
                
                # 70% de probabilidad de Cruzamiento
                if random.random() < 0.7:
                    padreB = random.choice(poblacion[:5])
                    hijo = self.mutar_cruce(padreA, padreB)
                else:
                    hijo = copy.deepcopy(padreA)

                # 30% de probabilidad de Mutación (Fusión) sobre el hijo resultante
                if random.random() < 0.3:
                    hijo = self.mutar_fusion(hijo)
                
                nueva_gen.append(hijo)
                
            poblacion = nueva_gen
        mejor_global = self.limpiar_duplicados(mejor_global)
        return mejor_global

# --- MAIN ---
def main():
    try:
        start_time = time.time()
        input_data = sys.stdin.read().strip()
        if not input_data and len(sys.argv) > 1: input_data = sys.argv[1]
        if not input_data: return

        data = json.loads(input_data)
        definicion = data.get('json_definicion', data.get('automata', data))
        
        # LEER ALGORITMO ELEGIDO
        algoritmo_elegido = data.get('algoritmo', 'genetico') # default genético

        if 'tipo' not in definicion: definicion['tipo'] = data.get('tipo', 'DFA')

        optimizer = None
        if algoritmo_elegido == 'sa':
            optimizer = AnnealingOptimizer(definicion)
        else:
            optimizer = GeneticOptimizer(definicion)
        
        mejor_automata = optimizer.ejecutar()
        end_time = time.time()
        duration = round(end_time - start_time, 4)
        n_antes = len(definicion['estados'])
        n_despues = len(mejor_automata['estados'])
        reduccion = 0
        if n_antes > 0:
            reduccion = round(((n_antes - n_despues) / n_antes) * 100, 1)

        # Respuesta estructurada
        print(json.dumps({
            "success": True,
            "automata": mejor_automata,
            "reporte": {
                "algoritmo": algoritmo_elegido,
                "tiempo_seg": duration,
                "estados_iniciales": n_antes,
                "estados_finales": n_despues,
                "reduccion_porcentaje": reduccion,
                "mensaje": f"Se redujeron {n_antes - n_despues} estados en {duration}s."
            }
        }))

    except Exception as e:
        print(json.dumps({"success": False, "message": str(e)}))

if __name__ == "__main__":
    main()