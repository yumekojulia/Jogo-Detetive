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



# --- Função para os retângulos de carta ---
def criar_rect_por_pontos(x1, y1, x2, y2):
    largura = x2 - x1
    altura = y2 - y1
    return pygame.Rect(x1, y1, largura, altura)


# Dimensões da tela (ajuste conforme necessário para seu tabuleiro e cartas)
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

# --- DEFINIÇÃO DOS COMPONENTES DO JOGO  ---
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

# Carregar imagens de suspeitos
images['suspeitos'] = {name: load_image(filepath, (70, 100)) for name, filepath in SUSPEITOS.items()}
# Carregar imagens de métodos
images['metodos'] = {name: load_image(filepath, (70, 100)) for name, filepath in METODOS.items()}
# Carregar imagens de locais (usadas como cartas)
images['locais_cartas'] = {name: load_image(filepath, (70, 100)) for name, filepath in LOCAIS.items()}
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
        # lista com todas as casas de início disponíveis no mapa -b 
        start_positions = ["Ponto"]
        # embaralha a lista para garantir q ta random -b
        random.shuffle(start_positions)
        
        # cria a lista de jogadores, dando a cada um uma posição única - b
        self.players = []
        for i, name in enumerate(player_names):
            posicao_inicial = "PONTO_DE_PARTIDA" 
            player = Player(name, i + 1, images['players_pawns'][i+1], posicao_inicial)
            self.players.append(player)
            print(f"Jogador {name} criado na posição inicial {posicao_inicial}") #mudei a lógica de mapa então pode estar bugado - b

    
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.game_state = "PLAYER_TURN"

        self.solution = {}
        self.deal_cards()

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
           "PONTO_DE_PARTIDA": list(LOCAIS.keys())
        }
        
        images['btn_dados'] = load_image("rolar_dados.gif", (150, 50)) #torcer pro gif funcionar - não funcionou - trocar a imagem dps - b
        self.valid_moves = []
        self.dice_roll = 0
        self.game_state = "AWAITING_ROLL"

    def roll_dice(self):
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        self.dice_roll = dado1 + dado2
        print(f"{self.current_player.name} tirou {self.dice_roll}")

        current_pos = self.current_player.position
    
        if self.dice_roll <= 7:
            # movimento curto: apenas pra salas vizinhas -b
            self.valid_moves = self.mapa_do_tabuleiro.get(current_pos, [])
        else:
            # movimento longo: pra qualquer sala, em duvida se devo manter - b
            self.valid_moves = list(self.casas_pixel_coords.keys())
            # tira a própria sala e o ponto de partida das opções - b
            if current_pos in self.valid_moves: self.valid_moves.remove(current_pos)
            if "PONTO_DE_PARTIDA" in self.valid_moves: self.valid_moves.remove("PONTO_DE_PARTIDA")

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
        print(f"SOLUÇÃO SECRETA (para teste): {self.solution}") # DEBUG - B
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
            # só mudei pra usar o mapa lógico dali de cima - B
            pixel_pos = self.casas_pixel_coords.get(player.position)
            if pixel_pos:
                screen.blit(player.pawn_image, pixel_pos)
                text_surface = small_font.render(player.name, True, BLACK)
                screen.blit(text_surface, (pixel_pos[0], pixel_pos[1] - 20))

        if self.game_state == "PLAYER_MOVING":
            for sala_nome in self.valid_moves:
                rect = self.salas_rects.get(sala_nome)
            if rect:
                #cria um retangulo com 50% de opacidade em cima da sala, PRECISA SER MELHORADO! - B
                s = pygame.Surface(rect.size, pygame.SRCALPHA)
                # Pinta essa superfície com uma cor (verde com 50% de opacidade) - pinta de verde - B
                s.fill((0, 255, 0, 128)) 
                # Desenha em cima da sala, a lógica aqui ainda tá confusa, não preenche todas as salas que o jogador pode ir e atualmente nem eu sei qual ta sendo a lógica - B
                screen.blit(s, rect.topleft)
        # --- Lógica de desenhar a mão do jogador ---
        # Modifiquei pra quebrar a linha depois da quarta carta - B
        text_surface = font.render(f"Mao de {self.current_player.name}:", True, BLACK)
        screen.blit(text_surface, (930, 20))
        start_x, start_y, margin, cards_per_row = 930, 50, 10, 4
        x_offset, y_offset = start_x, start_y
        card_width, card_height = 70, 100
        for i, card_name in enumerate(self.current_player.hand):
            card_image = images.get('suspeitos', {}).get(card_name) or images.get('metodos', {}).get(card_name) or images.get('locais_cartas', {}).get(card_name) or images['verso_carta']
            if i > 0 and i % cards_per_row == 0:
                x_offset = start_x
                y_offset += card_height + margin
            screen.blit(card_image, (x_offset, y_offset))
            x_offset += card_width + margin
        if self.game_state == "AWAITING_ROLL":
            screen.blit(images['btn_dados'], (930, 600))
        # --- Desenhar UI (botões, textos, etc.) ---
        screen.blit(images['btn_acusar'], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        turn_text = font.render(f"Vez de: {self.current_player.name}", True, BLACK)
        screen.blit(turn_text, (930, SCREEN_HEIGHT - 150 ))

    def handle_click(self, pos):   # LEMBRETE - Corrigir depois para não permitir jogadores ficarem na mesma casa
        
        # --- Botão de acusar, ainda está inoperante - B
        acusar_rect = images['btn_acusar'].get_rect(topleft=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        if acusar_rect.collidepoint(pos):
            print(f"Botão 'Acusar' clicado pelo jogador {self.current_player.name}!")
            # (Aqui entrará a lógica de acusação)
            return

        # ESTADO DE ESPERA PELA ROLAGEM DE DADOS - B 
        if self.game_state == "AWAITING_ROLL":
            dados_rect = images['btn_dados'].get_rect(topleft=(930, 600))
            if dados_rect.collidepoint(pos):
                self.roll_dice()
            return # termina o processamento do clique aqui neste turno -b

        # --- Movimentação do jogador - Tem como melhorar, mas no momento é o que temos - B
        if self.game_state == "PLAYER_MOVING":
            for sala_nome in self.valid_moves:
                rect = self.salas_rects.get(sala_nome)
                if rect and rect.collidepoint(pos):
                    self.current_player.position = sala_nome
                    self.current_player.location = sala_nome
                    print(f"{self.current_player.name} moveu para {sala_nome}")
                    
                    # Prepara para o próximo turno
                    self.valid_moves = []
                    self.game_state = "AWAITING_ROLL" 
                    self.current_player_index = (self.current_player_index + 1) % len(self.players)
                    self.current_player = self.players[self.current_player_index]
                    return # se deu td certo ele devolve a ação - B

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