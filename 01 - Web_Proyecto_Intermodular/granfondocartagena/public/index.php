// PARTE PHP
<?php

// Manejo de estado - Persistencia de datos
session_start();

// Importación e inyección de código del archivo db.php (conexión PDO a la BBDD)
require_once '../config/db.php';

// Constante de control: aforo máximo de inscritos
define("PLAZAS_TOTALES", 500);

// ALGORITMO DE CARGA DE DATOS
// Con Manejo de excepciones
try {
    // Algoritmo de carga dinámica: Consulta de Categorías desde BBDD
    // Se evita emplear SELECT *
    // SQL a ejecutar
    $sqlcategorias = "SELECT id, nombre, distancia, desnivel, precio FROM categorias ORDER BY id ASC";
    // Envio de la sentencia SQL a la BBDD mediante el objeto de conexión PDO
    $stmtcategorias = $pdo->query($sqlcategorias);
    // Variable que guarda todas las rutas de la BBDD -> posterior inyección en el HTML
    $categorias = $stmtcategorias->fetchAll(PDO::FETCH_ASSOC);

    // Algoritmo para el marcador en vivo: Conteo dinámico de participantes registrados
    // SQL a ejecutar
    $sqlcuenta = "SELECT COUNT(*) FROM participantes";
    // Envio de la sentencia SQL a la BBDD mediante el objeto de conexión PDO
    $stmtcuenta = $pdo->query($sqlcuenta);
    // Variable que almacena el número de inscritos actualizado -> posterior inyección en el HTML
    $totalInscritos = $stmtcuenta->fetchColumn();
    
    // Cálculo de vacantes para inscripción -> variable para posterior inyección en el HTML
    $plazasDisponibles = PLAZAS_TOTALES - $totalInscritos; 

} catch (PDOException $e) {
    die("Error en la conexión: " . $e->getMessage());
}

?>

// PARTE HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gran Fondo Cartagena 2026 - Homenaje Equipo Reynolds</title>
    <meta name="description" content="One Page Web - Proyecto Intermodular 1º DAM">
    <meta name="keywords" content="uax, fp online uax, uax online, one page web, parallax, php">
    
    <!--Enlace a la hoja con los estilos-->
    <link rel="stylesheet" href="../assets/css/style.css">

    <!--Descarga de la biblioteca jQuery-->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
