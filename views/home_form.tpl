<!DOCTYPE html>

<html>
	<head>
		<title>WikiTree - Criar Wiki</title>
		<link rel="stylesheet" href="/static/css/home.css"/>
		<script src="home.js"></script>
	</head>
	<body>
		<form action="../wikis/create" method="post">
			<div class="header">
					<input type="text" name="nome" placeholder="Nome da Wiki" class="form-name">
			</div>
			<input type="text" name="titulo" placeholder="Título" class="form-title">
			<div class="form-main">
				<div class="link-table">
					<!-- inserir função para coletar os primeiros 10 links da database aqui -->
					<p> Suas páginas virão aqui. </p>
				</div>
				<textarea name="texto" placeholder="Descrição" class="form-description"></textarea>
			</div>
			<button type="submit"> Enviar </button>
		</form>
		<footer>
		<p> 2025, WikiTree. Todos os direitos reservados.</p>
		</footer>
	</body>
</html>
