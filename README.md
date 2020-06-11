# Projeto Final - DesSoft - 1A:

* Jogo Into The Tunnel


# Integrantes do Grupo:

* Bruno Conte Paiva
* Guilherme Schmulevich de Souza Aranha
* Leonardo dos Santos Alvarez

# Video exemplo do jogo sendo jogado:
* https://youtu.be/dCp7KLK1YyU

# Detalhes do projeto:

* O projeto foi feito em python, usando apenas o pygame como dependencia que não vem inclusa no python.
* O jogo eh composto por duas telas: o menu e o tunel.
* Os controles disponíveis são:
  * No menu: [ENTER] para começar o jogo, [E] para apagar os scores gravados.
  * No tunel: [ESPAÇO] para fazer a personagem voar. (soltar o [ESPAÇO] faz com que a personagem caia)
* O objetivo do jogo eh percorrer a maior distancia dentro do tunel sem ser acertado por um obstáculo.
* Foram usados como fonte de pesquisa para a criação do código apenas os dois tutoriais fornecidos pelo professor Luciano Soares sobre pygame e a documentação do pygame em https://www.pygame.org
* Todas as imagens foram criadas a partir dos TileSets gratuitos do site https://www.gameart2d.com, com exceção do personagem do jogador, que foi tirado do site https://icons8.com. As versões originais de todas as imagens tiradas desses dois sites estão na pasta imagens\ originais/. Usamos o Photoshop para adaptarmos a maioria das imagens usadas.
* A música tema do jogo foi tirada do site https://patrickdearteaga.com/royalty-free-music/, enquanto o som da batida foi criado artesanalmente.
* Como recurso complementar, implementamos o armazenamento dos scores em um arquivo separado do código principal chamado score_arquivo.db, com o uso do módulo Shelve, para que os scores não fossem reiniciados cada vez que o jogo fosse aberto.  


