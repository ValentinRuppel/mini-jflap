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

# --- CLASE BASE ---
class BaseOptimizer:
    def __init__(self, original):
        self.original = original
        self.oracle = AutomataOracle(original)
        self.dataset = self.oracle.generar_dataset(200) # 200 casos de prueba

    def validar(self, candidato):
        # Verifica si el candidato se comporta IGUAL al original
        oraculo_cand = AutomataOracle(candidato)
        for caso in self.dataset:
            if oraculo_cand.simular(caso['input']) != caso['label']:
                return False
        return True

    def fusionar_estados(self, automata, q1, q2):
        # Fusión y limpieza (DFA y NFA)
        nuevo = copy.deepcopy(automata)
        trans = nuevo['transiciones']
        def replace(obj):
            if isinstance(obj, list): return [replace(x) for x in obj]
            if isinstance(obj, dict): return {k: replace(v) for k,v in obj.items()}
            if obj == q2: return q1
            return obj

        for k in list(trans.keys()): trans[k] = replace(trans[k])
        # Limpieza de duplicados NFA
        for origen, reglas in trans.items():
            if isinstance(reglas, dict):
                for entrada, destinos in reglas.items():
                    if isinstance(destinos, list):
                        if len(destinos) > 1 and all(isinstance(x, str) for x in destinos):
                            reglas[entrada] = sorted(list(set(destinos)))
                        elif len(destinos) > 1 and all(isinstance(x, dict) for x in destinos):
                            try:
                                unique = set(json.dumps(x, sort_keys=True) for x in destinos)
                                reglas[entrada] = [json.loads(x) for x in unique]
                            except: pass
        if nuevo['estado_inicial'] == q2: nuevo['estado_inicial'] = q1
        if q2 in nuevo['estados_finales']:
            nuevo['estados_finales'] = list(set(nuevo['estados_finales'] + [q1]))
            if q2 in nuevo['estados_finales']: nuevo['estados_finales'].remove(q2)
        if q2 in nuevo['estados']: nuevo['estados'].remove(q2)
        if q2 in trans: del trans[q2]
        return nuevo

    def generar_vecino(self, individuo):
        estados = individuo['estados']
        if len(estados) < 2: return None
        qA, qB = random.sample(estados, 2)
        return self.fusionar_estados(individuo, qA, qB)

# --- OPCIÓN 1: ALGORITMO GENÉTICO ---
class GeneticOptimizer(BaseOptimizer):
    def ejecutar(self):
        poblacion = [self.original] # Iniciamos con clones
        mejor_global = self.original
        generaciones = 10  # Cantidad de ciclos
        poblacion_size = 8 # Individuos por ciclo

        for gen in range(generaciones):
            nueva_poblacion = []
            
            # Elitismo: El mejor siempre pasa
            nueva_poblacion.append(mejor_global)

            # Llenar el resto con mutaciones
            while len(nueva_poblacion) < poblacion_size:
                padre = random.choice(poblacion)
                hijo = self.generar_vecino(padre)
                
                # En Genético, si el hijo es inválido (rompe el lenguaje), muere.
                if hijo and self.validar(hijo):
                    nueva_poblacion.append(hijo)
                else:
                    nueva_poblacion.append(padre)
            poblacion = nueva_poblacion
            # Evaluar: buscamos el que tenga MENOS estados
            poblacion.sort(key=lambda x: len(x['estados']))
            mejor_actual = poblacion[0]
            
            if len(mejor_actual['estados']) < len(mejor_global['estados']):
                mejor_global = mejor_actual

        return mejor_global

# --- OPCIÓN 2: RECOCIDO SIMULADO (SIMULATED ANNEALING) ---
class AnnealingOptimizer(BaseOptimizer):
    def ejecutar(self):
        actual = self.original
        mejor = self.original
        T = 100.0   # Temperatura inicial
        alpha = 0.9 # Enfriamiento
        
        while T > 1:
            vecino = self.generar_vecino(actual)
            
            if not vecino: break # No se puede reducir más
            if not self.validar(vecino):
                T *= alpha
                continue

            # Costo = Cantidad de estados
            costo_actual = len(actual['estados'])
            costo_vecino = len(vecino['estados'])
            delta = costo_vecino - costo_actual

            # Si mejora (delta < 0), aceptamos siempre
            if delta < 0:
                actual = vecino
                if len(actual['estados']) < len(mejor['estados']):
                    mejor = actual
            else:
                # Si empeora o es igual, aceptamos con probabilidad (Boltzmann)
                prob = math.exp(-delta / T)
                if random.random() < prob:
                    actual = vecino
            
            T *= alpha
            
        return mejor

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
        if algoritmo_elegido == 'recocido':
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