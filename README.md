# Vendor management

O sisema contem diversas utilidades, irei citar alguma delas - 

- Recuperar a senha por e-mail caso tenha esquecido.
- Cadastro precisa de ativação e será enviado um link de ativação apra o seu email.
- Voce pode se cadastrar como Usuário comum ou Fornecedor.
- Cada usuário tem seu nivel de permissão, nem tudo eles podem fazer.
- Quando é criado um usuáio fornecedor, o Administrador tem que ir no cadastro e libera-lo.
- Faça as alterações do seu perfil
- Informações do perfil do Fornecedor é mais ompleta
- O Admin pode adicionar categorias, produtos e fazer demais alterações

<img src='video.gif' width=500px>

### remover o `-example` do arquivo `.env-example`

## Passo a passo
- Crie um ambiente virtual na sua máquie e em seguida instale as deçendências
~~~shell
pip install -r requirements.txt
~~~

- Crie um banco de dados Postgresql contendo as seguintes informações
~~~shell
DB_NAME=product_management
DB_USER=postgres
DB_PASSWORD=123
DB_HOST=localhost
DB_PORT=5432
~~~

- Faça um Migrate e crie um super usuário
~~~shell
python manage.py migrate
~~~
~~~shell
python manage.py createsuperuser
~~~

- Rode a aplicação
~~~shell
python manage.py runserver
~~~

- Abra a aplicação no navegador
~~~shell
http://127.0.0.1:8000/home
~~~

- Link da api -Liberação via Token pelo Admin
~~~shell
http://127.0.0.1:8000/api/v1/
~~~
