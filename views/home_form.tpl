<!DOCTYPE html>

<html>
	<head>
		<title>WikiTree - Criar Wiki</title>
		<link rel="stylesheet" href="/static/css/home.css"/>
		<script src="home.js"></script>
	</head>
	<body>
		<div class="header">
			<form action="create/add" method="post">
				<input type="text" name="titulo" placeholder="Título" class="form-title">
				<button type="submit">Enviar</button>		
			</form>
		</div>
		<form action="create/add" method="post" class="form-table">
			<input type="text" name="titulo" placeholder="Título" class="form-title">
			<input type="text" name="texto" placeholder="Descrição" class="form-text">
			
			<button type="submit" class="form-button">Enviar</button>		
		</form>
		<footer>
		<p> 2025, WikiTree. Todos os direitos reservados.</p>
		</footer>
	</body>
</html>
