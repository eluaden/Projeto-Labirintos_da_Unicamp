from jogador import Jogador

class Moderador:
    def _init_(self, jogo):
        self.jogo = jogo

    def atualizar_tempo(self, jogador:Jogador):
        jogador.tempo_restante -= 1
        if jogador.tempo_restante <= 0:
            self.verificar_fim_de_jogo(jogador)

    def verificar_fim_de_jogo(self, jogador:Jogador):
        if jogador.vidas <= 0 or jogador.tempo_restante <= 0:
            # Aqui haverá algum tipo de interrupção no loop principal do jogo
            print("Fim de jogo!")
    
    def reiniciar_labirinto(jogador:Jogador, tempo_max):
        jogador.posicao_atual = [0,0]
        jogador.vidas = 5
        jogador.tempo_restante = tempo_max

    def verificar_colisao(self, jogador):
        x, y = jogador.posicao

        for professor in self.jogo.professores:
            if (x, y) == professor.posicao:
                #Chamar a funçao da classe professor
                print('fazendo......')

        for tipo_item, posicoes in self.jogo.itens.items():
            if (x, y) in posicoes:
                if tipo_item == 'pontos':
                    jogador.incrementar_pontos(10)
                elif tipo_item == 'vidas':
                    jogador.incrementar_vidas(1)
                elif tipo_item == 'bombas':
                    jogador.inventario.append('bomba')
                posicoes.remove((x, y))