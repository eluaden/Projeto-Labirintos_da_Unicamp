# Os Labirintos da Unicamp

## Descrição

"Os Labirintos da Unicamp" é um jogo desenvolvido em Python, inspirado no jogo "Laberinto del Saber". O objetivo do jogador é completar diferentes labirintos, coletar pontos e interagir com professores dentro de um tempo limite. O jogador deve acumular NOTA suficiente para avançar para o próximo labirinto, enquanto deve responder as perguntas dos professores que se movimentam pelo labirinto. O jogo possui vários níveis de dificuldade e funcionalidades, incluindo salvamento e carregamento de estado do jogo, tabela de pontuação, Nível extra(que é ilimitado) e muito mais.

## Funcionalidades

- Navegação em labirintos com diferentes layouts e níveis de dificuldade.
- Coleta de nota espalhados pelos labirintos.
- Interação com professores (guardians).
- Perguntas de cultura geral com múltipla escolha para derrotar os professores.
- Itens especiais como relógios (tempo extra), corações (vidas extras), e bombas.
- Sistema de vidas e tempo limite para completar cada labirinto.
- Tela de menu inicial com opções Jogar, classificação e informações.
- Tabela de pontuação armazenada em arquivo, exibindo os melhores jogadores.
- Salvamento e carregamento do estado do jogo a partir de arquivos.
- Banco de dados local para salvar dados dos usuários.

## Requisitos

- Python 3.x
- Pygame
- pip install opencv-python

## Como Rodar

1. Certifique-se de ter o Python 3.x e o Pygame instalados em sua máquina.
2. Clone o repositório ou extraia o arquivo zip contendo o código-fonte.
3. Navegue até o diretório do projeto no seu terminal.
4. Execute o comando `python src/main.py` para iniciar o jogo.

## Estrutura do Projeto

- `main.py`: Arquivo principal para iniciar o jogo.
- `src/`: Contém os arquivos fonte do jogo.
- `assets/`: Contém os recursos do jogo, como imagens e sons.
- `data/`: Contém arquivos de dados, incluindo o banco de dados de usuários e estados salvos do jogo.

## Controles do Jogo

- Use as teclas de direção do teclado para mover o aluno pelo labirinto.
- Use a tecla `space` para acionar as bombas.

## Informações Adicionais

- O jogo salva automaticamente o estado do jogador e a tabela de pontuação em arquivos locais.
- Se o jogador perder todas as vidas, ele será adicionado ao banco de dados local como um colega que pode ser salvo em jogos futuros.

## Autores

Este jogo foi desenvolvido por Rafael Feltrin e Lucas Souza como parte de um projeto da disciplina de Algoritmo e Programação da Unicamp.

