import pygame.font


class Button():
    def __init__(self, screen, ai_settings, msg) -> None:
        """ Initialize Button attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set dimensions and ui properties of Button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        # ----- None -> default font , 48-> font size
        self.font = pygame.font.SysFont(None, 48)

        # Build the button rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The Button msg needs to be preped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Turn msg into a image and center text on the button """
        # in pygame text is rendered as image

        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)  # True-> aniti aliasing

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)  # ---draws blank button
        # --- draws the text image
        self.screen.blit(self.msg_image, self.msg_image_rect)
