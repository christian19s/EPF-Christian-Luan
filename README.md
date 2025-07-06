# WikiTree: POO com Python + Bottle + Sqlite

WikiTree é um projeto de template educacional voltado para o ensino de **Programação Orientada a Objetos (POO)** do Prof. Lucas Boaventura, Universidade de Brasília (UnB).

Utiliza o microframework **Bottle**. Ideal para uso em disciplinas introdutórias de Engenharia de Software ou Ciência da Computação.

Utiliza de bibliotecas extras como:
## 💡 Objetivo

Criar e implementar um sistema de wikis organizadas por categoria (jogos,filmes,livros, etc)

---

## 🗂 Estrutura de Pastas

```bash
WikiTree
├── controllers
├── data
│   ├── db
│   └── uploads
│       ├── users
│       └── wiki
├── models
├── services
├── static
│   ├── css
│   ├── exceptions
│   ├── img
│   └── js
└── views
```


---

## 📁 Descrição das Pastas

### `controllers/`
Contém as classes responsáveis por lidar com as rotas da aplicação. Exemplos:
- `user_controller.py`: rotas para listagem, adição, edição, remoção e autenticação de usuários.
- `base_controller.py`: classe base com utilitários comuns.
- `wiki_controller.py` rotas para operções de wiki como a criação, remoção, listagem e organização

### `models/`
Define as classes que representam os dados da aplicação. Exemplo:
- `user.py`: classe `User`, com atributos como `id`, `name`, `email`, etc.
- `wiki.py`: classe `wiki_instance`, com atributos como `id`, `slug`, `categoria`, etc.

### `services/`
Responsável por salvar, carregar e manipular dados usando sqlite Exemplo:
- `user_service.py`: contém métodos como `get_all`, `add_user`, `delete_user`.
- `wiki_service.py`: contém métodos como `get_all`, `create_wiki`, `delete_wiki`.

### `views/`
Contém os arquivos `.tpl` utilizados pelo Bottle como páginas HTML:
- `layout.tpl`: estrutura base com navegação e bloco `content`.
- `users.tpl`: lista os usuários.
- `user_form.tpl`: formulário para adicionar/editar usuário.

### `static/`
Arquivos estáticos como:
- `css/style.css`: estilos básicos.
- `js/dark-mode.js` script de dark mode baseado em catpuccin e gruvbox
- `img/default-icon.png`: exemplo de imagem.

### `data/`
Armazena os arquivos salvos e o  banco de dados:
- `users/`: onde os dados dos usuários são persistidos.
- `wikis/`: onde os dados das wikis e suas instâncias são persistidos
---

## ▶️ Como Executar

1. Crie o ambiente virtual na pasta fora do seu projeto:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
```
alternativamente:

```bash
make docker
make run-docker
```

2. Entre dentro do seu projeto criado a partir do template e instale as dependências(não necessario para docker):
```bash
pip install -r requirements.txt
```

3. Rode a aplicação:
```bash
python main.py
```

4. Accese sua aplicação no navegador em: [http://localhost:8080](http://localhost:8080)

---

5. A fazer:
adiciona aqui o que tem a fazer christian:
1 -- modelagem
2 -- 



## ✍️ Personalização
Para adicionar novos modelos (ex: Atividades):

1. Crie a classe no diretório **models/**.

2. Crie o service correspondente para manipulação do JSON.

3. Crie o controller com as rotas.

4. Crie as views .tpl associadas.

---

# A FAZER:

- Docker []
- Deploy em um server 
- Database, portar o codigo existente para sql (sqlite) 
- Tratanento de imagens na DB
- Usuarios e admins:
  - sistema de autenticação
  - sistema de verificaçao de usuarios
- template da wiki funcional onde um usuario autenticado pode criar uma wiki:
  - deixar o editor customizar a wiki
  - salvar tudo isso na database de forma correta
- Tratamento de erros
- Diagrama
- Estilização de CSS
- JS e HTML da wiki
- remover tudo relacionado ao exemplo activity


## 🧠 Autor e Licença
Projeto desenvolvido como template didático para disciplinas de Programação Orientada a Objetos, baseado no [BMVC](https://github.com/hgmachine/bmvc_start_from_this).
Você pode reutilizar, modificar e compartilhar livremente.
