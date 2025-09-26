import pygame
import sys
import os
import random

'''
Desenvolvido por:
Julia Colle
Bruno Lisboa Lima - B

'''


# --- CONFIGURAÇÕES BÁSICAS ---
pygame.init()



# Criar retangulos (func auxiliar) - b
def criar_rect_por_pontos(x1, y1, x2, y2):
    largura = x2 - x1
    altura = y2 - y1
    return pygame.Rect(x1, y1, largura, altura)


# Dimensões da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LGPD: Detetives de Dados")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

# Fontes
font = pygame.font.Font(None, 36) # Fonte padrão, tamanho 36
small_font = pygame.font.Font(None, 24)

# Define componentes
SUSPEITOS = {
    "Analista de TI descuidado": "carta_analista.png",
    "Funcionario do RH": "carta_rh.png",
    "Gerente de Marketing": "carta_gmarketing.png",
    "Estagiario curioso": "carta_estagiario.png",
    "Diretor da Empresa": "carta_diretor.png",
    "Fornecedor Externo": "carta_fornecedor.png",
    "Atendente de Call Center": "carta_callcenter.png",
    "Hacker Infiltrado": "carta_hacker.png",
}

METODOS = {
    "Pendrive": "carta_pendrive.png",
    "E-mail": "carta_email.png",
    "Documentos impressos": "carta_documentos.png",
    "Telefone": "carta_telefone.png",
    "Dados na nuvem": "carta_nuvem.png",
    "Senhas": "carta_senha.png",
    "Software": "carta_software.png",
    "Cameras de seguranca": "carta_camera.png",
}

LOCAIS = {
    "RH": "sala_rh.png",
    "TI": "sala_ti.png",
    "Marketing": "sala_marketing.png",
    "Call Center": "sala_callcenter.png",
    "Financeiro": "sala_financeiro.png",
    "Juridico": "sala_juridico.png",
    "Diretoria": "sala_diretoria.png",
    "Data Center": "sala_data.png",
    "Servidor em Nuvem": "sala_servidor.png",
    "Reuniao Online": "sala_reuniao.png",
    "Estacionamento": "sala_estacionamento.png",
}

PLAYERS_IMAGES = {
    1: "player1.png",
    2: "player2.png",
    3: "player3.png",
    4: "player4.png",
    5: "player5.png",
    6: "player6.png",
}

# --- CARREGAR E ARMAZENAR IMAGENS ---
script_dir = os.path.dirname(os.path.abspath(__file__)) # puxa o local do script -b
# Corrigido pra puxar independente do disco e local do arquivo- B


images = {}
def load_image(filepath, scale=None):
    #carrega a imagem e escala
    full_path = os.path.join(script_dir, filepath)  # Garante que o caminho é absoluto
    try:
        image = pygame.image.load(full_path).convert_alpha() # convert_alpha para imagens com transparência
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Erro ao carregar imagem {filepath}: {e}")
        print(f"O programa procurou a imagem em: {full_path}") # facilita a depuração de qual é o erro - B
        print("VERIFIQUE se o nome do arquivo está correto e se ele está na MESMA PASTA do script.")
        pygame.quit()
        sys.exit()

# Carregar imagens específicas
images['tabuleiro'] = load_image("meu_tabuleiro_final.png", (900, 700))
images['verso_carta'] = load_image("verso.png", (70, 100))
images['btn_acusar'] = load_image("acusar.png", (150, 50))
images['btn_investigar'] = load_image("investigar.png", (150, 50))
images['btn_ver_pistas'] = load_image("ver_pistas.png", (150, 50)) 
images['btn_fechar'] = load_image("fechar.png", (40, 40)) 
# Carregar imagens de suspeitos
images['suspeitos'] = {name: load_image(filepath, (70, 100)) for name, filepath in SUSPEITOS.items()}
# Carregar imagens de métodos
images['metodos'] = {name: load_image(filepath, (70, 100)) for name, filepath in METODOS.items()}
# Carregar imagens de locais (usadas como cartas)
images['locais'] = {name: load_image(filepath, (70, 100)) for name, filepath in LOCAIS.items()}
# Carregar imagens dos peões dos jogadores
images['players_pawns'] = {num: load_image(filepath, (40, 40)) for num, filepath in PLAYERS_IMAGES.items()}

