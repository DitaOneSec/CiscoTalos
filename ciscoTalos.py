import yaml
import requests
from requests.exceptions import RequestException, HTTPError, JSONDecodeError

def load_config():
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        # Validar la configuración
        required_keys = ['api']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"La clave '{key}' es requerida en el archivo de configuración.")
        return config
    except FileNotFoundError:
        print("El archivo de configuración 'config.yaml' no se encontró.")
        return None
    except yaml.YAMLError as e:
        print(f"Error al cargar la configuración: {e}")
        return None

def call_api(endpoint, method='GET', params=None, headers=None, data=None):
    try:
        response = requests.request(method, endpoint, params=params, headers=headers, data=data)
        response.raise_for_status()  # Lanza una excepción si la respuesta indica un error HTTP
        return response.json()
    except HTTPError as e:
        print(f"Error HTTP al llamar a la API: {e}")
        return None
    except JSONDecodeError:
        print("Error al decodificar la respuesta JSON.")
        return None
    except RequestException as e:
        print(f"Error al llamar a la API: {e}")
        return None

def extract_observables(observable_type):
    config = load_config()
    if config is None:
        return None
    
    if 'observables' not in config['api']:
        print("El archivo de configuración no contiene el endpoint para extraer observables.")
        return None
    
    endpoint = config['api']['observables']
    params = {"type": observable_type}
    extracted_observables = call_api(endpoint, method='GET', params=params)
    return extracted_observables

def deliberate_observables(observables):
    config = load_config()
    if config is None:
        return None
    
    if 'deliberate' not in config['api']:
        print("El archivo de configuración no contiene el endpoint para deliberar observables.")
        return None
    
    endpoint = config['api']['deliberate']
    data = {"observables": observables}
    deliberated_observables = call_api(endpoint, method='POST', data=data)
    return deliberated_observables

def contextualize_observable(observable):
    config = load_config()
    if config is None:
        return None
    
    if 'contextualize' not in config['api']:
        print("El archivo de configuración no contiene el endpoint para contextualizar observables.")
        return None
    
    endpoint = config['api']['contextualize']
    data = {"observable": observable}
    contextualized_observable = call_api(endpoint, method='POST', data=data)
    return contextualized_observable

if __name__ == "__main__":
    # Ejemplo de uso de las funciones
    observable_type = "IP"
    observables = [{"type": "IP", "value": "192.168.1.1"}]
    
    # Extraer observables
    extracted_observables = extract_observables(observable_type)
    if extracted_observables:
        print("Observables extraídos:", extracted_observables)
    
    # Deliberar observables
    deliberated_observables = deliberate_observables(observables)
    if deliberated_observables:
        print("Observables deliberados:", deliberated_observables)
    
    # Contextualizar observable
    observable_to_contextualize = {"type": "IP", "value": "192.168.1.1"}
    contextualized_observable = contextualize_observable(observable_to_contextualize)
    if contextualized_observable:
        print("Observable contextualizado:", contextualized_observable)
