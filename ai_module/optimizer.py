import sys
import json
import random
import copy
import math
import statistics
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
        if self.tipo in ['AP', 'PDA']:
            return self.simular_pila(cadena)
        return self.simular_finito(cadena)

    def simular_finito(self, cadena):
        estados_actuales = {self.estado_inicial}
        trans = self.transiciones
        alfabeto = self.alfabeto
        for simbolo in cadena:
            proximos = set()
            for est in estados_actuales:
                rules = trans.get(est)
                if not rules:
                    continue
                if isinstance(rules, dict):
                    dests = rules.get(simbolo)
                elif isinstance(rules, list):
                    try:
                        idx = alfabeto.index(simbolo)
                        dests = rules[idx] if idx < len(rules) else None
                    except ValueError:
                        dests = None
                else:
                    dests = None

                if not dests:
                    continue
                if isinstance(dests, str):
                    proximos.add(dests)
                elif isinstance(dests, list):
                    for d in dests:
                        if isinstance(d, str) and d:
                            proximos.add(d)
            estados_actuales = proximos
            if not estados_actuales:
                break
        finales = self.estados_finales
        for est in estados_actuales:
            if est in finales:
                return True
        return False

    def simular_pila(self, cadena):
        configuraciones = {(self.estado_inicial, ())}
        for simbolo in cadena:
            nuevas = set()
            for est, pila in configuraciones:
                if est not in self.transiciones:
                    continue
                rules = self.transiciones[est]
                moves = []
                if isinstance(rules, dict):
                    moves = rules.get(simbolo, [])
                elif isinstance(rules, list):
                    try:
                        idx = self.alfabeto.index(simbolo)
                        if idx < len(rules):
                            moves = rules[idx]
                    except ValueError:
                        return False
                if not isinstance(moves, list):
                    continue
                for mov in moves:
                    if not isinstance(mov, dict):
                        continue
                    pila_new = list(pila)
                    pop_val = mov.get('pop', 'λ')
                    if pop_val and pop_val != 'λ':
                        if not pila_new or pila_new[-1] != pop_val:
                            continue
                        pila_new.pop()
                    push_val = mov.get('push', 'λ')
                    if push_val and push_val != 'λ':
                        pila_new.append(push_val)
                    if len(pila_new) < 20:
                        nuevas.add((mov['dest'], tuple(pila_new)))
            configuraciones = nuevas
            if not configuraciones:
                return False
        for est, pila in configuraciones:
            if est in self.estados_finales and len(pila) == 0:
                return True
        return False

    def generar_dataset(self, cantidad=300):
        data = []
        vistos = set()

        def agregar(s):
            if s not in vistos:
                vistos.add(s)
                data.append({'input': s, 'label': self.simular(s)})

        agregar("")
        for c in self.alfabeto:
            agregar(c)
        # Cadenas cortas de longitud 2 para buena cobertura inicial
        if len(self.alfabeto) <= 6:
            for c1 in self.alfabeto:
                for c2 in self.alfabeto:
                    agregar(c1 + c2)
                    if len(data) >= cantidad:
                        return data

        intentos = 0
        max_intentos = cantidad * 6
        while len(data) < cantidad and intentos < max_intentos:
            l = random.randint(1, 10)
            s = "".join(random.choice(self.alfabeto) for _ in range(l))
            agregar(s)
            intentos += 1
        return data


