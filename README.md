# COVID-19
Predizer o número de casos de COVID-19 mundial

 <h1>Ambiente de desenvolvimento:</h1>
 Primeiro será baixado o ambiente para construção e treino do modelo - '''docker pull jupyter/datascience-notebook'''.

Em seguida, o comando para rodar o ambiente para desenvolvimento
 '''docker run --rm -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes -v "%cd%":/home/jovyan/work jupyter/datascience-notebook'''

 Link de apoio: https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html
