<?php
// Incluir el archivo de conexión (usa el usuario 'cliente_granfondo_ct')
require_once '../config/db.php';

// Verificar que se ha recibido un ID válido por la URL
if (isset($_GET['id']) && !empty($_GET['id'])) {
    // Forzar que el ID sea un número entero por seguridad
    $id = intval($_GET['id']);

    try {
        // Preparar la consulta SQL de eliminación (Requiere permiso DELETE)
        $sql = "DELETE FROM participantes WHERE id = :id";
        $stmt = $pdo->prepare($sql);
        
        // Ejecutar pasando el parámetro del ID
        $stmt->execute([':id' => $id]);
        
        // Redirigir de vuelta a admin.php con bandera de éxito
        header("Location: admin.php?status=deleted");
        exit;

    } catch (PDOException $e) {
        // En caso de fallo, detener y mostrar el error técnico
        die("Error crítico: No se pudo eliminar el registro. Detalle: " . $e->getMessage());
    }
} else {
    // Si se accede al archivo sin un ID, redirigir al panel sin hacer nada
    header("Location: admin.php");
    exit;
}
?>