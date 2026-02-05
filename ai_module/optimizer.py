import sys
import json
import random
import copy
import time
import math
import traceback

# --- 1. CLASE ORÁCULO UNIVERSAL (DFA / NFA / AP-PILA) ---
class AutomataOracle:
    def __init__(self, definicion):
        self.tipo = definicion.get('tipo', 'DFA').upper()
        self.estados = definicion.get('estados', [])
        self.transiciones = definicion.get('transiciones', {})
        self.estado_inicial = definicion.get('estado_inicial', '')
        self.estados_finales = set(definicion.get('estados_finales', []))
        self.alfabeto = definicion.get('alfabeto', ['0', '1']) 

    def simular(self, cadena):
        if self.tipo == 'AP' or self.tipo == 'PDA':
            return self.simular_pila(cadena)
        else:
            return self.simular_finito(cadena)

    def simular_finito(self, cadena):
        # LÓGICA PARA DFA Y NFA
        estados_actuales = {self.estado_inicial}
        
        for simbolo in cadena:
            proximos_estados = set()
            for estado in estados_actuales:
                if estado not in self.transiciones: continue
                
                transicion = self.transiciones[estado]
                destinos = None

                # Caso 1: Array posicional ["q1", "q2"]
                if isinstance(transicion, list):
                    try:
                        if simbolo in self.alfabeto:
                            idx = self.alfabeto.index(simbolo)
                            if idx < len(transicion):
                                destinos = transicion[idx]
                    except: pass
                
                # Caso 2: Diccionario {"0": "q1", "1": "q2"}
                elif isinstance(transicion, dict):
                    destinos = transicion.get(simbolo)

                if destinos:
                    # Corrección de seguridad: Si por error llega un dict aquí, lo ignoramos para no romper
                    if isinstance(destinos, list):
                        # Solo agregamos si los elementos son strings (estados), no dicts
                        limpios = [d for d in destinos if isinstance(d, str)]
                        proximos_estados.update(limpios)
                    elif isinstance(destinos, str):
                        proximos_estados.add(destinos)

            estados_actuales = proximos_estados
            if not estados_actuales: break 

        for estado in estados_actuales:
            if estado in self.estados_finales:
                return True
        return False

    def simular_pila(self, cadena):
        # LÓGICA PARA AP (Automata de Pila)
        # Configuración: (estado_actual, tupla_pila)
        configuraciones = {(self.estado_inicial, ())} 
        
        for simbolo in cadena:
            nuevas_configuraciones = set()
            try:
                idx = self.alfabeto.index(simbolo)
            except ValueError:
                # Si viene un símbolo que no está en el alfabeto, morimos
                return False

            for estado, pila in configuraciones:
                if estado not in self.transiciones: continue
                
                fila_alfabeto = self.transiciones[estado]
                if idx >= len(fila_alfabeto): continue
                
                movimientos = fila_alfabeto[idx] 

                # Validación extra: movimientos debe ser una lista de dicts
                if not isinstance(movimientos, list): continue

                for mov in movimientos:
                    if not isinstance(mov, dict): continue # Ignorar basura
                    
                    dest = mov.get('dest')
                    pop_char = mov.get('pop')
                    push_char = mov.get('push')
                    
                    # LOGICA DE PILA
                    pila_temp = list(pila)
                    valido = True

                    # 1. POP
                    if pop_char != 'λ':
                        if not pila_temp or pila_temp[-1] != pop_char:
                            valido = False
                        else:
                            pila_temp.pop()
                    
                    # 2. PUSH
                    if valido:
                        if push_char != 'λ':
                            pila_temp.append(push_char)
                        
                        # Limitamos la profundidad de pila para evitar bucles infinitos en tests
                        if len(pila_temp) < 50: 
                            nuevas_configuraciones.add((dest, tuple(pila_temp)))

            configuraciones = nuevas_configuraciones
            if not configuraciones: return False

        for estado, pila in configuraciones:
            if estado in self.estados_finales:
                # En muchos AP se pide pila vacía también, pero aquí asumimos aceptación por estado final
                return True
        return False

    def generar_test_set(self, cantidad=100):
        dataset = []
        intentos = 0
        count_true = 0
        count_false = 0
        limit_per_class = cantidad * 0.6 

        while len(dataset) < cantidad and intentos < cantidad * 15:
            largo = random.randint(0, 10) # Cadenas más cortas para Pila (es costoso)
            cadena = "".join(random.choice(self.alfabeto) for _ in range(largo))
            
            label = self.simular(cadena)
            
            agregar = False
            if label and count_true < limit_per_class:
                agregar = True
                count_true += 1
            elif not label and count_false < limit_per_class:
                agregar = True
                count_false += 1
            elif intentos > cantidad * 8:
                agregar = True

            if agregar:
                if not any(d['input'] == cadena for d in dataset):
                    dataset.append({'input': cadena, 'label': label})
            
            intentos += 1
            
        return dataset