# --- CLASSES DO JOGO (Simplificadas para o visual) ---
class Player:
    def __init__(self, name, player_id, pawn_image, start_position):
        self.name = name
        self.id = player_id
        self.pawn_image = pawn_image
        self.position = start_position
        self.location = start_position
        self.hand = []

    def draw(self, screen):
        screen.blit(self.pawn_image, self.pixel_pos)
        text_surface = small_font.render(self.name, True, BLACK)
        screen.blit(text_surface, (self.pixel_pos[0], self.pixel_pos[1] - 20))


class Game:
    def __init__(self, player_names):
        
         # simplifiquei, todas aquelas conexões só funcionariam se o mapa fosse muito maior, se tiver algo errado, acessa o .png do mapa pelo paint e pega os pixel x e y de lá. - b
        self.casas_pixel_coords = {
            "SALA_TI": (130, 125),
            "JURIDICO": (367, 156), 
            "ESTACIONAMENTO": (502, 141), 
            "MARKETING": (790, 166), 
            "RH": (146, 389), 
            "DATA_CENTER": (787, 375), 
            "DIRETORIA": (285, 372), 
            "FINANCEIRO": (453, 609), 
            "SERV_NUVEM": (560, 350), 
            "CALL_CENTER": (238, 567), 
            "REUNIAO_ONLINE": (631,610),
            "PONTO_DE_PARTIDA": (292, 369),
        }
        self.mapa_do_tabuleiro = {
            "SALA_TI": ["JURIDICO", "RH"],
            "JURIDICO": ["SALA_TI", "ESTACIONAMENTO", "DIRETORIA"],
            "ESTACIONAMENTO": ["JURIDICO", "MARKETING","SERV_NUVEM"],
            "RH": ["SALA_TI", "DIRETORIA", "CALL_CENTER"],
            "DATA_CENTER": ["MARKETING", "SERV_NUVEM"],
            "MARKETING": ["ESTACIONAMENTO", "DATA_CENTER"],
            "DIRETORIA": ["RH", "FINANCEIRO","REUNIAO_ONLINE","CALL_CENTER","JURIDICO","SERV_NUVEM"],
            "FINANCEIRO": ["DIRETORIA", "DATA_CENTER", "SERV_NUVEM"],
            "SERV_NUVEM": ["FINANCEIRO", "DATA_CENTER","DIRETORIA","ESTACIONAMENTO"],
            "CALL_CENTER": ["RH", "FINANCEIRO","DIRETORIA"],
            "REUNIAO_ONLINE": ["DIRETORIA"], #só pode ser acessado através da sala de reunião ou com um resultado acima de 7 no dado -b
            "PONTO_DE_PARTIDA": list(LOCAIS.keys())
            #terminado o vinculo finalmente - b
        }

        # puxa x1,y1, x2,y2 desse site aqui https://www.image-map.net/
        self.salas_rects = {
           "SALA_TI":    criar_rect_por_pontos(36,16, 214, 213),
           "JURIDICO":   criar_rect_por_pontos(256, 10, 434,207),
           "ESTACIONAMENTO": criar_rect_por_pontos(475,16,653,211),
           "MARKETING":  criar_rect_por_pontos(692, 11, 870, 208),
           "RH": criar_rect_por_pontos(39, 247, 217, 444),
           "DATA_CENTER": criar_rect_por_pontos(694, 250, 872, 447),
           "DIRETORIA": criar_rect_por_pontos(260, 249, 438, 446),
           "FINANCEIRO": criar_rect_por_pontos(365, 484, 543, 681),
           "SERV_NUVEM": criar_rect_por_pontos(475, 251, 653, 448),
           "CALL_CENTER": criar_rect_por_pontos(151, 484, 329, 681),
           "REUNIAO_ONLINE": criar_rect_por_pontos(584, 484, 762, 681),
           "PONTO_DE_PARTIDA": criar_rect_por_pontos(292, 369, 292+10, 369+10)  # um quadrado pequeno, só pra ter rect (estava disparando erro de atributo antes) - B

        }
        self.pistas_por_local = {
            "RH": "SUSPEITOS", "DIRETORIA": "SUSPEITOS", "CALL_CENTER": "SUSPEITOS",
            "SALA_TI": "METODOS", "DATA_CENTER": "METODOS", "SERV_NUVEM": "METODOS",
            "JURIDICO": "LOCAIS", "FINANCEIRO": "LOCAIS", "MARKETING": "LOCAIS",
            "ESTACIONAMENTO": "LOCAIS", "REUNIAO_ONLINE": "LOCAIS"
        }

        
        # lista com todas as casas de início disponíveis no mapa -b 
        start_positions = list(self.casas_pixel_coords.keys())
        start_positions.remove("PONTO_DE_PARTIDA")
        random.shuffle(start_positions)
        
        # cria a lista de jogadores, dando a cada um uma posição única - b
        self.players = []
        for i, name in enumerate(player_names):
            posicao_inicial = start_positions[i % len(start_positions)]
            player = Player(name, i + 1, images['players_pawns'][i+1], posicao_inicial)
            self.players.append(player)
            print(f"Jogador {name} criado na posição inicial {posicao_inicial}") #mudei a lógica de mapa então pode estar bugado - b

    
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.game_state = "AWAITING_ROLL"

        self.solution = {}
        self.deal_cards()        
        images['btn_mover'] = load_image("mover.png", (150, 50))
        self.valid_moves = []
        self.dice_roll = 0
        self.game_state = "AWAITING_ROLL"
        self.horas_restantes = 48 # jogadores vão ter 48h pra acabar o jogo - B (só 24 estava acabando mt rápido e não tinha mt como investigar)
        self.pistas_descobertas = [] 
        self.mensagem_de_pista = "" 
        self.clue_display_timer = 0
        self.accusation_rects = {}  
        self.current_accusation = {}
        self.bloco_de_anotacoes = {}
        self.inicializar_bloco_de_anotacoes()
        self.showing_notebook = False # eu nao aguento mais adicionar conteudo, vou ver se esse é o ultimo antes de ir pra correção de bug - foi o ultimo - B

    def investigate(self):
        player_location = self.current_player.position
        print(f"{self.current_player.name} está investigando em {player_location}.")

        # custa 2 horas para investigar - b
        self.horas_restantes -= 2
        print(f"Tempo restante: {self.horas_restantes} horas")
        
        # Descobrir qual TIPO de pista dar com base no local -b
        tipo_de_pista = self.pistas_por_local.get(player_location)
        if not tipo_de_pista:
            print("Este local não oferece pistas.")
            # (devolve o tempo se a ação foi inválida) -b
            self.horas_restantes += 2
            return

        # montar a lista de cartas "inocentáveis" - b
        lista_de_cartas = []
        if tipo_de_pista == "SUSPEITOS":
            lista_de_cartas = list(SUSPEITOS.keys())
        elif tipo_de_pista == "METODOS":
            lista_de_cartas = list(METODOS.keys())
        elif tipo_de_pista == "LOCAIS":
            lista_de_cartas = list(LOCAIS.keys())

        # remove a carta que está na solução e as que já foram descobertas
        mapping = {"SUSPEITOS": "suspeito", "METODOS": "metodo", "LOCAIS": "local"}
        carta_solucao = self.solution.get(mapping.get(tipo_de_pista))
        cartas_possiveis = [carta for carta in lista_de_cartas if carta != carta_solucao]

        cartas_reveladas = []
        for jogador in self.players:
            if jogador == self.current_player:
                continue
            for carta in jogador.hand:
                if carta in cartas_possiveis and carta not in self.pistas_descobertas:
                    cartas_reveladas.append(carta)

        if cartas_reveladas:
            pista_revelada = random.choice(cartas_reveladas)
            self.bloco_de_anotacoes[pista_revelada] = "Inocentado"
            self.pistas_descobertas.append(pista_revelada)
            self.mensagem_de_pista = f"Investigação inocentou: {pista_revelada}"
            print(self.mensagem_de_pista)
        else:
            self.mensagem_de_pista = "Nenhuma nova pista encontrada neste local."
            print(self.mensagem_de_pista)

        self.game_state = "SHOWING_CLUE"
        self.clue_display_timer = pygame.time.get_ticks() # 5 segundos pra mostrar a pista

    def roll_dice(self):
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        self.dice_roll = dado1 + dado2
        print(f"{self.current_player.name} tirou {self.dice_roll}")

        current_pos = self.current_player.position

        if self.dice_roll <= 7:
            # movimento curto: apenas salas vizinhas - b
            self.valid_moves = self.mapa_do_tabuleiro.get(current_pos, [])
        else:
            # movimento longo: para qualquer sala - b
            self.valid_moves = list(self.casas_pixel_coords.keys())
            # tira a própria sala das opções
            if current_pos in self.valid_moves:
                self.valid_moves.remove(current_pos)
    
        # permite múltiplos jogadores no ponto de partida - b
        posicoes_ocupadas = {p.position for p in self.players if p != self.current_player and p.position != "PONTO_DE_PARTIDA"}
        self.valid_moves = [move for move in self.valid_moves if move not in posicoes_ocupadas]

        print(f"Pode mover para: {self.valid_moves}")
        self.game_state = "PLAYER_MOVING"

    def deal_cards(self):
        print("Criando o envelope secreto e distribuindo as cartas...")
        todos_suspeitos = list(SUSPEITOS.keys())
        todos_metodos = list(METODOS.keys())
        todos_locais = list(LOCAIS.keys())
        solucao_suspeito = random.choice(todos_suspeitos)
        solucao_metodo = random.choice(todos_metodos)
        solucao_local = random.choice(todos_locais)
        self.solution = {"suspeito": solucao_suspeito, "metodo": solucao_metodo, "local": solucao_local}
        print(f"SOLUÇÃO SECRETA (para teste): {self.solution}") # DEBUG, REMOVER/COMENTAR ANTES DA ENTREGA FINAL - B
        baralho_para_distribuir = todos_suspeitos + todos_metodos + todos_locais
        baralho_para_distribuir.remove(solucao_suspeito)
        baralho_para_distribuir.remove(solucao_metodo)
        baralho_para_distribuir.remove(solucao_local)
        random.shuffle(baralho_para_distribuir)
        player_idx = 0
        while baralho_para_distribuir:
            carta = baralho_para_distribuir.pop(0)
            self.players[player_idx].hand.append(carta)
            player_idx = (player_idx + 1) % len(self.players)

    
    def draw_game_elements(self):
        screen.blit(images['tabuleiro'], (0, 0))
        for player in self.players:
            #agora usa o mapa lógico ali em cima - B
            pixel_pos = self.casas_pixel_coords.get(player.position)
            if pixel_pos:
                screen.blit(player.pawn_image, pixel_pos)
                text_surface = small_font.render(player.name, True, BLACK)
                screen.blit(text_surface, (pixel_pos[0], pixel_pos[1] - 20))

        # Ta corrigido, eu tinha deixado o if fora do for - B
        if self.game_state == "PLAYER_MOVING":
            # O loop agora processa e desenha CADA movimento válido - B
            for sala_nome in self.valid_moves:
                rect = self.salas_rects.get(sala_nome)
                # corrigido de vdd agora
                if rect:
                    s = pygame.Surface(rect.size, pygame.SRCALPHA)
                    s.fill((0, 255, 0, 128)) 
                    screen.blit(s, rect.topleft)   

        # --- Desenha a mão do jogador  - pequenas correções e sistema de cortar em 4 antes de ir pra próxima
        text_surface = font.render(f"Mao de {self.current_player.name}:", True, BLACK)
        screen.blit(text_surface, (930, 20))
        start_x, start_y, margin, cards_per_row = 930, 50, 10, 4
        x_offset, y_offset = start_x, start_y
        card_width, card_height = 70, 100
        for i, card_name in enumerate(self.current_player.hand):
            card_image = images.get('suspeitos', {}).get(card_name) or images.get('metodos', {}).get(card_name) or images.get('locais', {}).get(card_name) or images['verso_carta']
            if i > 0 and i % cards_per_row == 0:
                x_offset = start_x
                y_offset += card_height + margin
            screen.blit(card_image, (x_offset, y_offset))
            x_offset += card_width + margin

        # --- Desenhar UI (botões, textos, etc.) ---
        screen.blit(images['btn_ver_pistas'], ((SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50)))

        if self.game_state == "AWAITING_ROLL":
            screen.blit(images['btn_mover'], (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 100))
            if self.current_player.position != "PONTO_DE_PARTIDA":
                screen.blit(images['btn_investigar'], (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 50))
    
        screen.blit(images['btn_acusar'], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        turn_text = font.render(f"Vez de: {self.current_player.name}", True, BLACK)
        screen.blit(turn_text, (930, SCREEN_HEIGHT - 150 ))
        
        timer_text_str = f"Tempo Restante: {self.horas_restantes} horas"
        timer_color = BLACK if self.horas_restantes > 6 else (255, 0, 0)
        timer_text = font.render(timer_text_str, True, timer_color)
        screen.blit(timer_text, (930, SCREEN_HEIGHT - 200))

        #interface de acusação final - B
        if self.game_state == "AWAITING_ACCUSATION":
            
            # Fundo Cinza - B
            pygame.draw.rect(screen, GRAY, (40, 50, 850, 600))
            title_text = font.render("ACUSAÇÃO FINAL", True, WHITE)
            screen.blit(title_text, (60, 70))
        
            # Instrução - B
            instruction_text = "Selecione o Suspeito, o Método e o Local"
            if "suspeito" in self.current_accusation:
                instruction_text = "Agora selecione o Método e o Local"
            if "metodo" in self.current_accusation:
                instruction_text = "Agora selecione o Local"
        
            instr_surf = small_font.render(instruction_text, True, WHITE)
            screen.blit(instr_surf, (60, 100))
        
            # Lógica para desenhar as cartas de seleção em COLUNAS - B (Similar ao corte em 4 porém corta em 3)
            categorias = {"SUSPEITOS": SUSPEITOS, "METODOS": METODOS, "LOCAIS": LOCAIS}
            start_x_coluna = 60 # Posição X da primeira coluna

            for categoria, itens in categorias.items():
                cat_key = categoria.lower()[:-1] # 'suspeito', 'metodo', 'local'
                
                # Só desenha a categoria se ela ainda não foi selecionada
                if cat_key not in self.current_accusation:
                    cat_text = small_font.render(f"Selecione um(a) {cat_key.capitalize()}:", True, WHITE)
                    screen.blit(cat_text, (start_x_coluna, 120))

                    x_offset = start_x_coluna
                    y_offset = 150
                    for i, name in enumerate(itens.keys()):
                        image = images.get(categoria.lower(), {}).get(name)
                        if image:
                            # Calcula posição em grade: 3 por linha
                            col = i % 3          # 0,1,2 → coluna
                            row = i // 3         # sobe 1 a cada 3 cartas
                            x_offset = start_x_coluna + col * 90   # espaçamento horizontal
                            y_offset = 150 + row * 120             # espaçamento vertical

                            screen.blit(image, (x_offset, y_offset))
                            self.accusation_rects[name] = pygame.Rect(x_offset, y_offset, 70, 100)

                start_x_coluna += 280 # Move para a próxima coluna - B
                
                pygame.draw.rect(screen, BLACK, (300, 580, 280, 110))  

                # Posições fixas para cada carta escolhida - Evita dor de cabeça mais tarde - b
                slot_positions = [(310, 585), (390, 585), (470, 585)]  

                # Se já foi escolhido, mostra - B
                if "suspeito" in self.current_accusation:
                    img = images['suspeitos'].get(self.current_accusation["suspeito"])
                    if img: 
                        screen.blit(img, slot_positions[0])

                if "metodo" in self.current_accusation:
                    img = images['metodos'].get(self.current_accusation["metodo"])
                    if img: 
                        screen.blit(img, slot_positions[1])

                if "local" in self.current_accusation:
                    img = images['locais'].get(self.current_accusation["local"])
                    if img: 
                        screen.blit(img, slot_positions[2])

        # Atualizei a parte de derrota para mostrar a resposta - J
        if self.game_state == "GAME_OVER":
            # --- Fundo escuro ---
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            screen.blit(s, (0, 0))

            # --- Derrota ---
            game_over_text = font.render("O TEMPO ACABOU!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 120))
            screen.blit(game_over_text, text_rect)

            lose_text = small_font.render("A equipe não conseguiu resolver o caso a tempo.", True, WHITE)
            lose_rect = lose_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 80))
            screen.blit(lose_text, lose_rect)

            # --- Título para a solução ---
            solution_title_text = small_font.render("Solução do Caso:", True, (200, 200, 200))
            solution_title_rect = solution_title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30))
            screen.blit(solution_title_text, solution_title_rect)

            # --- Pega os nomes e as imagens das cartas da solução ---
            solucao_suspeito_nome = self.solution["suspeito"]
            solucao_metodo_nome = self.solution["metodo"]
            solucao_local_nome = self.solution["local"]

            solucao_suspeito_img = images['suspeitos'][solucao_suspeito_nome]
            solucao_metodo_img = images['metodos'][solucao_metodo_nome]
            solucao_local_img = images['locais'][solucao_local_nome]

            # --- Calcula as posições para centralizar as 3 cartas ---
            card_width = 70
            spacing = 20
            total_width = (card_width * 3) + (spacing * 2)
            start_x = (SCREEN_WIDTH - total_width) / 2
            card_y = SCREEN_HEIGHT / 2 # Posição vertical das cartas

            # --- Desenha as cartas da solução na tela ---
            screen.blit(solucao_suspeito_img, (start_x, card_y))
            screen.blit(solucao_metodo_img, (start_x + card_width + spacing, card_y))
            screen.blit(solucao_local_img, (start_x + 2 * (card_width + spacing), card_y))

        
        if self.game_state == "WIN":
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((255, 255, 100, 180)) # Fundo dourado de vitória
            screen.blit(s, (0, 0))
            win_text = font.render("PARABÉNS! CASO RESOLVIDO!", True, BLACK)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(win_text, text_rect)

        if self.game_state == 'SHOWING_CLUE':
            pygame.draw.rect(screen,BLACK,(SCREEN_WIDTH/2-300, SCREEN_HEIGHT/2 - 50,600,100))
            pygame.draw.rect(screen,WHITE,(SCREEN_WIDTH/2-298, SCREEN_HEIGHT/2 - 48,596,96),2)
            #Texto da pista - b
            clue_text = font.render(self.mensagem_de_pista, True, WHITE)
            text_rect = clue_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(clue_text, text_rect) 
            # vê se já se passou 5 segundos (5000 ms) - B
            if pygame.time.get_ticks() - self.clue_display_timer > 5000:
                # passa o turno - B
                self.game_state = "AWAITING_ROLL"
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                self.current_player = self.players[self.current_player_index]

        if self.showing_notebook:
            # Fundo semi-transparente para focar no bloco - b
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            screen.blit(s, (0, 0))

            # Fundo do bloco de anotações - B
            pygame.draw.rect(screen, LIGHT_GRAY, (300, 50, 680, 620))
            pygame.draw.rect(screen, BLACK, (300, 50, 680, 620), 3)

            # Botão de Fechar - B
            fechar_rect = images['btn_fechar'].get_rect(topright=(970, 60))
            screen.blit(images['btn_fechar'], fechar_rect)

            y_offset = 70
            x_coluna = 320
            for categoria, itens in {"SUSPEITOS": SUSPEITOS, "METODOS": METODOS, "LOCAIS": LOCAIS}.items():
                cat_text = font.render(categoria, True, BLACK)
                screen.blit(cat_text, (x_coluna, y_offset))
                y_offset += 30
            
                for item in itens:
                    estado = self.bloco_de_anotacoes.get(item)
                    cor = GRAY  # Possibilidade - B
                    if estado == "Na Mão":
                        cor = GRAY
                    elif estado == "Inocentado":
                        cor = (200, 0, 0)
                    elif estado == "Solução":
                        cor = (0, 150, 0) 
                    item_text = small_font.render(f"- {item}", True, cor)

                    # Desenhar linha para “Inocentado” ou “Na Mão” - B
                    if estado in ["Na Mão", "Inocentado"]:
                        start_pos = (x_coluna + 10, y_offset + item_text.get_height()//2)
                        end_pos = (x_coluna + 10 + item_text.get_width(), y_offset + item_text.get_height()//2)
                        pygame.draw.line(screen, cor, start_pos, end_pos)

                    screen.blit(item_text, (x_coluna + 10, y_offset))
                    y_offset += 20
                
                    # Quebra de coluna para não sair da tela
                    if y_offset > 650:
                        y_offset = 100
                        x_coluna += 220
            
                y_offset = 70
                x_coluna += 220

    def handle_click(self, pos): 
        # se perder ou ganhar n deixa fazer mais nada - B
        if self.game_state == "GAME_OVER" or self.game_state == "WIN":
            return

        # Essa verificação roda antes de tudo, já q o botão de pistas deve funcionar a qualquer momento. - b
        ver_pistas_rect = images['btn_ver_pistas'].get_rect(topleft=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50))
        if ver_pistas_rect.collidepoint(pos):
            self.showing_notebook = not self.showing_notebook # altera entre true e false
            return # a ação do turno foi abrir/fechar o bloco ent para aqui - b

        # se o bloco tá aberto tu só pode fechar - b
        if self.showing_notebook:
            fechar_rect = images['btn_fechar'].get_rect(topright=(970, 60))
            if fechar_rect.collidepoint(pos):
                self.showing_notebook = False
            return # trava todos os outros cliques se ele tiver aberto - b

        acusar_rect = images['btn_acusar'].get_rect(topleft=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        if acusar_rect.collidepoint(pos):
            print(f"A equipe decidiu fazer a acusação final!")
            self.game_state = "AWAITING_ACCUSATION" 
            self.current_accusation = {}
            self.accusation_rects = {}
            return

        # acusação - b
        if self.game_state == "AWAITING_ACCUSATION":
            for name, rect in self.accusation_rects.items():
                if rect.collidepoint(pos):
                    # descobre a categoria da carta clicada e a adiciona à acusação - b
                    if name in SUSPEITOS and "suspeito" not in self.current_accusation:
                        self.current_accusation["suspeito"] = name
                    elif name in METODOS and "metodo" not in self.current_accusation:
                        self.current_accusation["metodo"] = name
                    elif name in LOCAIS and "local" not in self.current_accusation:
                        self.current_accusation["local"] = name
                    
                    print(f"Seleção atual: {self.current_accusation}")
                    self.accusation_rects = {} # Limpa para redesenhar a UI - b
            
            if "suspeito" in self.current_accusation and "metodo" in self.current_accusation and "local" in self.current_accusation:
                self.check_final_accusation()
            
            return 
            
            #espera o movimento - b
        if self.game_state == "AWAITING_ROLL":
            mover_rect = images['btn_mover'].get_rect(topleft=(SCREEN_WIDTH - 350, SCREEN_HEIGHT - 100))
            investigar_rect = images['btn_investigar'].get_rect(topleft=(SCREEN_WIDTH - 350, SCREEN_HEIGHT - 50))
            
            if mover_rect.collidepoint(pos):
                self.roll_dice()
            # O elif garante que o jogador só pode fazer uma ação por clique. - b
            elif self.current_player.position != "PONTO_DE_PARTIDA" and investigar_rect.collidepoint(pos):
                self.investigate()
            return # termina o processamento do clique aqui neste turno -b 

        # --- Movimentação do jogador 
        if self.game_state == "PLAYER_MOVING":
            for sala_nome in self.valid_moves:
                rect = self.salas_rects.get(sala_nome)
                if rect and rect.collidepoint(pos):
                    self.current_player.position = sala_nome
                    self.current_player.location = sala_nome
                    print(f"{self.current_player.name} moveu para {sala_nome}")
                    
                    self.horas_restantes -= 1 # depois do movimento diminui em 1 as horas restantes
                    print(f"Tempo restante: {self.horas_restantes} horas")
                    
                    # valida se tem tempo sobrando - b 
                    if self.horas_restantes <= 0:
                        print("O tempo acabou! A equipe perdeu.")
                        self.game_state = "GAME_OVER"
                        return # encerra o turno

                    # Prepara para o próximo turno - b
                    self.valid_moves = []
                    self.game_state = "AWAITING_ROLL" 
                    self.current_player_index = (self.current_player_index + 1) % len(self.players)
                    self.current_player = self.players[self.current_player_index]
                    return # se deu td certo ele devolve a ação - B
                
    def check_final_accusation(self):
        print("Verificando acusação...")
        # Compara a acusação com a solução - b
        if self.current_accusation == self.solution:
            print("ACUSAÇÃO CORRETA! A EQUIPE VENCEU!")
            self.game_state = "WIN" # estado de vitória
        else:
            print("ACUSAÇÃO INCORRETA! Penalidade de tempo aplicada.")
            self.horas_restantes -= 6 # Penalidade de 6 horas
            if self.horas_restantes <= 0:
                self.game_state = "GAME_OVER"
            else:
                # volta pro jogo
                self.game_state = "AWAITING_ROLL"   

    # Novo método na classe Game
    def inicializar_bloco_de_anotacoes(self):
        # Começa com todas as cartas como "Possibilidade" (Evita bug de ele revelar qual é a resposta, passei umas 2 horas só nisso pq n sabia oq causava) - B
        for suspeito in SUSPEITOS: self.bloco_de_anotacoes[suspeito] = "Possibilidade"
        for metodo in METODOS: self.bloco_de_anotacoes[metodo] = "Possibilidade"
        for local in LOCAIS: self.bloco_de_anotacoes[local] = "Possibilidade"

        # Marca as cartas que os jogadores têm na mão como "Na Mão" (não podem ser solução) - B
        for player in self.players:
            for card in player.hand:
                self.bloco_de_anotacoes[card] = "Na Mão"
        for key, carta in self.solution.items():
            # Só se ainda não estiver marcada como "Na Mão" - B
            if self.bloco_de_anotacoes.get(carta) != "Na Mão":
                self.bloco_de_anotacoes[carta] = "Possibilidade"
# --- FUNÇÃO PRINCIPAL DO JOGO ---
def main():
    num_players = 0
    while num_players < 2 or num_players > 6:
        try:
            num_players = int(input("Digite o número de jogadores (2-6): "))
        except ValueError:
            print("Por favor, digite um número válido.")
            
    player_names = []
    for i in range(num_players):
        name = input(f"Digite o nome do Jogador {i+1}: ")
        player_names.append(name)

    game = Game(player_names)

    running = True
    while running:
        # --- 1. PROCESSAMENTO DE EVENTOS  ---
        # Este é o bloco que impede o jogo de travar.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_click(event.pos)
        
        # --- 2. ATUALIZAÇÃO DA LÓGICA DO JOGO ---
        # (Nesta seção ficaria a lógica mais complexa no futuro)

        # --- 3. DESENHO NA TELA ---
        screen.fill(LIGHT_GRAY)
        game.draw_game_elements()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

# --- INICIA O JOGO ---
if __name__ == "__main__":
    main()