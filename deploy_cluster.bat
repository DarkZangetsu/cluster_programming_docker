@echo off
echo --- Suppression de la stack existante ---
docker stack rm task_cluster
timeout /t 5

echo --- Construction de la nouvelle image Docker ---
docker build -t task_image .

echo --- Redéploiement de la stack avec les mises à jour ---
docker stack deploy -c stack.yml task_cluster
timeout /t 5

echo --- Affichage des logs du service ---
docker service logs task_cluster_mon_app

pause