class BaseOptimizer:
    PENALIZACION = 999999

    def __init__(self, original, dataset=None):
        # 1. Normalizamos el autómata antes de hacer cualquier cosa
        self.original = self.normalizar_transiciones(original)

        # 2. Iniciamos el Oráculo con la versión ya normalizada
        self.oracle = AutomataOracle(self.original)
        self.dataset = dataset if dataset is not None else self.oracle.generar_dataset(300)

        # Métricas de ejecución
        self.evaluaciones_oraculo = 0
        self.historial_fitness = []
        self.mejor_iteracion = 0
        self.total_iteraciones = 0

    def fitness(self, candidato):
        """
        Función Monoobjetivo: f(A) = Cantidad de estados.
        Restricción rígida: El lenguaje debe ser idéntico sobre el dataset del oráculo.
        """
        if not self.validar(candidato):
            return self.PENALIZACION
        return len(candidato['estados'])

    def validar(self, candidato):
        self.evaluaciones_oraculo += 1
        cand_oracle = AutomataOracle(candidato)
        if cand_oracle.tipo not in ['AP', 'PDA']:
            trans = cand_oracle.transiciones
            estado_inicial = cand_oracle.estado_inicial
            finales = cand_oracle.estados_finales
            for caso in self.dataset:
                estados_actuales = {estado_inicial}
                for simbolo in caso['input']:
                    proximos = set()
                    for est in estados_actuales:
                        rules = trans.get(est)
                        if not rules:
                            continue
                        dests = rules.get(simbolo)
                        if not dests:
                            continue
                        if isinstance(dests, str):
                            proximos.add(dests)
                        else:
                            for d in dests:
                                if d:
                                    proximos.add(d)
                    estados_actuales = proximos
                    if not estados_actuales:
                        break
                aceptada = any(est in finales for est in estados_actuales)
                if aceptada != caso['label']:
                    return False
            return True

        for caso in self.dataset:
            if cand_oracle.simular(caso['input']) != caso['label']:
                return False
        return True

    def mutar_fusion(self, automata):
        """Movimiento de mejora: fusiona dos estados aleatorios reduciendo |Q| en 1."""
        if len(automata['estados']) < 2:
            return copy.deepcopy(automata)
        q1, q2 = random.sample(automata['estados'], 2)
        return self.fusionar_estados(automata, q1, q2)

    def mutar_split(self, automata):
        """Movimiento de exploración: duplica un estado aumentando |Q| en 1 (para SA)."""
        nuevo = copy.deepcopy(automata)
        if not nuevo['estados']:
            return nuevo
        q_target = random.choice(nuevo['estados'])
        idx = len(nuevo['estados'])
        nuevo_nombre = f"s{idx}n"
        while nuevo_nombre in nuevo['estados']:
            idx += 1
            nuevo_nombre = f"s{idx}n"
        nuevo['estados'].append(nuevo_nombre)
        if q_target in nuevo['estados_finales']:
            nuevo['estados_finales'].append(nuevo_nombre)
        if q_target in nuevo['transiciones']:
            nuevo['transiciones'][nuevo_nombre] = copy.deepcopy(nuevo['transiciones'][q_target])
        return nuevo

    def fusionar_estados(self, automata, q1, q2):
        """Fusiona el estado q2 dentro de q1 manteniendo coherencia de transiciones."""
        nuevo = copy.deepcopy(automata)
        trans = nuevo['transiciones']
        es_dfa = nuevo.get('tipo', 'DFA').upper() == 'DFA'

        def replace_state(obj):
            if isinstance(obj, list):
                return [replace_state(x) for x in obj]
            if isinstance(obj, dict):
                return {k: replace_state(v) for k, v in obj.items()}
            return q1 if obj == q2 else obj

        for k in list(trans.keys()):
            trans[k] = replace_state(trans[k])

        if q2 in trans:
            if q1 not in trans:
                trans[q1] = trans[q2]
            elif isinstance(trans[q1], dict) and isinstance(trans[q2], dict):
                for simbolo, dests_q2 in trans[q2].items():
                    dests_q1 = trans[q1].get(simbolo, [])
                    if not dests_q1:
                        trans[q1][simbolo] = dests_q2
                    elif not es_dfa:
                        combinados = list(dests_q1)
                        for d in dests_q2:
                            if d not in combinados:
                                combinados.append(d)
                        trans[q1][simbolo] = combinados
            del trans[q2]

        if nuevo['estado_inicial'] == q2:
            nuevo['estado_inicial'] = q1
        if q2 in nuevo['estados_finales']:
            if q1 not in nuevo['estados_finales']:
                nuevo['estados_finales'].append(q1)
            nuevo['estados_finales'].remove(q2)

        if q2 in nuevo['estados']:
            nuevo['estados'].remove(q2)

        return nuevo

    def _misma_finalidad(self, automata, q1, q2):
        finales = set(automata.get('estados_finales', []))
        return (q1 in finales) == (q2 in finales)

    def mutar_cruce(self, padre1, padre2, f_p1=None, f_p2=None):
        """
        Operador de Crossover basado en estructura y fusiones válidas:
        - Si padre2 es válido y más compacto que padre1, hereda la estructura compacta
          e intenta aplicar fusiones adicionales presentes en padre1.
        - En caso contrario, toma padre1 e intenta incorporar fusiones de estados
          eliminados en padre2 (o fusionar pares compatibles de misma finalidad).
        """
        p1_valido = (f_p1 < self.PENALIZACION) if f_p1 is not None else self.validar(padre1)
        p2_valido = (f_p2 < self.PENALIZACION) if f_p2 is not None else self.validar(padre2)

        if p2_valido and (not p1_valido or len(padre2['estados']) < len(padre1['estados'])):
            base = copy.deepcopy(padre2)
            donante = padre1
        elif p1_valido:
            base = copy.deepcopy(padre1)
            donante = padre2
        else:
            # Si ninguno es válido, reiniciar desde una copia del original con una fusión
            return self.mutar_fusion(self.original)

        estados_base = set(base['estados'])
        estados_donante = set(donante['estados'])

        # Estados presentes en 'base' que el 'donante' logró eliminar mediante fusión
        eliminados_en_donante = [q for q in base['estados'] if q not in estados_donante]
        random.shuffle(eliminados_en_donante)

        hijo = base
        for q_elim in eliminados_en_donante[:2]:
            if q_elim not in hijo['estados'] or len(hijo['estados']) < 2:
                continue
            # Candidatos compatibles en 'hijo' (misma condición de aceptación: Myhill-Nerode)
            candidatos_dest = [
                q for q in hijo['estados']
                if q != q_elim and self._misma_finalidad(hijo, q, q_elim)
            ]
            if not candidatos_dest:
                continue
            random.shuffle(candidatos_dest)
            # Probar hasta 3 destinos compatibles para heredar una fusión válida
            for q_dest in candidatos_dest[:3]:
                intento = self.fusionar_estados(hijo, q_dest, q_elim)
                if self.validar(intento):
                    hijo = intento
                    break

        # Si el donante no aportó estados eliminados distintos, intentar combinar
        # mediante una fusión guiada de estados con misma finalidad en el hijo
        if len(hijo['estados']) == len(base['estados']) and len(hijo['estados']) >= 2:
            finales = [q for q in hijo['estados'] if q in hijo['estados_finales']]
            no_finales = [q for q in hijo['estados'] if q not in hijo['estados_finales']]
            grupos = [g for g in (finales, no_finales) if len(g) >= 2]
            if grupos:
                grupo = random.choice(grupos)
                q1, q2 = random.sample(grupo, 2)
                intento = self.fusionar_estados(hijo, q1, q2)
                if self.validar(intento):
                    hijo = intento

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

            if isinstance(reglas, dict):
                for simbolo, destinos in reglas.items():
                    if not isinstance(destinos, list):
                        destinos = [destinos] if destinos else []
                    destinos_validos = [d for d in destinos if d]
                    if destinos_validos:
                        trans_normalizadas[estado][simbolo] = destinos_validos

            elif isinstance(reglas, list):
                for idx, destinos in enumerate(reglas):
                    if idx < len(alfabeto):
                        simbolo = alfabeto[idx]
                        if not isinstance(destinos, list):
                            destinos = [destinos] if destinos else []
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
                        if all(isinstance(x, str) for x in destinos):
                            transiciones[estado][simbolo] = sorted(list(set(destinos)))

        return limpio


