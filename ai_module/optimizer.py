import sys
import json

def main():
    try:
        # 1. Leer el argumento que viene de Laravel (el JSON como string)
        if len(sys.argv) < 2:
            print(json.dumps({"error": "No se recibió el JSON de entrada"}))
            sys.exit(1)

        input_json_str = sys.argv[1]
        
        # 2. Parsear a Diccionario
        automata = json.loads(input_json_str)

        # 3. --- AQUÍ IRÁ TU MAGIA DE IA MÁS ADELANTE ---
        # Por ahora, solo simulamos que hicimos algo
        automata['nombre'] = automata.get('nombre', 'Sin Nombre') + " [OPTIMIZADO POR IA]"
        automata['descripcion_ia'] = "Este autómata pasó por Python correctamente."

        # 4. Devolver el resultado imprimíendolo en consola (Laravel capturará esto)
        print(json.dumps(automata))

    except Exception as e:
        # Si algo falla, devolvemos un JSON de error para que Laravel no explote
        error_response = {
            "error": str(e),
            "tipo": "Critical Error"
        }
        print(json.dumps(error_response))
        sys.exit(1)

if __name__ == "__main__":
    main()