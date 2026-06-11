<?php
// Manejo de estado - Persistencia de datos
session_start();

// Importación e inyección de código del archivo db.php (conexión PDO a la BBDD)
require_once '../config/db.php';

// Comprobar si se ha enviado el formulario por POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Recoger y limpiar datos del formulario
    $nombre = isset($_POST['nombre']) ? trim($_POST['nombre']) : "";
    $apellidos = isset($_POST['apellidos']) ? trim($_POST['apellidos']) : "";
    $dni = isset($_POST['dni']) ? trim($_POST['dni']) : "";
    $email = isset($_POST['email']) ? trim($_POST['email']) : "";
    $id_categoria = isset($_POST['id_categoria']) ? trim($_POST['id_categoria']) : "";
    $alojamiento = isset($_POST['alojamiento']) ? trim($_POST['alojamiento']) : "";

    // Validación básica: campos obligatorios
    if (empty($nombre) || empty($apellidos) || empty($dni) || empty($email) || empty($id_categoria)) {
        $_SESSION['msg_error'] = "Todos los campos obligatorios, incluido el recorrido, deben ser rellenados.";
        header("Location: index.php#inscripciones");
        exit;
    } 
    
    // Validación de formato de email
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $_SESSION['msg_error'] = "El formato del correo electrónico no es válido.";
        header("Location: index.php#inscripciones");
        exit;
    }

    try {
        // Consulta SQL de inserción con todos los campos previamente validados
        $sql = "INSERT INTO participantes (nombre, apellidos, dni, email, id_categoria, alojamiento) 
                VALUES (:nombre, :apellidos, :dni, :email, :id_categoria, :alojamiento)";
        
        // Prepared Statement con la consulta
        $stmt = $pdo->prepare($sql);
        
        // Ejecuta la consulta pasando los valores mapeados
        $stmt->execute([
            ':nombre' => $nombre,
            ':apellidos' => $apellidos,
            ':dni' => $dni,
            ':email' => $email,
            ':id_categoria' => $id_categoria,
            ':alojamiento' => $alojamiento
        ]);

        //Si registro exitoso: se guarda el mensaje en la sesión y redirige a la index
        $_SESSION['msg_exito'] = "¡Inscripción realizada correctamente!";
        header("Location: index.php#inscripciones");
        exit;
        
    } catch (PDOException $e) {
        // Si registro fallido: se guarda el fallo técnico en la sesión y redirige a la index
        $_SESSION['msg_error'] = "Error al guardar en la base de datos: " . $e->getMessage();
        header("Location: index.php#inscripciones");
        exit;
    }
} else {
    // Si se intenta entrar a registrar.php directamente con la URL (no envio por POST desde el formulario) --> devuelve a la index
    header("Location: index.php");
    exit;
}
?>