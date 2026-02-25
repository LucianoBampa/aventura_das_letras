import os
from datetime import datetime


class RelatorioAluno:

    @staticmethod
    def gerar(ra_aluno, nome_aluno, palavras, acertos_totais, erros_totais, pontuacao_total, tempo_total):

        minutos = tempo_total // 60
        segundos = tempo_total % 60

        tempo_formatado = f"{minutos:02d}:{segundos:02d}"

        total_tentativas = acertos_totais + erros_totais

        if total_tentativas > 0:
            aproveitamento = int((acertos_totais / total_tentativas) * 100)
        else:
            aproveitamento = 0

        data = datetime.now().strftime("%d/%m/%Y %H:%M")

        texto = f"""
=====================================
        RELATÓRIO DE DESEMPENHO
=====================================

Aluno: {nome_aluno}
RA: {ra_aluno}
Data: {data}

Palavras trabalhadas: {len(palavras)}
Acertos: {acertos_totais}
Erros: {erros_totais}
Aproveitamento: {aproveitamento}%
Tempo de Jogo: {tempo_formatado}
Pontuação final: {pontuacao_total} pontos

=====================================
"""

        # cria pasta relatorios se não existir
        if not os.path.exists("relatorios"):
            os.makedirs("relatorios")

        nome_arquivo = f"relatorios/{nome_aluno}_{ra_aluno}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

        return texto
