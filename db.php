<?php
	print_r($_GET);
	print_r($_POST);
	session_start();
	$_SESSION["srgtest"]=time();
	print_r($_SESSION);

	
	


?>

<script>
	
	alert("<?php echo($_SESSION["srgtest"]); ?>");
	alert("srg test");
</script>