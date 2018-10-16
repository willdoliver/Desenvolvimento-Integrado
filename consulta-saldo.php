<?php

try {
	$conn = new PDO("mysql:host=200.134.10.221;dbname=wolverine", "wolverine", "@wolverine#");
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo 'ERROR: ' . $e->getMessage();
}

$clientes = $conn->query('SELECT id_cliente, nome_cliente FROM clientes');
  
foreach($clientes as $cliente) {
    echo $cliente['id_cliente'] . " - ".  $cliente['nome_cliente'] ."\n"; 
    exit;
}

$cartoes = $conn->query('SELECT id_cartao, cod_seg, data_vcto FROM cartoes WHERE idfk_cliente = ' . $conn->quote($cliente['id_cliente']));


?>