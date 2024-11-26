import pygame

class TextEngine:
    def __init__(self, font:pygame.Font=None, font_size=20, text_speed=10, line_pause=30, stop_pause=15, fps=60):
        """Initialize the text engine with customizable parameters"""
        pygame.init()

        self.char = ""
        self.row_idx = 0
        self.clm_idx = 0
        self.pause_timer = 0
        self.typing_timer = 0
        self.completed = False  # Track if the text is fully displayed

        self.font_size = font_size
        self.text_speed = text_speed
        self.line_pause = line_pause
        self.stop_pause = stop_pause
        self.fps = fps

        # Font setup
        self.font = font or pygame.font.SysFont("monospace ", font_size)

    def is_punctuation(self, character):
        """Check if a character is punctuation"""
        return character in ".!?"

    def set_pause(self, duration):
        """Set a pause timer for a specified duration."""
        self.pause_timer = duration

    def load_text(self, text:str, separator="\n"):
        """Load text into the engine and reset variables"""
        self.texts = text.strip().split(separator)
        self.char = ""
        self.row_idx = 0
        self.clm_idx = 0
        self.pause_timer = 0
        self.typing_timer = 0
        self.completed = False

    def update(self, keys, skip_key):
        """Update text rendering logic"""
        wait = True
        if self.pause_timer > 0:
            self.pause_timer -= 1
        else:
            self.typing_timer += 1
            # Skip functionality
            if keys[skip_key] and self.row_idx < len(self.texts):
                # self.char += self.texts[self.row_idx][self.clm_idx:] + "\n"
                # self.row_idx += 1
                # self.clm_idx = 0
                self.set_pause(self.line_pause if self.row_idx < len(self.texts) else 0)
            elif self.typing_timer >= self.fps // self.text_speed:
                self.typing_timer = 0
                if self.row_idx < len(self.texts):
                    current_char = self.texts[self.row_idx][self.clm_idx]
                    self.char += current_char
                    self.clm_idx += 1
                    wait = True

                    # Pause on punctuation
                    if self.is_punctuation(current_char):
                        self.set_pause(self.stop_pause)

                    # Move to the next line
                    if self.clm_idx >= len(self.texts[self.row_idx]):
                        while wait:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:                                    
                                    wait = False
                        self.row_idx += 1
                        self.clm_idx = 0
                        self.char += "\n"
                        self.set_pause(self.line_pause)

        if self.row_idx >= len(self.texts):
            self.completed = True  # Mark text as completed

    def render(self, surface:pygame.Surface, position, text_color=(255, 255, 255)):
        """Render the current text on the given surface with word wrap."""

        text_surface = self.font.render(self.char, True, text_color)
        surface.blit(text_surface, position)


def main():
    # Example Sample
    texts = """
Hello Traveller!
What made you come to this poor farmer?
Traveller?
TRAVELLER?        
"""
    Engine = TextEngine()
    Engine.load_text(texts)
    
    screen = pygame.display.set_mode((1000,500))
    clock = pygame.time.Clock()
    font = pygame.Font(None, 32)
    main_loop = True
    
    while main_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
        
        Engine.update(pygame.key.get_pressed(),pygame.K_q)

        screen.fill((25,25,25))

        Engine.render(screen,(50,50))

        pygame.display.flip()
        clock.tick()
    pygame.quit()


if __name__ == "__main__":
    main()