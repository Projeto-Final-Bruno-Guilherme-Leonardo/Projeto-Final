# Projeto Final - DesSoft - 1A:

* Jogo Into The Tunnel


# Integrantes do Grupo:

* Bruno Conte Paiva
* Guilherme Schmulevich de Souza Aranha
* Leonardo dos Santos Alvarez

# Video exemplo do jogo sendo jogado:
* https://youtu.be/dCp7KLK1YyU

# Detalhes do projeto:

* O projeto foi feito em python, usando apenas o pygame como dependencia que nao vem inclusa no python.
* O jogo eh composto por duas telas: o menu e o tunel.
* Os controles disponiveis sao:
  * No menu: [ENTER] para comecar o jogo, [E] para apagar os scores gravados.
  * No tunel: [ESPACO] para fazer a personagem voar. (soltar o [ESPACO] faz com que a personagem caia)
* O objetivo do jogo eh percorrer a maior distancia dentro do tunel sem ser acertado por um obstaculo.
* Foram usados como fonte de pesquisa para a criacao do codigo apenas os dois tutoriais fornecidos pelo professor Luciano Soares sobre pygame e a documentacao do pygame em https://www.pygame.org
* Todas as imagens foram criadas a partir dos TileSets gratuitos do site https://www.gameart2d.com, com excecao do personagem do jogador, que foi tirado do site https://icons8.com. As versoes originais de todas as imagens tiradas desses dois sites estao na pasta imagens\ originais/. Usamos o Photoshop para adaptarmos a maioria das imagens usadas.
* A musica tema do jogo foi tirada do site https://patrickdearteaga.com/royalty-free-music/, enquanto o som da batida foi criado artesanalmente.
* Como recurso complementar, implementamos o armazenamento dos scores em um arquivo separado do codigo principal chamado score_arquivo.db, com o uso do modulo Shelve, para que os scores nao fossem reiniciados cada vez que o jogo fosse aberto.  