# --- TRAYECTORIA ÚNICA: SIMULATED ANNEALING ---
class AnnealingOptimizer(BaseOptimizer):
    def ejecutar(self):
        actual = copy.deepcopy(self.original)
        mejor = copy.deepcopy(self.original)

        # Cachear fitness para evitar recálculos redundantes en cada iteración
        f_actual = self.fitness(actual)
        f_mejor = f_actual

        t = 2.0
        alfa = 0.92
        t_min = 0.05

        historial = []
        iteracion = 0
        mejor_iter = 0

        while t > t_min:
            iteracion += 1

            # En SA, el vecino puede reducir (fusión) o expandir (split exploratorio)
            if random.random() > 0.25:
                vecino = self.mutar_fusion(actual)
            else:
                vecino = self.mutar_split(actual)

            f_vecino = self.fitness(vecino)
            delta = f_vecino - f_actual

            # Aceptar si mejora (delta < 0) o por criterio de Boltzmann sobre soluciones válidas
            if delta < 0 or (f_vecino < self.PENALIZACION and random.random() < math.exp(-delta / t)):
                actual = vecino
                f_actual = f_vecino
                if f_actual < f_mejor:
                    mejor = copy.deepcopy(actual)
                    f_mejor = f_actual
                    mejor_iter = iteracion

            historial.append(f_mejor)
            t *= alfa

        self.historial_fitness = historial
        self.mejor_iteracion = mejor_iter
        self.total_iteraciones = iteracion

        mejor = self.limpiar_duplicados(mejor)
        return mejor