</head>
<body class="modo-claro">

    <!--BARRA SUPERIOR - Bloque con enlaces de navegación-->
    <nav class="barra-menu">
        <div class="contenedor-barra">
            <span class="marca">GF CARTAGENA-REYNOLDS</span>
            
            <ul class="enlaces-secciones">
                <li class="desplegable">
                    <!--Desplegable-->
                    <a href="#" class="desplegable-toggle">MENÚ ▾</a>
                    <!--Enlaces a las secciones-->
                    <ul class="desplegable-menu">
                        <li><a href="#inicio">Inicio</a></li>
                        <li><a href="#datos">Recorridos</a></li>
                        <li><a href="#servicios">Servicios</a></li>
                        <li><a href="#inscripciones">Inscripciones</a></li>
                    </ul>
                </li>
                <!--Elemento asociado al cambio de modo de luminosidad-->
                <li><a href="#" id="toggleMode">Modo Oscuro</a></li>
            </ul>
        </div>
    </nav>

    <!--SECCIÓN PORTADA - PRESENTACIÓN DEL EVENTO-->
    <header id="inicio" class="seccion-parallax presentacion">
        <div class="filtro-fotos">
            <div class="contenido-inicio animacion-entrada">
                <div class="insignia-reynolds">REYNOLDS RETRO</div>
                <h1>GRAN FONDO CARTAGENA</h1>
                <p class="fecha-evento">14 de Junio de 2026 | Cartagena, España</p>
                <p class="slogan">De vuelta a los 80 en los puertos de Cartagena</p>
                <a href="#inscripciones" class="boton-ppal desplaza-suave">INSCRIBETE YA</a>
            </div>
        </div>
    </header>

    <!--SECCIÓN PRINCIPAL-->
    <main>
        <!-- SECCIÓN 1: LA EXPERIENCIA -->
        <section id="datos" class="seccion-parallax seccion-experiencia">
            <div class="contenedor-reducido texto-centrado">
                <h2 class="titulo-seccion">LA EXPERIENCIA</h2>
                
                <!-- Rejilla para 3 tarjetas -->
                <div class="rejilla-flex rejilla-3 max-ancho-contenedor">
                    <div class="tarjeta-metricas">
                        <span class="metrica">180 KM</span>
                        <p class="dato-metrica">Distancia Máxima</p>
                    </div>
                    <div class="tarjeta-metricas">
                        <span class="metrica">3.500 M</span>
                        <p class="dato-metrica">Desnivel Acumulado</p>
                    </div>
                    <div class="tarjeta-metricas">
                        <span class="metrica"><?= $totalInscritos; ?></span>
                        <p class="dato-metrica">Valientes Inscritos</p>
                    </div>
                </div>

                <h3 class="seccion-subtitulo">RECORRIDOS DISPONIBLES</h3>

                <!-- Rejilla para 3 tarjetas -->
                <div class="rejilla-flex rejilla-3 max-ancho-contenedor" style="margin-top: 30px;">
                    <!-- Bucle para pintar las categorias tomadas de la variable $categorias -->
                    <!-- Una tarjeta por categoría -->
                    <?php foreach ($categorias as $cat): ?>
                        <!-- Mediante clases y CSS se preparan las tarjetas para giro 3D -->
                        <div class="contenedor-tarjeta-recorrido">
                            <div class="eje-tarjeta-recorrido">
                                
                                <!-- Cara delantera -->
                                <div class="frontal-tarjeta-recorrido">
                                    <h4><?= htmlspecialchars($cat['nombre']); ?></h4>
                                </div>
                                
                                <!-- Cara trasera -->
                                <div class="trasera-tarjeta-recorrido">
                                    <div class="encabezado-tarjeta">
                                        <h4><?= htmlspecialchars($cat['nombre']); ?></h4>
                                    </div>
                                    <div class="cuerpo-tarjeta">
                                        <p class="valores-recorrido"><strong>Distancia:</strong> <?= htmlspecialchars($cat['distancia']); ?></p>
                                        <p class="valores-recorrido"><strong>Desnivel:</strong> <?= htmlspecialchars($cat['desnivel']); ?></p>
                                        <div class="precio-recorrido"><?= number_format($cat['precio'], 2, ',', '.'); ?> €</div>
                                    </div>
                                </div>

                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </section>

        <div class="seccion-parallax parallax-seccion-media">
            <div class="filtro-fotos flex-centrado">
                <blockquote class="frase-inspiracion">
                    "Sin pinganillo; suda, sufre y revienta"
                </blockquote>
            </div>
        </div>

        <!-- SECCIÓN 2: SERVICIOS -->
        <section id="servicios" class="seccion-parallax seccion-servicios">
            <div class="contenedor-reducido">
                <h2 class="titulo-seccion texto-centrado">SERVICIOS</h2>
                <!-- Rejilla para 2 tarjetas -->
                <div class="rejilla-flex grid-2">
                    <div class="tarjeta-servicio">
                        <h3>Servicios en Carrera</h3>
                        <ul>
                            <li>Avituallamientos líquidos y sólidos.</li>
                            <li>Regalo de Maillot oficial conmemorativo Reynolds Retro.</li>
                            <li>Comida post-carrera</li>
                            <li>Asistencia mecánica neutral y coche escoba.</li>
                        </ul>
                    </div>
                    <div class="tarjeta-servicio">
                        <h3>Alojamientos Recomendados</h3>
                        <ul>
                            <li>Acuerdos oficiales con los mejores hoteles de la comarca de Cartagena, con zonas de videovigilancia para guardar las bicicletas y horarios de desayuno adelantados para el corredor</li>
                            <li>Solicita tu plaza de alojamiento junto con tu inscripción del formulario inferior.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECCIÓN 3: INSCRIPCIONES -->
        <section id="inscripciones" class="seccion-parallax seccion-boletin">
            <div class="contenedor-formulario">
                <h2 class="titulo-seccion texto-centrado" style="color: var(--primary-color); margin-bottom: 1.5rem;">BOLETÍN DE INSCRIPCIÓN</h2>
                
                <div class="contador-vivo texto-centrado">
                    <span class="numero-inscritos">¡Ya somos <strong><?= $totalInscritos; ?></strong> valientes apuntados!</span>
                    <span class="numero-plazas">¡Solo quedan <strong><?= $plazasDisponibles; ?></strong> plazas disponibles!</span>
                </div>

                <!-- Renderizado del mensaje de éxito en la inscripción -->
                <?php if (isset($_SESSION['msg_exito'])): ?>
                    <div class="alerta alerta-exito"><?= $_SESSION['msg_exito']; unset($_SESSION['msg_exito']); ?></div>
                <?php endif; ?>
                <!-- Renderizado del mensaje de error en la inscripción -->
                <?php if (isset($_SESSION['msg_error'])): ?>
                    <div class="alerta alerta-error"><?= $_SESSION['msg_error']; unset($_SESSION['msg_error']); ?></div>
                <?php endif; ?>

                <!-- FORMULARIO DE INSCRIPCIÓN -->
                <!-- Todos los campos obligatorios (required) -->

                <!-- Llamada al archivo registrar.php --> 
                <form action="registrar.php" method="POST" class="formulario-inscribe">
                    <div class="grupo-formulario">
                        <label for="nombre">Nombre:</label>
                        <input type="text" id="nombre" name="nombre" placeholder="Tu nombre" required>
                    </div>
                    
                    <div class="grupo-formulario">
                        <label for="apellidos">Apellidos:</label>
                        <input type="text" id="apellidos" name="apellidos" placeholder="Tus apellidos" required>
                    </div>

                    <div class="grupo-formulario">
                        <label for="dni">DNI (Con letra, sin guiones):</label>
                        <input type="text" id="dni" name="dni" placeholder="Ej: 12345678Z" required>
                    </div>

                    <div class="grupo-formulario">
                        <label for="email">Correo Electrónico:</label>
                        <input type="email" id="email" name="email" placeholder="ejemplo@correo.com" required>
                    </div>

                    <div class="grupo-formulario">
                        <label for="id_categoria">Elige tu Recorrido:</label>
                        <select id="id_categoria" name="id_categoria" required>
                            <option value="">-- Selecciona una ruta --</option>
                            <!-- Pinta las categorías en el desplegable -->
                            <?php foreach ($categorias as $cat): ?>
                                <option value="<?= $cat['id']; ?>"><?= htmlspecialchars($cat['nombre']); ?> (<?= $cat['distancia']; ?>)</option>
                            <?php endforeach; ?>
                        </select>
                    </div>

                    <div class="grupo-formulario">
                        <label>¿Deseas incluir alojamiento oficial?</label>
                        <div class="radio-inline">
                            <label><input type="radio" name="alojamiento" value="Si"> Opción: Alojamiento y carrera</label>
                            <label><input type="radio" name="alojamiento" value="No" checked> Opción: Solo carrera</label>
                        </div>
                    </div>

                    <div class="texto-centrado" style="margin-top: 25px;">
                        <button type="submit" class="boton-envio">CONFIRMAR INSCRIPCIÓN</button>
                    </div>
                </form>
            </div>
        </section>
    </main>

    <!-- PIE DE PÁGINA: Descripción u patrocinios con enlaces externos -->
    <footer class="pie-pagina">
        <p>&copy; 2026 Gran Fondo Cartagena - Proyecto Intermodular 1º DAM - UAX. Francisco José García Franco</p>
        <p class="titulo-patrocinios">Patrocinadores de Leyenda</p>
        <!-- Rejilla con patrocinadores (logos y enlaces a sus webs) -->
        <div class="rejilla-patrocinios max-ancho-contenedor">
            <a href="https://www.pinarello.com" target="_blank" class="elemento-patrocinio" title="Cuadros Pinarello - Web Oficial">
                <img src="../assets/img/logo-pinarello.png" alt="Cuadros Pinarello" class="logo-patrocinio">
            </a>
            <a href="https://www.campagnolo.com" target="_blank" class="elemento-patrocinio" title="Componentes Campagnolo - Web Oficial">
                <img src="../assets/img/logo-campagnolo.png" alt="Componentes Campagnolo" class="logo-patrocinio">
            </a>
            <a href="https://www.cartagena.es" target="_blank" class="elemento-patrocinio" title="Ayuntamiento de Cartagena - Web Oficial">
                <img src="../assets/img/logo-ayto.png" alt="Ayuntamiento de Cartagena" class="logo-patrocinio">
            </a>
        </div>
        
        <!-- ACCESO INTERNO A ORGANIZADOR PARA GESTIONAR INSCRITOS -->
        <p style="margin-top: 25px;">
            <a href="admin.php" class="acceso-organizador" onclick="var clave = prompt('Introduce la contraseña de la Organización:');
            if (clave === 'Reynolds1980') {
                return true; // Contraseña correcta, deja pasar a admin.php
            } else {
                alert('❌ Contraseña incorrecta. Acceso denegado.');
            return false; // Cancela el clic y no te lleva a ningún lado
        }
    ">Acceso Interno Organización</a>
