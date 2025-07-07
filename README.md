# WikiTree: POO com Python + Bottle + Sqlite

WikiTree é um projeto de template educacional voltado para o ensino de **Programação Orientada a Objetos (POO)** do Prof. Lucas Boaventura, Universidade de Brasília (UnB).

Utiliza o microframework **Bottle**. Ideal para uso em disciplinas introdutórias de Engenharia de Software ou Ciência da Computação.

Utiliza de bibliotecas extras como: hashlib, [Tost ui](https://ui.toast.com/tui-editor), Markdown render
## 🎯 Objetivo do Projeto

### 📌 Funcionalidades Principais:
- **Sistema de Wikis Organizadas por Categoria**  
  - Implementar categorias como jogos, filmes, livros, etc.  
  - Permitir navegação e filtragem por categoria.  

- **Persistência em Banco de Dados SQL**  
  - Armazenar wikis, páginas, usuários e categorias em um banco relacional (SQLite/PostgreSQL).  
  - Garantir integridade dos dados com relações adequadas (chaves estrangeiras).  

- **Sistema de Permissões Robustas**  
  - Definir níveis de acesso (ex: `viewer`, `editor`, `admin`, `superadmin`).  
  - Restringir edição/exclusão com base em:  
    - **Papel global do usuário** (ex: `superadmin` pode editar todas as wikis).  
    - **Papel em wikis específicas** (ex: `moderator` só na wiki X).  
  - Implementar verificações de permissão em todas as operações críticas.  

### 🔧 Requisitos Técnicos:
- **Backend**:  
  - Classes Python para modelos (`Wiki`, `Category`, `User`, `PermissionSystem`).  
  - Operações CRUD com SQL (via `sqlite3`)

- **Segurança**:  
  - Hash de senhas com `bcrypt`.  
  - Middleware para validar permissões antes de cada ação.  

- **Extensibilidade**:  
  - Design modular para adicionar novas categorias/permissões futuramente.  

---

## 🗂 Estrutura de Pastas

```bash
WikiTree
├── controllers
├── data
│   ├── db
│   └── uploads
│       ├── users # uploads relativos a usuario
│       └── wiki # uploads relativos a wikis 
├── models
├── services
├── static
│   ├── css
│   ├── exceptions
│   ├── img
│   └── js # scripts relativos
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

## diagrama de classes UML ![diagrama_de_classesUML](https://github.com/user-attachments/assets/3947d5f0-3b85-437c-8bbe-62f5828d4559)


## 🧠 Autor e Licença
Projeto desenvolvido como template didático para disciplinas de Programação Orientada a Objetos, baseado no [BMVC](https://github.com/hgmachine/bmvc_start_from_this).
Você pode reutilizar, modificar e compartilhar livremente. sob a licensa GPL  2.0
