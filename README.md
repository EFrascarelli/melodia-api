# Melodia API

API REST para gestionar playlists y canciones. Trabajo práctico individual para la materia Ingeniería de Software II.

## Cómo correr el proyecto

### Opción 1: Docker

```bash
docker-compose up --build



## Comandos útiles

### Docker básico
- `docker-compose up --build` → levantar todo y compilar
- `docker-compose down` → apagar los servicios

### Verificar que funcione
- `curl http://localhost:8000/ping`
- [http://localhost:8000/docs](http://localhost:8000/docs)

### Tests
- `docker-compose exec web pytest`

### Debug
- `docker-compose exec web bash`
- `docker-compose logs -f`
