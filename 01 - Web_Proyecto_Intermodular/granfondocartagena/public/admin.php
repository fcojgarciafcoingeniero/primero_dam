<?php
// Importación e inyección de código del archivo db.php (conexión PDO a la BBDD)
require_once '../config/db.php';

// Inicializa variable para mensajes de control
$mensaje_notificacion = "";

// Comprobar si el archivo 'eliminar.php' nos ha devuelto con un estado concreto
if (isset($_GET['status'])) {
    if ($_GET['status'] == 'deleted') {
        $mensaje_notificacion = "✅ El participante ha sido eliminado correctamente de la lista.";
    }
}

// Manejo de excepciones
try {
    // Consulta SQL lanzada a la BBDD
    $sql = "SELECT id, nombre, apellidos, dni, email FROM participantes ORDER BY id ASC";
    // Envio de la sentencia SQL a la BBDD mediante el objeto de conexión PDO
    $stmt = $pdo->query($sql);
    // Variable que guarda todas las filas devueltas por la consulta en forma de matriz
    $participantes = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    die("Error al consultar la lista de participantes: " . $e->getMessage());
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel de Administración - Gran Fondo Cartagena</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; color: #333; }
        .contenedor { max-width: 1000px; margin: 0 auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .panel-boton { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #eeece9; padding-bottom: 10px; margin-bottom: 20px;} 
        h2 { color: #0b2545; border-bottom: 2px solid #eeece9; padding-bottom: 10px; }
        .boton-regreso {background-color: #0b2545; color: white; text-decoration: none; padding: 8px 16px; border-radius: 4px; font-size: 14px; font-weight: bold; transition: background 0.2s, transform 0.2s;}
        .boton-regreso:hover {background-color: #134074; transform: scale(1.03);}
        .alerta-exito { background: #d4edda; color: #155724; padding: 12px; margin-bottom: 20px; border-radius: 4px; border: 1px solid #c3e6cb; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #0b2545; color: white; }
        tr:hover { background-color: #f8f9fa; }
        .boton-borrar { background: #dc3545; color: white; padding: 6px 12px; text-decoration: none; border-radius: 4px; font-size: 14px; font-weight: bold; }
        .boton-borrar:hover { background: #bd2130; }
        .sin-datos { text-align: center; padding: 20px; color: #777; font-style: italic; }
    </style>
</head>
<body>

<div class="contenedor">
    <!-- Encabezado del contenedor con botón de vuelta al index -->
    <div class="panel-boton">
        <h2>Panel de Control: Gestión de Inscritos</h2>
        <a href="index.php" class="boton-regreso">🏠 Volver al Inicio</a>
    </div>

    <?php if (!empty($mensaje_notificacion)): ?>
        <div class="alerta alerta-exito">
            <?php echo htmlspecialchars($mensaje_notificacion); ?>
        </div>
    <?php endif; ?>

    <!-- Tabla para pintar los inscritos -->
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Apellidos</th>
                <th>DNI / NIE</th>
                <th>Email</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            <?php if (count($participantes) > 0): ?>
                <!-- Bucle para pintar el contenido de cada fila de la Tabla - 1 por registrado -->
                <?php foreach ($participantes as $p): ?>
                    <tr>
                        <td><?php echo htmlspecialchars($p['id']); ?></td>
                        <td><?php echo htmlspecialchars($p['nombre']); ?></td>
                        <td><?php echo htmlspecialchars($p['apellidos']); ?></td>
                        <td><?php echo htmlspecialchars($p['dni']); ?></td>
                        <td><?php echo htmlspecialchars($p['email']); ?></td>
                        <td>
                            <a href="eliminar.php?id=<?php echo $p['id']; ?>" 
                               class="boton-borrar" 
                               onclick="return confirm('¿Seguro  que desea eliminar a <?php echo htmlspecialchars($p['nombre'] . ' ' . $p['apellidos']); ?> del sistema?');">
                                ❌ Eliminar
                            </a>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php else: ?>
                <tr>
                    <td colspan="6" class="sin-datos">No hay ningún participante inscrito en la base de datos actualmente.</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

</body>
</html>