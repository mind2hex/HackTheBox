Este codigo no esta en un orden especifico, simplemente estan las lineas de codigo especificas que dieron lugar a la vulnerabilidad

<?php

/* 
 * Una de las principales fallas se encuentra en esta funcion.
 * Esta funcion se encarga de retornar la variable de la solicitud HTTP
 * sin aplicarle ningun filtro, asi por ejemplo cuando se solicita el valor de 
 * poller_id, no se le aplica ningun filtro a pesar de que este pueda contener codigo
 * maligno.
 */
function get_nfilter_request_var($name, $default = '') {
	global $_CACTI_REQUEST;
	if (isset($_CACTI_REQUEST[$name])) {
		return $_CACTI_REQUEST[$name];
	} elseif (isset($_REQUEST[$name])) {
		return $_REQUEST[$name];
	} else {
		return $default;
	}
}

// codigo sin corregir
$local_data_ids = get_nfilter_request_var('local_data_ids');
$host_id        = get_filter_request_var('host_id');
$poller_id      = get_nfilter_request_var('poller_id'); // en $poller_id se aloja el payload 
$return         = array();
if (function_exists('proc_open')) {
    /* 
     * La funcion proc_open sirve para ejecutar comandos del sistema de forma asincrona, sin embargo
     * lo importante radica en que como no se le aplicaron filtros ni se realizo un escapeshellargs a la variable poller_id
     * dicha variable se esta pasando directo sin sanear a la funcion proc_open, por lo que lo unico que tendrian que agregar es 
     * un payload tipo "1; whoami" para ejecutar codigo
     */
	$cactiphp = proc_open(read_config_option('path_php_binary') . ' -q ' . $config['base_path'] . '/script_server.php realtime ' . $poller_id, $cactides, $pipes);
    $output = fgets($pipes[1], 1024);
	$using_proc_function = true;
} else { 
}

// codigo corregido
$local_data_ids = get_nfilter_request_var('local_data_ids');
$host_id        = get_filter_request_var('host_id');
$poller_id      = get_filter_request_var('poller_id');
$return         = array();
if (function_exists('proc_open')) {
    $cactiphp = proc_open(read_config_option('path_php_binary') . ' -q ' . $config['base_path'] . '/script_server.php realtime ' . cacti_escapeshellarg($poller_id), $cactides, $pipes);
    $output = fgets($pipes[1], 1024);
	$using_proc_function = true;
} else {
}

?>