# --- POBLACIONAL: ALGORITMO GENÉTICO ---
class GeneticOptimizer(BaseOptimizer):
    TAM_POBLACION = 16
    GENERACIONES = 25

    def _inicializar_poblacion(self):
        """Genera una población diversa de 16 individuos: original + variantes fusionadas."""
        poblacion = [copy.deepcopy(self.original)]
        estados = self.original.get('estados', [])

        # Armar pares distintos de estados para diversificar las fusiones iniciales
        pares = []
        for i in range(len(estados)):
            for j in range(i + 1, len(estados)):
                pares.append((estados[i], estados[j]))
        random.shuffle(pares)

        par_idx = 0
        while len(poblacion) < self.TAM_POBLACION:
            if len(estados) < 2:
                poblacion.append(copy.deepcopy(self.original))
                continue

            if par_idx < len(pares) and len(poblacion) < 11:
                # Variantes con una fusión única distinta
                q1, q2 = pares[par_idx]
                par_idx += 1
                individuo = self.fusionar_estados(self.original, q1, q2)
            else:
                # Variantes con 1 o 2 fusiones encadenadas aleatorias
                individuo = copy.deepcopy(self.original)
                pasos = random.randint(1, min(2, len(estados) - 1))
                for _ in range(pasos):
                    individuo = self.mutar_fusion(individuo)

            poblacion.append(individuo)

        return poblacion

    def ejecutar(self):
        poblacion = self._inicializar_poblacion()
        mejor_global = copy.deepcopy(self.original)
        f_mejor_global = self.fitness(mejor_global)

        historial = []
        mejor_gen = 0

        for gen in range(1, self.GENERACIONES + 1):
            # 1. Evaluación única por individuo y ordenamiento por fitness
            evaluados = [(self.fitness(ind), ind) for ind in poblacion]
            evaluados.sort(key=lambda x: x[0])

            if evaluados[0][0] < f_mejor_global:
                f_mejor_global = evaluados[0][0]
                mejor_global = copy.deepcopy(evaluados[0][1])
                mejor_gen = gen

            historial.append(f_mejor_global)

            # 2. Selección con elitismo (top 2)
            nueva_gen = [copy.deepcopy(evaluados[0][1]), copy.deepcopy(evaluados[1][1])]

            # Pool de selección (torneo / mejores 6)
            pool = evaluados[:min(6, len(evaluados))]

            # 3. Cruzamiento y Mutación
            while len(nueva_gen) < self.TAM_POBLACION:
                f_a, padre_a = random.choice(pool)

                # 70% de probabilidad de Cruzamiento estructural
                if random.random() < 0.7:
                    f_b, padre_b = random.choice(pool)
                    hijo = self.mutar_cruce(padre_a, padre_b, f_p1=f_a, f_p2=f_b)
                else:
                    hijo = copy.deepcopy(padre_a)

                # 35% de probabilidad de Mutación (Fusión) sobre el hijo
                if random.random() < 0.35:
                    hijo = self.mutar_fusion(hijo)

                nueva_gen.append(hijo)

            poblacion = nueva_gen

        self.historial_fitness = historial
        self.mejor_iteracion = mejor_gen
        self.total_iteraciones = self.GENERACIONES

        mejor_global = self.limpiar_duplicados(mejor_global)
        return mejor_global


