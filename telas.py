"""
Telas de Menu e Fim de Jogo
"""
import pygame
import random
import math
from config import (AZUL_ESCURO, BRANCO, COR_LETRA,
                    COR_LETRA_BORDA, PRETO,
                    VERDE_SUCESSO, ROXO, 
                    LARGURA, ALTURA)


class TelaMenu:
    """Tela de menu inicial"""
    
    @staticmethod
    def desenhar(tela, fonte_titulo, fonte_media, fonte_pequena):
        """Desenha o menu inicial"""
        # Fundo degradê
        for y in range(ALTURA):
            cor_r = 135
            cor_g = 206 - int(y * 0.2)
            cor_b = 250
            pygame.draw.line(tela, (cor_r, cor_g, cor_b), (0, y), (LARGURA, y))
        
        # Título com sombra
        texto_sombra = fonte_titulo.render("AVENTURA DAS LETRAS", True, AZUL_ESCURO)
        rect_sombra = texto_sombra.get_rect(center=(LARGURA // 2 + 4, 124))
        tela.blit(texto_sombra, rect_sombra)
        
        texto_titulo = fonte_titulo.render("AVENTURA DAS LETRAS", True, COR_LETRA)
        rect_titulo = texto_titulo.get_rect(center=(LARGURA // 2, 120))
        tela.blit(texto_titulo, rect_titulo)
        
        # Instruções
        instrucoes = [
            "Use as setas DIREITA e ESQUERDA para mover",
            "Pressione ESPAÇO para pular",
            "Colete todas as letras",
            "Forme a palavra correta!",
        ]
        
        y = 250
        for linha in instrucoes:
            texto = fonte_pequena.render(linha, True, AZUL_ESCURO)
            rect = texto.get_rect(center=(LARGURA // 2, y))
            tela.blit(texto, rect)
            y += 50
        
        # Botão começar (piscando)
        if pygame.time.get_ticks() % 1000 < 500:
            texto_comecar = fonte_media.render("Pressione ENTER para INICIAR", True, VERDE_SUCESSO)
            rect_comecar = texto_comecar.get_rect(center=(LARGURA // 2, 480))
            
            # Fundo do botão
            fundo_botao = pygame.Rect(rect_comecar.x - 20, rect_comecar.y - 10, 
                                     rect_comecar.width + 40, rect_comecar.height + 20)
            pygame.draw.rect(tela, BRANCO, fundo_botao, border_radius=10)
            pygame.draw.rect(tela, VERDE_SUCESSO, fundo_botao, 3, border_radius=10)
            
            tela.blit(texto_comecar, rect_comecar)


class TelaFim:
    """Tela de fim de jogo"""

    serpentinas = []

    @staticmethod
    def iniciar_serpentinas():
        TelaFim.serpentinas = []

        cores = [
            (255, 0, 0),
            (0, 200, 0),
            (0, 150, 255),
            (255, 200, 0),
            (180, 0, 255)
        ]

        for _ in range(40):
            TelaFim.serpentinas.append({
                "x": random.randint(0, LARGURA),
                "y": random.randint(-ALTURA, 0),
                "vel": random.randint(2, 5),
                "cor": random.choice(cores),
                "tam": random.randint(12, 20)
            })

    @staticmethod
    def desenhar(tela, fonte_titulo, fonte_grande, fonte_media, fonte_pequena,
                 pontuacao_total, acertos_totais, erros_totais):
        """Desenha a tela de fim de jogo"""
        tela.fill(VERDE_SUCESSO)

        # Serpentinas caindo
        for s in TelaFim.serpentinas:
            pygame.draw.line(
                tela,
                s["cor"],
                (s["x"], s["y"]),
                (s["x"], s["y"] + s["tam"]),
                3
            )

            s["y"] += s["vel"]

            if s["y"] > ALTURA:
                s["y"] = random.randint(-50, -10)
                s["x"] = random.randint(0, LARGURA)

        centro_x = LARGURA // 2
        pos_y = 150

        # Título
        texto_sombra = fonte_titulo.render("PARABÉNS!", True, (0, 100, 0))
        tela.blit(texto_sombra, texto_sombra.get_rect(center=(centro_x + 4, pos_y + 4)))

        texto_parabens = fonte_titulo.render("PARABÉNS!", True, BRANCO)
        tela.blit(texto_parabens, texto_parabens.get_rect(center=(centro_x, pos_y)))

        # Pontuação Total
        pos_y += 90
        texto_pontos = fonte_grande.render(
            f"Pontuação Total: {pontuacao_total}", True, BRANCO)
        tela.blit(texto_pontos, texto_pontos.get_rect(center=(centro_x, pos_y)))

        # Mensagem
        pos_y += 70
        texto_fim = fonte_media.render(
            "Você completou todos os níveis!", True, BRANCO)
        tela.blit(texto_fim, texto_fim.get_rect(center=(centro_x, pos_y)))

        # Acertos
        pos_y += 70
        texto_acertos = fonte_media.render(
            f"Acertos: {acertos_totais}", True, (0, 255, 0))
        tela.blit(texto_acertos, texto_acertos.get_rect(center=(centro_x, pos_y)))

        # Erros
        pos_y += 50
        texto_erros = fonte_media.render(
            f"Erros: {erros_totais}", True, (255, 100, 100))
        tela.blit(texto_erros, texto_erros.get_rect(center=(centro_x, pos_y)))

        # Aproveitamento
        total = acertos_totais + erros_totais
        percentual = int((acertos_totais / total) * 100) if total > 0 else 0

        pos_y += 50
        texto_percentual = fonte_media.render(
            f"Aproveitamento: {percentual}%", True, (0, 255, 255))
        tela.blit(texto_percentual, texto_percentual.get_rect(center=(centro_x, pos_y)))


        # # Medalha
        # cx, cy = LARGURA // 2, 430

        # pygame.draw.rect(tela, ROXO, (cx - 30, cy - 130, 60, 70), border_radius=12)
        # pygame.draw.circle(tela, COR_LETRA, (cx, cy), 65)
        # pygame.draw.circle(tela, COR_LETRA_BORDA, (cx, cy), 65, 5)
        # pygame.draw.circle(tela, (255, 235, 150), (cx, cy), 45)

        # estrela = [
        #     (cx, cy - 28), (cx + 8, cy - 8), (cx + 28, cy - 8),
        #     (cx + 12, cy + 6), (cx + 18, cy + 26),
        #     (cx, cy + 14),
        #     (cx - 18, cy + 26), (cx - 12, cy + 6),
        #     (cx - 28, cy - 8), (cx - 8, cy - 8)
        # ]

        # pygame.draw.polygon(tela, PRETO, [(x+3, y+3) for x, y in estrela])
        # pygame.draw.polygon(tela, AZUL_ESCURO, estrela)

        # Reiniciar
        texto_r = fonte_media.render("Pressione R para jogar novamente", True, BRANCO)
        tela.blit(texto_r, texto_r.get_rect(center=(LARGURA//2, 540)))

      
        