</p>


    </footer>

    <!-- jQuery para gestión de cambio de modo claro/oscuro y desplazamiento fluido entre secciones -->
    <script>
        
        $(document).ready(function() {
        
            <!-- Control manual cambio modos claro/oscuro -->                    
            $('#toggleMode').click(function(e) {
                e.preventDefault();
                if ($('body').hasClass('modo-claro')) {
                    enableDarkMode();
                } else {
                    enableLightMode();
                }
            });

            <!-- Control automático cambio modos claro/oscuro: según horario -->  
            <!-- De 00:00 a 08:00 modo oscuro -->                    
            <!-- De 08:00 a 20:00 modo claro -->                    
            <!-- De 20:00 a 24:00 modo oscuro -->                    
            var currentHour = new Date().getHours();
            if (currentHour >= 20 || currentHour < 8) {
                enableDarkMode();
            } else {
                enableLightMode();
            }

            <!-- Funciones auxiliares para cambio de clases que define claro u oscuro -->                    
            function enableDarkMode() {
                $('body').removeClass('modo-claro').addClass('modo-oscuro');
                $('#toggleMode').text('Modo Claro');
            }

            function enableLightMode() {
                $('body').removeClass('modo-oscuro').addClass('modo-claro');
                $('#toggleMode').text('Modo Oscuro');
            }
        });
    </script>
</body>
</html>