# --- ANÁLISIS ESTADÍSTICO NO PARAMÉTRICO (PYTHON PURO) ---
def _percentil(valores_ordenados, p):
    """Calcula el percentil p (0..1) por interpolación lineal sobre lista ordenada."""
    n = len(valores_ordenados)
    if n == 0:
        return 0.0
    if n == 1:
        return float(valores_ordenados[0])
    pos = p * (n - 1)
    idx_inf = math.floor(pos)
    idx_sup = math.ceil(pos)
    if idx_inf == idx_sup:
        return float(valores_ordenados[idx_inf])
    frac = pos - idx_inf
    return float(valores_ordenados[idx_inf]) + frac * (
        float(valores_ordenados[idx_sup]) - float(valores_ordenados[idx_inf])
    )


def calcular_estadisticas(muestra):
    """
    Calcula estadísticos descriptivos y parámetros de Boxplot (regla de Tukey 1.5*RIC).
    """
    if not muestra:
        return {
            "valores_ordenados": [],
            "n": 0,
            "media": 0.0,
            "desviacion_std": 0.0,
            "min": 0.0,
            "q1": 0.0,
            "mediana": 0.0,
            "q3": 0.0,
            "max": 0.0,
            "ric": 0.0,
            "bigote_inf": 0.0,
            "bigote_sup": 0.0,
            "outliers": [],
        }

    valores_ordenados = sorted(muestra)
    n = len(valores_ordenados)
    media = statistics.mean(valores_ordenados)
    desviacion_std = statistics.stdev(valores_ordenados) if n > 1 else 0.0

    q1 = _percentil(valores_ordenados, 0.25)
    mediana = _percentil(valores_ordenados, 0.50)
    q3 = _percentil(valores_ordenados, 0.75)
    ric = q3 - q1

    limite_inf = q1 - 1.5 * ric
    limite_sup = q3 + 1.5 * ric

    no_outliers = [v for v in valores_ordenados if limite_inf <= v <= limite_sup]
    outliers = [round(v, 4) if isinstance(v, float) else v for v in valores_ordenados if v < limite_inf or v > limite_sup]

    bigote_inf = min(no_outliers) if no_outliers else valores_ordenados[0]
    bigote_sup = max(no_outliers) if no_outliers else valores_ordenados[-1]

    return {
        "valores_ordenados": [round(v, 4) if isinstance(v, float) else v for v in valores_ordenados],
        "n": n,
        "media": round(media, 4),
        "desviacion_std": round(desviacion_std, 4),
        "min": round(valores_ordenados[0], 4) if isinstance(valores_ordenados[0], float) else valores_ordenados[0],
        "q1": round(q1, 4),
        "mediana": round(mediana, 4),
        "q3": round(q3, 4),
        "max": round(valores_ordenados[-1], 4) if isinstance(valores_ordenados[-1], float) else valores_ordenados[-1],
        "ric": round(ric, 4),
        "bigote_inf": round(bigote_inf, 4) if isinstance(bigote_inf, float) else bigote_inf,
        "bigote_sup": round(bigote_sup, 4) if isinstance(bigote_sup, float) else bigote_sup,
        "outliers": outliers,
    }


