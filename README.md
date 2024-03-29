# COVID-19
Predizer o número de casos de COVID-19 mundialmente

 <h1>Ambiente de desenvolvimento:</h1>
 <p>Primeiro será baixado o ambiente para construção e treino do modelo e ambiente.</p>
 <pre><code>docker pull jupyter/datascience-notebook</code></pre>

<p>Em seguida, o comando para rodar o ambiente para desenvolvimento</p>
 <pre><code>docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "%cd%":/home/jovyan/work jupyter/datascience-notebook</code></pre>
 <p>Será gerada uma URL com token, basta copiá-la e acessar os arquivos.</p>
 <p>Link de apoio: https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html</p>
 
 <h3>Ideia</h3>

<h4>Dados são carregados atualizados a cada execução de atualização do modelos: "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"</h4>

 <h4>A ideia era verificar a relação dos dados e tentar montar uma
 forma onde pudesse utilizar o próprio número de novos casos ao longo dos dias para ter uma previsão do número de novos casos de um dia. Para isso se criou um array Numpy com tamanho da quantidade de dias até o atual momento, e em cada posição foi colocado um outro array contendo números de casos do dia/index do array atual até 9 dias a frente. Exemplo: Na posição 0 do Numpy array, que seria o primeiro dia com caso registrado no mundo, recebe um outro array contendo o número de novos casos desse primeiro dia e dos próximos 9. Esse valor 9 é arbitrário, foram testados alguns outros, mas o 9 teve bons resultados. </h4>

 <h4>Bom, já temos os dados para treinar e testar, e temos os labels para validar, que são o número de novos casos no dia simplesmente. Também de forma arbitrária foi escolhido o valor de 67% do conjunto de dados para treino e 33% para testes, apenas por ter dado bons resultados. Foram testados alguns modelos de regressão linear do SKLearn, como: LinearRegression, GradientBoostingRegressor, RidgeCV, entre outros. Mas o que mais se destacou foi o Lars. O score do modelo ficou na faixa de 97%. </h4>

 <h4>O modelo então é salvo em um arquivo, para que seja carregado e utilizado quando o programa que o usuário usa para prever os novos casos ao longo dos dias é executado.</h4>

 <h1>Produção:</h1>

 <h4>Foram separados em dois arquivos: build_model.py e predict.py. O build_model.py serve para atualizar o modelo diariamente, baseado nos dados reais, ele após treinar o novo modelo, salva-o como arquivo.</h4>
 <h5>Executar com Docker</h5>
 <pre><code>docker run --rm -it -v "%cd%":/usr/src/app -w /usr/src/app faizanbashir/python-datascience:3.6 python build_model.py</code></pre>

<h4>Enquanto o predict.py seria o arquivo destinado ao usuário, com ele basta passar o número de dias como parâmetro, que terá a saida desejada.</h4>
<h5>Executar com Docker</h5>
 <pre><code>docker run --rm -it -v "%cd%":/usr/src/app -w /usr/src/app faizanbashir/python-datascience:3.6 python predict.py <numero de dias></code></pre>
 
 <h4>Para a previsão ele vai gerando dia a dia, e salvando a previsão no array de novos casos para usar como entrada para prever o dia seguinte.</h4>
 
 <h1>Publicação:</h1>
 <h4>Para publicar seria interessante pensar em um front web que interagisse ou "direto" (através de um back-end) com o modelo salvo, ou então, com um banco não-relacional que se atualizasse todos os dias, contendo os números de previsão para dias seguintes</h4>
