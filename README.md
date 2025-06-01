# Usina solar

podman build -t usina_solar:v1 .

podman run -it --rm --name usina -p 5000:5000 -v ${PWD}/csv:/app/csv:Z usina_solar:v1 