def test_wilcoxon_ranksum(muestra_a, muestra_b):
    """
    Test de Wilcoxon Rank-Sum (equivalente a Mann-Whitney U bilateral) en Python puro,
    con corrección por empates y aproximación normal mediante math.erfc.
    """
    n1 = len(muestra_a)
    n2 = len(muestra_b)
    n_total = n1 + n2

    if n1 == 0 or n2 == 0:
        return {
            "estadistico_u": 0.0,
            "z_score": 0.0,
            "p_value": 1.0,
            "significativo": False,
        }

    combinada = [(v, 0) for v in muestra_a] + [(v, 1) for v in muestra_b]
    combinada.sort(key=lambda item: item[0])

    # Asignación de rangos promedio para empates y cálculo de corrección T = sum(t^3 - t)
    r1 = 0.0
    tie_sum = 0.0
    i = 0
    while i < n_total:
        j = i
        while j + 1 < n_total and combinada[j + 1][0] == combinada[i][0]:
            j += 1
        t = j - i + 1
        rango_promedio = (i + 1 + j + 1) / 2.0
        if t > 1:
            tie_sum += (t ** 3 - t)
        for k in range(i, j + 1):
            if combinada[k][1] == 0:
                r1 += rango_promedio
        i = j + 1

    u1 = r1 - (n1 * (n1 + 1)) / 2.0
    u2 = (n1 * n2) - u1
    estadistico_u = min(u1, u2)

    mu_u = (n1 * n2) / 2.0
    denom_tie = n_total * (n_total - 1)
    correccion_empates = (tie_sum / denom_tie) if denom_tie > 0 else 0.0
    var_u = (n1 * n2 / 12.0) * ((n_total + 1) - correccion_empates)

    if var_u <= 1e-12:
        return {
            "estadistico_u": round(estadistico_u, 4),
            "z_score": 0.0,
            "p_value": 1.0,
            "significativo": False,
        }

    sigma_u = math.sqrt(var_u)
    diff = u1 - mu_u
    # Corrección por continuidad hacia cero
    if abs(diff) > 0.5:
        z_score = math.copysign((abs(diff) - 0.5) / sigma_u, diff)
    else:
        z_score = 0.0

    p_value = math.erfc(abs(z_score) / math.sqrt(2.0))
    p_value = min(1.0, max(0.0, p_value))

    return {
        "estadistico_u": round(estadistico_u, 4),
        "z_score": round(z_score, 4),
        "p_value": round(p_value, 6),
        "significativo": bool(p_value < 0.05),
    }


def _promediar_curvas(curvas):
    if not curvas:
        return []
    longitud = min(len(c) for c in curvas)
    return [
        round(sum(c[i] for c in curvas) / len(curvas), 4)
        for i in range(longitud)
    ]


