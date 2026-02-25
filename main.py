"""
AVENTURA DAS LETRAS
Jogo educativo de plataforma para ensino fundamental
Desenvolvido para projeto de extensão - SI 5º período

Versão Modular - Sistema dinâmico de plataformas
"""

import pygame
import sys
from relatorio import RelatorioAluno
from config import (
    LARGURA, ALTURA, FPS,
    FACIL, MEDIO, DIFICIL
)
from nivel import Nivel
from tela_formacao import TelaFormacao
from telas import TelaMenu, TelaFim
from typing import Optional


class Jogo:
    """Classe principal que gerencia o jogo"""
    
    def __init__(self):
        # Inicialização do Pygame
        pygame.init()
        
        # Configurar tela
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Aventura das Letras")
        
        # Clock
        self.clock = pygame.time.Clock()

        # Tempo total de jogo
        self.tempo_inicio = pygame.time.get_ticks()
        self.tempo_total = 0
        
        # Fontes
        self.fonte_titulo = pygame.font.Font(None, 80)
        self.fonte_grande = pygame.font.Font(None, 64)
        self.fonte_media = pygame.font.Font(None, 48)
        self.fonte_pequena = pygame.font.Font(None, 32)
        
        # Estado do jogo
        self.estado = "menu"
        self.ra_aluno = ""
        self.digitando_ra = True
        self.nome_aluno = ""
        self.digitando_nome = False
        self.nivel_atual = 0

        # Pontuação Global
        self.pontuacao_total = 0
        self.erros_totais = 0
        self.acertos_totais = 0
        
        # Lista de palavras - agora suporta palavras de qualquer tamanho!
        self.palavras = [
            "GATO", 
            "BOLA", 
            # "CASA", 
            # "FLOR", 
            # "LIVRO",            
            # "COMPUTADOR",
            # "FELICIDADE",
            # "PARALELEPIPEDO",
            # "ANTICONSTITUCIONALISSIMAMENTE"
        ]
        
        self.nivel: Optional[Nivel] = None
        self.tela_formacao: Optional[TelaFormacao] = None
        
        # Dificuldades
        self.dificuldades = [FACIL, MEDIO, DIFICIL]
        self.dificuldade_atual = 0
        
    def iniciar_nivel(self):
        """Inicia um novo nível"""
        if self.nivel_atual < len(self.palavras):
            palavra = self.palavras[self.nivel_atual]
            dificuldade = self.dificuldades[self.dificuldade_atual]
            self.nivel = Nivel(palavra, dificuldade, self.fonte_media)
            self.estado = "jogando"
        else:
            # Calcula tempo total antes de finalizar
            self.tempo_total = (pygame.time.get_ticks() - self.tempo_inicio) // 1000

            # Gerar relatório antes de ir para tela final
            RelatorioAluno.gerar(
                self.ra_aluno,
                self.nome_aluno,
                self.palavras,
                self.acertos_totais,
                self.erros_totais,
                self.pontuacao_total,
                self.tempo_total
            )

            TelaFim.iniciar_serpentinas()
            self.estado = "fim"

            
    def proximo_nivel(self):
        """Avança para o próximo nível"""

        # Acumula pontuação global
        if self.nivel:
            self.pontuacao_total += self.nivel.pontuacao
            self.acertos_totais += self.nivel.acertos
            self.erros_totais += self.nivel.erros

        # Avança nível
        self.nivel_atual += 1

        # A cada 2 níveis aumenta dificuldade
        if self.nivel_atual % 2 == 0 and self.dificuldade_atual < 2:
            self.dificuldade_atual += 1

        self.iniciar_nivel()

        
    def processar_eventos(self):
        """Processa eventos do jogo"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
                
            if evento.type == pygame.KEYDOWN:
                
                # Tecla ESC fecha o jogo
                if evento.key == pygame.K_ESCAPE:
                    return False

                # Menu - digitando nome
                if self.estado == "menu":

                    # Alternar entre RA e nome com setas
                    if evento.key == pygame.K_UP:
                        self.digitando_ra = True
                        self.digitando_nome = False

                    elif evento.key == pygame.K_DOWN:
                        if len(self.ra_aluno) >= 10:
                            self.digitando_ra = False
                            self.digitando_nome = True

                    # DIGITANDO RA
                    if self.digitando_ra:

                        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and len(self.ra_aluno) >= 10:
                            self.digitando_ra = False
                            self.digitando_nome = True

                        elif evento.key == pygame.K_BACKSPACE:
                            self.ra_aluno = self.ra_aluno[:-1]

                        else:
                            if evento.unicode.isdigit() and len(self.ra_aluno) < 10:
                                self.ra_aluno += evento.unicode

                    # DIGITANDO NOME
                    elif self.digitando_nome:

                        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and len(self.nome_aluno) > 0:
                            self.digitando_nome = False

                        elif evento.key == pygame.K_BACKSPACE:
                            if len(self.nome_aluno) == 0:
                                self.digitando_nome = False
                                self.digitando_ra = True
                            else:
                                self.nome_aluno = self.nome_aluno[:-1]

                        else:
                            caractere = evento.unicode

                            if len(self.nome_aluno) < 45:
                                                               
                                if caractere.isalpha():
                                    self.nome_aluno += caractere.upper()

                                elif caractere == " " and len(self.nome_aluno) > 0 and not self.nome_aluno.endswith(" "):
                                    self.nome_aluno += " "

                    # PRONTO PARA COMEÇAR
                    else:
                        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            self.iniciar_nivel()

                    
                # Jogando
                elif (
                    self.estado == "jogando" 
                    and self.nivel is not None
                    and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
                    ):
                    if len(self.nivel.letras_coletadas) == len(self.nivel.palavra_alvo):
                        self.tela_formacao = TelaFormacao(
                            self.nivel.letras_coletadas,
                            self.nivel.palavra_alvo
                        )
                        self.estado = "formando"
                        
                # Formando palavra
                elif self.estado == "formando" and self.tela_formacao is not None and self.nivel is not None:
                    if evento.key == pygame.K_BACKSPACE:
                        self.tela_formacao.remover_ultima()

                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):

                        # Se já acertou → próximo nível
                        if self.tela_formacao.correto:
                            self.nivel.acertos += 1
                            self.proximo_nivel()

                        # Se ainda não acertou → verificar
                        elif len(self.tela_formacao.palavra_formada) > 0:

                            acertou = self.tela_formacao.verificar()

                            # Se errou → aplicar penalidade
                            if not acertou:
                                self.nivel.erros += 1

                                penalidade = self.tela_formacao.tentativas * 5
                                self.nivel.pontuacao -= penalidade

                                if self.nivel.pontuacao < 0:
                                    self.nivel.pontuacao = 0

                # Fim
                elif self.estado == "fim" and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):

                    # Reset progresso
                    self.nivel_atual = 0
                    self.dificuldade_atual = 0
                    self.pontuacao_total = 0
                    self.acertos_totais = 0
                    self.erros_totais = 0
                    self.tempo_inicio = pygame.time.get_ticks()
                    self.tempo_total = 0

                    # Reset aluno
                    self.ra_aluno = ""
                    self.nome_aluno = ""

                    # Reset controle de digitação
                    self.digitando_ra = True
                    self.digitando_nome = False

                    # Limpa objetos
                    self.nivel = None
                    self.tela_formacao = None

                    # Volta para menu
                    self.estado = "menu"
            
            # Clique nas letras (formando palavra)
            if (
                self.estado == "formando"
                and self.tela_formacao is not None
                and evento.type == pygame.MOUSEBUTTONDOWN
            ):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                rects = self.tela_formacao.get_rect_letras_disponiveis()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        letra = self.tela_formacao.letras_disponiveis[i]
                        self.tela_formacao.adicionar_letra(letra)
                        break
                        
        return True
        
    def atualizar(self):
        """Atualiza a lógica do jogo"""
        if self.estado == "jogando" and self.nivel is not None:
            self.nivel.update()
            
    def desenhar(self):
        """Desenha todos os elementos na tela"""
        if self.estado == "menu":

            self.tela.fill((30, 30, 60))

            titulo = self.fonte_titulo.render("AVENTURA DAS LETRAS", True, (255, 255, 0))
            self.tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 80))

            cor_ra = (0, 255, 0) if self.digitando_ra else (180, 180, 180)
            cor_nome = (0, 255, 0) if self.digitando_nome else (180, 180, 180)

            # RA
            texto_ra = self.fonte_media.render("Digite seu RA:", True, (255, 255, 255))
            self.tela.blit(texto_ra, (LARGURA // 2 - texto_ra.get_width() // 2, 200))

            ra_render = self.fonte_grande.render(
                self.ra_aluno + ("|" if self.digitando_ra else ""),
                True,
                cor_ra
            )
            self.tela.blit(ra_render, (LARGURA // 2 - ra_render.get_width() // 2, 250))

            # Nome
            texto_nome = self.fonte_media.render("Digite seu nome:", True, (255, 255, 255))
            self.tela.blit(texto_nome, (LARGURA // 2 - texto_nome.get_width() // 2, 350))

            nome_render = self.fonte_grande.render(
                self.nome_aluno + ("|" if self.digitando_nome else ""),
                True,
                cor_nome
            )
            self.tela.blit(nome_render, (LARGURA // 2 - nome_render.get_width() // 2, 400))

            # Se terminou ambos
            if not self.digitando_ra and not self.digitando_nome:

                iniciar = self.fonte_media.render(
                    "Pressione ENTER para começar",
                    True,
                    (255, 255, 0)
                )
                self.tela.blit(iniciar, (LARGURA // 2 - iniciar.get_width() // 2, 500))

            
        elif self.estado == "jogando" and self.nivel is not None:
            self.nivel.desenhar(
                self.tela,
                self.fonte_pequena,
                self.fonte_media,
                self.fonte_grande,
                self.pontuacao_total
            )

            
        elif (
            self.estado == "formando"
            and self.tela_formacao is not None
            and self.nivel is not None
        ):
            self.tela_formacao.desenhar(
                self.tela,
                self.fonte_titulo,
                self.fonte_grande,
                self.fonte_media,
                self.fonte_pequena,
                self.pontuacao_total,
                self.nivel.pontuacao
            )

            
        elif self.estado == "fim":
            TelaFim.desenhar(
                self.tela, 
                self.fonte_titulo, 
                self.fonte_grande, 
                self.fonte_media, 
                self.fonte_pequena,
                self.nome_aluno,
                self.pontuacao_total,
                self.acertos_totais,
                self.erros_totais,
                self.tempo_total,
                len(self.palavras)
            )
            
        pygame.display.flip()

    
        
    def executar(self):
        """Loop principal do jogo"""
        rodando = True
        
        while rodando:
            self.clock.tick(FPS)
            
            rodando = self.processar_eventos()
            self.atualizar()
            self.desenhar()
            
        pygame.quit()
        sys.exit()


# Executar o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