# --- CLASE BASE DE OPTIMIZACIÓN ---
class BaseOptimizer:
    def __init__(self, original_json, test_set):
        self.original = original_json
        self.test_set = test_set
        self.alfabeto = original_json.get('alfabeto', ['0', '1'])
        self.tipo = original_json.get('tipo', 'DFA').upper()

    def evaluar_fitness(self, automata):
        oracle = AutomataOracle(automata)
        aciertos = 0
        for caso in self.test_set:
            if oracle.simular(caso['input']) == caso['label']:
                aciertos += 1
        
        precision = aciertos / len(self.test_set)
        
        try:
            n_estados = len(automata['estados'])
        except: n_estados = 1
        
        if n_estados == 0: return 0
        
        fitness = (precision * 2000) + (100 / n_estados)
        return fitness

    def generar_vecino(self, individuo):
        mutante = copy.deepcopy(individuo)
        estados = mutante['estados']
        if len(estados) < 2: return mutante 

        qA = random.choice(estados)
        qB = random.choice(estados)
        while qA == qB:
            qB = random.choice(estados)

        # FUSIÓN
        transiciones = mutante['transiciones']
        es_pila = (self.tipo == 'AP' or self.tipo == 'PDA')

        for estado_origen, trans_data in transiciones.items():
            
            # CASO PILA
            if es_pila:
                if isinstance(trans_data, list):
                    for lista_movimientos in trans_data:
                        if isinstance(lista_movimientos, list):
                            for mov in lista_movimientos:
                                if isinstance(mov, dict) and mov.get('dest') == qB:
                                    mov['dest'] = qA
            
            # CASO DFA/NFA
            elif isinstance(trans_data, list): 
                for i in range(len(trans_data)):
                    val = trans_data[i]
                    if isinstance(val, list): # NFA
                        trans_data[i] = [qA if x == qB else x for x in val]
                    elif val == qB: 
                        trans_data[i] = qA
            
            elif isinstance(trans_data, dict):
                for key in trans_data:
                    target = trans_data[key]
                    if isinstance(target, list):
                        trans_data[key] = [qA if x == qB else x for x in target]
                    elif target == qB:
                        trans_data[key] = qA
        
        if mutante['estado_inicial'] == qB:
            mutante['estado_inicial'] = qA

        if qB in mutante['estados_finales']:
            if qA not in mutante['estados_finales']:
                mutante['estados_finales'].append(qA)

        mutante['estados'].remove(qB)
        if qB in mutante['estados_finales']:
            mutante['estados_finales'].remove(qB)
        if qB in transiciones:
            del transiciones[qB]
            
        return mutante

# --- ALGORITMOS ---
class GeneticOptimizer(BaseOptimizer):
    def ejecutar(self, generaciones=50, poblacion_size=20):
        poblacion = [copy.deepcopy(self.original) for _ in range(poblacion_size)]
        mejor_fitness = -1
        mejor_individuo = self.original

        for gen in range(generaciones):
            nueva_poblacion = []
            if mejor_fitness > 0: nueva_poblacion.append(mejor_individuo)

            while len(nueva_poblacion) < poblacion_size:
                padre = random.choice(poblacion)
                hijo = self.generar_vecino(padre)
                nueva_poblacion.append(hijo)
            
            poblacion = nueva_poblacion
            for ind in poblacion:
                fit = self.evaluar_fitness(ind)
                if fit > mejor_fitness:
                    mejor_fitness = fit
                    mejor_individuo = copy.deepcopy(ind)
        return mejor_individuo, mejor_fitness

class SimulatedAnnealingOptimizer(BaseOptimizer):
    def ejecutar(self, temperatura_inicial=1000, alpha=0.95):
        actual = copy.deepcopy(self.original)
        fitness_actual = self.evaluar_fitness(actual)
        mejor_global = actual
        fitness_mejor = fitness_actual
        T = temperatura_inicial
        
        while T > 1:
            vecino = self.generar_vecino(actual)
            fitness_vecino = self.evaluar_fitness(vecino)
            delta = fitness_vecino - fitness_actual
            
            if delta > 0:
                actual = vecino
                fitness_actual = fitness_vecino
                if fitness_vecino > fitness_mejor:
                    mejor_global = vecino
                    fitness_mejor = fitness_vecino
            else:
                probabilidad = math.exp(delta / T)
                if random.random() < probabilidad:
                    actual = vecino
                    fitness_actual = fitness_vecino
            T = T * alpha
        return mejor_global, fitness_mejor

# --- MAIN ---
def main():
    try:
        if len(sys.argv) < 2: return
        data = json.loads(sys.argv[1])
        
        # 1. RECUPERACIÓN INTELIGENTE DE DATOS
        automata_wrapper = data.get('automata', {})
        definicion = automata_wrapper.get('json_definicion', {})
        
        # Si no vino dentro de 'automata', quizás vino plano
        if not definicion: 
            definicion = data.get('json_definicion', data)
            tipo_externo = data.get('tipo', 'DFA')
        else:
            tipo_externo = automata_wrapper.get('tipo', 'DFA')

        # >>> CORRECCIÓN CRUCIAL <<<
        # Inyectamos el 'tipo' dentro de la definición para que el Oráculo lo vea
        if 'tipo' not in definicion:
            definicion['tipo'] = tipo_externo
            
        algoritmo = data.get('algoritmo', 'genetico')

        # 2. Oráculo
        oracle = AutomataOracle(definicion)
        test_set = oracle.generar_test_set(cantidad=100)

        # 3. Selección de Algoritmo
        if algoritmo == 'hill_climbing' or algoritmo == 'simulated_annealing':
            optimizer = SimulatedAnnealingOptimizer(definicion, test_set)
        else:
            optimizer = GeneticOptimizer(definicion, test_set)
        
        # 4. Ejecución
        start_time = time.time()
        mejor_automata, mejor_score = optimizer.ejecutar()
        end_time = time.time()

        # 5. Respuesta
        respuesta = {
            "mensaje": "Optimización finalizada",
            "algoritmo_usado": algoritmo,
            "tiempo_ejecucion": round(end_time - start_time, 4),
            "score_final": round(mejor_score, 2),
            "estados_originales": len(definicion['estados']),
            "estados_finales": len(mejor_automata['estados']),
            "test_set_muestras": len(test_set),
            "automata_optimizado": mejor_automata 
        }
        print(json.dumps(respuesta))

    except Exception as e:
        # En caso de error, devolvemos el traceback para depurar fácil en Postman
        print(json.dumps({"error": str(e), "trace": traceback.format_exc()}))

if __name__ == "__main__":
    main()