def ejecutar_benchmark(definicion, corridas):
    n_antes = len(definicion.get('estados', []))

    # Pre-normalizamos una copia para armar un dataset de validación consistente por corrida
    base_tmp = BaseOptimizer(definicion)
    dataset_base = base_tmp.dataset

    def correr_algoritmo(clase_opt):
        estados_list = []
        tiempos_list = []
        reducciones_list = []
        evaluaciones_list = []
        mejor_iter_list = []
        curvas = []
        detalle = []

        for idx in range(1, corridas + 1):
            t0 = time.perf_counter()
            opt = clase_opt(definicion, dataset=dataset_base)
            mejor = opt.ejecutar()
            tiempo_ms = round((time.perf_counter() - t0) * 1000.0, 3)

            n_despues = len(mejor.get('estados', []))
            reduccion = round(((n_antes - n_despues) / n_antes) * 100.0, 2) if n_antes > 0 else 0.0

            estados_list.append(n_despues)
            tiempos_list.append(tiempo_ms)
            reducciones_list.append(reduccion)
            evaluaciones_list.append(opt.evaluaciones_oraculo)
            mejor_iter_list.append(opt.mejor_iteracion)
            curvas.append(opt.historial_fitness)
            detalle.append({
                "corrida": idx,
                "estados_finales": n_despues,
                "tiempo_ms": tiempo_ms,
                "reduccion_porcentaje": reduccion,
                "evaluaciones_oraculo": opt.evaluaciones_oraculo,
                "mejor_iteracion": opt.mejor_iteracion,
            })

        return {
            "estados": calcular_estadisticas(estados_list),
            "tiempo_ms": calcular_estadisticas(tiempos_list),
            "reduccion_porcentaje": calcular_estadisticas(reducciones_list),
            "evaluaciones_promedio": round(statistics.mean(evaluaciones_list), 2),
            "mejor_iteracion_promedio": round(statistics.mean(mejor_iter_list), 2),
            "corridas_detalle": detalle,
        }, estados_list, tiempos_list, curvas

    res_sa, estados_sa, tiempos_sa, curvas_sa = correr_algoritmo(AnnealingOptimizer)
    res_ga, estados_ga, tiempos_ga, curvas_ga = correr_algoritmo(GeneticOptimizer)

    return {
        "corridas": corridas,
        "estados_iniciales": n_antes,
        "sa": res_sa,
        "genetico": res_ga,
        "wilcoxon_estados": test_wilcoxon_ranksum(estados_sa, estados_ga),
        "wilcoxon_tiempo": test_wilcoxon_ranksum(tiempos_sa, tiempos_ga),
        "convergencia_promedio": {
            "sa": _promediar_curvas(curvas_sa),
            "genetico": _promediar_curvas(curvas_ga),
        },
    }


# --- MAIN ---
def main():
    try:
        start_time = time.perf_counter()
        input_data = sys.stdin.read().strip()
        if not input_data and len(sys.argv) > 1:
            input_data = sys.argv[1]
        if not input_data:
            return

        data = json.loads(input_data)
        definicion = data.get('json_definicion', data.get('automata', data))
        if 'tipo' not in definicion:
            definicion['tipo'] = data.get('tipo', 'DFA')

        # --- MODO BENCHMARK COMPARATIVO ---
        if data.get('modo') == 'benchmark':
            corridas = int(data.get('corridas', 25))
            corridas = max(5, min(50, corridas))
            benchmark = ejecutar_benchmark(definicion, corridas)
            print(json.dumps({
                "success": True,
                "benchmark": benchmark,
            }))
            return

        # --- MODO OPTIMIZACIÓN INDIVIDUAL ---
        algoritmo_elegido = data.get('algoritmo', 'genetico')

        if algoritmo_elegido == 'sa':
            optimizer = AnnealingOptimizer(definicion)
        else:
            optimizer = GeneticOptimizer(definicion)

        mejor_automata = optimizer.ejecutar()
        duration = round(time.perf_counter() - start_time, 4)
        n_antes = len(definicion.get('estados', []))
        n_despues = len(mejor_automata.get('estados', []))
        reduccion = round(((n_antes - n_despues) / n_antes) * 100, 1) if n_antes > 0 else 0

        print(json.dumps({
            "success": True,
            "automata": mejor_automata,
            "reporte": {
                "algoritmo": algoritmo_elegido,
                "tiempo_seg": duration,
                "tiempo_ms": round(duration * 1000, 2),
                "estados_iniciales": n_antes,
                "estados_finales": n_despues,
                "reduccion_porcentaje": reduccion,
                "evaluaciones_oraculo": optimizer.evaluaciones_oraculo,
                "mejor_iteracion": optimizer.mejor_iteracion,
                "total_iteraciones": optimizer.total_iteraciones,
                "historial_fitness": optimizer.historial_fitness,
                "mensaje": f"Se redujeron {n_antes - n_despues} estados en {duration}s.",
            },
        }))

    except Exception as e:
        print(json.dumps({"success": False, "message": str(e)}))


if __name__ == "__main__":
    main()
