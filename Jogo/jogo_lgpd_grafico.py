import pygame
import sys
import os
import random

# --- CONFIGURAÇÕES BÁSICAS ---
pygame.init()

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
images = {}
def load_image(filepath, scale=None):
    """Carrega uma imagem e opcionalmente a escala."""
    full_path = os.path.join(os.getcwd(), filepath) # Garante que o caminho é absoluto
    try:
        image = pygame.image.load(full_path).convert_alpha() # convert_alpha para imagens com transparência
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Erro ao carregar imagem {filepath}: {e}")
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
    def __init__(self, name, player_id, pawn_image):
        self.name = name
        self.id = player_id
        self.pawn_image = pawn_image
        self.location = "Ponto de Partida"
        self.pixel_pos = (50, 50 + (player_id-1) * 50)
        self.hand = []

    def draw(self, screen):
        screen.blit(self.pawn_image, self.pixel_pos)
        text_surface = small_font.render(self.name, True, BLACK)
        screen.blit(text_surface, (self.pixel_pos[0], self.pixel_pos[1] - 20))


class Game:
    def __init__(self, player_names):
        self.players = [Player(name, i + 1, images['players_pawns'][i+1]) for i, name in enumerate(player_names)]
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.game_state = "waiting_for_input"
        
        # ATENÇÃO: Você precisará ajustar estas coordenadas para corresponderem ao seu tabuleiro!
        self.locations_pixel_coords = {
            "Ponto de Partida": (50, 50), "RH": (150, 100), "TI": (250, 100),
            "Marketing": (350, 100), "Call Center": (150, 200), "Financeiro": (250, 200),
            "Juridico": (350, 200), "Diretoria": (150, 300), "Data Center": (250, 300),
            "Servidor em Nuvem": (350, 300), "Reuniao Online": (150, 400), "Estacionamento": (250, 400),
        }
        
        # Exemplo de distribuição de cartas (APENAS PARA DEMONSTRAR O DRAWING)
        self.players[0].hand.append(list(SUSPEITOS.keys())[0])
        self.players[0].hand.append(list(METODOS.keys())[0])
        if len(self.players) > 1:
            self.players[1].hand.append(list(LOCAIS.keys())[0])


    def draw_game_elements(self):
        screen.blit(images['tabuleiro'], (0, 0))
        for player in self.players:
            player.pixel_pos = self.locations_pixel_coords.get(player.location, player.pixel_pos)
            player.draw(screen)

        current_player_hand_x = 930
        current_player_hand_y = 50
        text_surface = font.render(f"Mao de {self.current_player.name}:", True, BLACK)
        screen.blit(text_surface, (current_player_hand_x, current_player_hand_y - 30))

        card_offset_x = 0
        for card_name in self.current_player.hand:
            card_image = images.get('suspeitos', {}).get(card_name) or \
                         images.get('metodos', {}).get(card_name) or \
                         images.get('locais_cartas', {}).get(card_name) or \
                         images['verso_carta']
            
            screen.blit(card_image, (current_player_hand_x + card_offset_x, current_player_hand_y))
            card_offset_x += 80

        screen.blit(images['btn_acusar'], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        turn_text = font.render(f"Vez de: {self.current_player.name}", True, BLACK)
        screen.blit(turn_text, (930, SCREEN_HEIGHT / 2))

    def handle_click(self, pos):
        button_rect = images['btn_acusar'].get_rect(topleft=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        if button_rect.collidepoint(pos):
            print(f"Botão 'Acusar' clicado pelo jogador {self.current_player.name}!")

        for loc_name, loc_coords in self.locations_pixel_coords.items():
            distance = ((pos[0] - loc_coords[0])**2 + (pos[1] - loc_coords[1])**2)**0.5
            if distance < 30:
                print(f"{self.current_player.name} clicou para mover para: {loc_name}")
                self.current_player.location = loc_name
                # Passa o turno após o movimento (exemplo simples)
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                self.current_player = self.players[self.current_player_index]
                break

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