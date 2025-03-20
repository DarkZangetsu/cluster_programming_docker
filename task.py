import os
import time
import redis

# Connexion à Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.StrictRedis(host=redis_host, port=6379, decode_responses=True)

def get_replica_id():
    return int(os.getenv("REPLICA_ID", "1"))  # Défaut à 1 si non défini

def compute_range(start, end):
    return sum(range(start, end + 1))

if __name__ == '__main__':
    replica_id = get_replica_id()

    # Définir les tranches de calcul en fonction du réplica
    ranges = {
        1: (1, 2500000000),
        2: (2500000001, 5000000000),
        3: (5000000001, 7500000000),
        4: (7500000001, 10000000000)
    }

    start_num, end_num = ranges.get(replica_id, (1, 2500))

    debut = time.time()
    resultat = compute_range(start_num, end_num)
    duree = time.time() - debut

    print(f"Replica {replica_id} : Calcul de la somme de {start_num} à {end_num} = {resultat} en {duree:.6f} secondes.")

    # Stocker le résultat dans Redis
    redis_client.set(f"result_{replica_id}", resultat)

    # Vérifier si tous les conteneurs ont terminé
    while True:
        time.sleep(1)  # Pause pour éviter une surcharge CPU
        all_results = [redis_client.get(f"result_{i}") for i in range(1, 5)]

        if None not in all_results:  # Vérifier si tous les résultats sont disponibles
            total = sum(map(int, all_results))
            print(f"✅ Somme totale calculée par tous les réplicas = {total}")
            break  # Arrêter la boucle une fois que le total est affiché
