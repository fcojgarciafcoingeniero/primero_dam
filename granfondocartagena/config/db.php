<?php
// Credenciales de acceso restringido para la página web
// Acceso en local
$host = 'localhost';
// BBDD = granfondo_cartagena
$dbname = 'granfondo_cartagena';
// Usuario creado explícitamente para gestionar la web: cliente_granfondo_ct
// Se evita emplear el usuario root y se emplean nombres que no son fácilmente adivinables
// Con permisos de lectura, escritura y borrado
$username = 'cliente_granfondo_ct';
// Contraseña para acceso a la BBDD
$password = 'cl5ent4.!Reynolds1980';

// Manejo de excepciones
try {
    // Configuración de la cadena de conexión PDO
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    
    // Configuración de directivas para el manejo de excepciones y vectores asociativos
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // Finalización del script en caso de error de conexión
    die("Error en la conexión a la base de datos: " . $e->getMessage());
}
?>
