from tkinter import filedialog, messagebox

import numpy as np
import pygame
from PIL import Image
from numpy.core.multiarray import asarray

pygame.init()


class graphiKart:
    def __init__(self, resolution):
        self.currentImageMatrix = None
        self.resolution = resolution
        self.window = pygame.display.set_mode(self.resolution)
        self.isWindowOpen = True
        self.gridSize = (500, 500)
        self.pixelSize = 10
        self.gridBorderSpace = 10
        self.gridMatrix = np.empty((self.gridSize[0] // self.pixelSize, self.gridSize[1] // self.pixelSize))
        self.colorMatrix = np.array([
            [0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19],
            [20, 21, 22, 23, 24]
        ])
        self.colorBox = pygame.Rect(50, 575, 100, 100)
        self.dicoColor = {0: [0, 0, 0], 1: [255, 255, 255], 2: [255, 192, 203], 3: [128, 0, 128], 4: [0, 255, 0],
                          5: [0, 255, 255], 6: [240, 230, 140], 7: [255, 165, 0], 8: [125, 125, 125],
                          9: [240, 255, 255], 10: [128, 0, 0], 11: [50, 205, 50], 12: [245, 222, 179],
                          13: [255, 255, 0], 14: [192, 192, 192], 15: [0, 128, 128], 16: [0, 0, 128], 17: [0, 255, 255],
                          18: [64, 224, 208], 19: [165, 42, 42], 20: [255, 0, 0], 21: [75, 0, 130], 22: [250, 235, 215],
                          23: [220, 20, 60], 24: [0, 0, 255], 25: (255, 255, 255)}
        self.currentColor = 1
        self.gridRect = pygame.Rect((self.gridBorderSpace, 50, self.gridSize[1], self.gridSize[1]))
        self.eraseButton = pygame.Rect((self.resolution[0] - 150, 600, 100, 50))
        self.eraseSmallButton = pygame.Rect((self.resolution[0] - 40, 600, 10, 10))
        self.eraseBigButton = pygame.Rect((self.resolution[0] - 40, 630, 20, 20))
        self.cleanButton = pygame.Rect((self.resolution[0] - 300, 600, 100, 50))
        self.saveButton = pygame.Rect((10, 10, 80, 30))
        self.saveAsButton = pygame.Rect((110, 10, 150, 30))
        self.openButton = pygame.Rect((280, 10, 80, 30))
        self.eraseActivate = True
        self.isMouseButtonLeft = True
        self.eraserSize = 0
        self.currentFile = ""
        self.currentImage = None

        self.font = pygame.font.SysFont("comicsans", 30)

        self.eraseButtonRender = self.font.render("erase", False, "black")
        self.cleanButtonRender = self.font.render("clean", False, "black")
        self.saveButtonRender = self.font.render("save", False, "black")
        self.saveAsButtonRender = self.font.render("save as", False, "black")
        self.openButtonRender = self.font.render("open", False, "black")

        pygame.display.set_caption("graphikArt")

    def main(self):
        self.initialize()
        while self.isWindowOpen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isWindowOpen = False
                    pygame.quit()
                elif event.type == pygame.VIDEORESIZE:
                    self.grid_border_space()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if not self.eraseActivate:
                            self.draw_cell(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        else:
                            self.erase(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        if self.eraseButton.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            self.erase_button_clicked()
                        self.select_eraser_size(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        self.change_color(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        self.clean(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        self.save(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        self.save_as(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        self.open(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.isMouseButtonLeft = True

            if self.isWindowOpen:
                self.window.fill("white")

                self.drawing()

                pygame.display.flip()

    def initialize(self):
        self.gridMatrix.fill(25)

    def grid_border_space(self):
        self.gridBorderSpace = (self.window.get_width() - self.gridSize[1]) / 2

    def drawing(self):
        self.draw_grid()
        self.draw_parameter()
        pygame.draw.rect(self.window, "black", self.eraseButton, width=1)
        pygame.draw.rect(self.window, "black", self.eraseSmallButton, width=1)
        pygame.draw.rect(self.window, "black", self.eraseBigButton, width=1)
        pygame.draw.rect(self.window, "black", self.cleanButton, width=1)
        pygame.draw.rect(self.window, "black", self.saveButton, width=1)
        pygame.draw.rect(self.window, "black", self.saveAsButton, width=1)
        pygame.draw.rect(self.window, "black", self.openButton, width=1)
        self.window.blit(self.eraseButtonRender, (
            self.resolution[0] - 150 + (self.eraseButton.width - self.eraseButtonRender.get_width()) / 2, 600))
        self.window.blit(self.cleanButtonRender, (
            self.resolution[0] - 300 + (self.cleanButton.width - self.cleanButtonRender.get_width()) / 2, 600))
        self.window.blit(self.saveButtonRender, (10 + (self.saveButton.width - self.saveButtonRender.get_width()) / 2,
                                                 (self.saveButton.height - self.saveButtonRender.get_height()) / 2))
        self.window.blit(self.saveAsButtonRender, (
            110 + (self.saveAsButton.width - self.saveAsButtonRender.get_width()) / 2,
            (self.saveAsButton.height - self.saveAsButtonRender.get_height()) / 2))
        self.window.blit(self.openButtonRender, (280 + (self.openButton.width - self.openButtonRender.get_width()) / 2,
                                                 (self.openButton.height - self.openButtonRender.get_height()) / 2))
        if not self.isMouseButtonLeft:
            if not self.eraseActivate:
                self.draw_cell(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            else:
                self.erase(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    def draw_grid(self):
        for i in range(self.gridSize[1] // self.pixelSize + 1):
            pygame.draw.line(self.window, "gray", (i * self.pixelSize + self.gridBorderSpace, 50),
                             (i * self.pixelSize + self.gridBorderSpace, self.gridSize[1] + 50))
            pygame.draw.line(self.window, "gray", (self.gridBorderSpace, i * self.pixelSize + 50),
                             (self.gridBorderSpace + self.gridSize[1], i * self.pixelSize + 50))
        for i in range(self.gridMatrix.shape[0]):
            for j in range(self.gridMatrix.shape[1]):
                if self.gridMatrix[i][j] != 25:
                    pygame.draw.rect(self.window, self.dicoColor[self.gridMatrix[i][j]],
                                     (j * self.pixelSize + 10, i * self.pixelSize + 50, 10, 10))
            pygame.draw.rect(self.window, "black", self.gridRect, width=1)

    def draw_parameter(self):
        k = 0
        pygame.draw.rect(self.window, "black", self.colorBox)
        for i in range(5):
            for j in range(5):
                pygame.draw.rect(self.window, self.dicoColor[k], (j * 20 + 50, i * 20 + 575, 20, 20))
                k += 1

    def draw_cell(self, x, y):
        if self.gridRect.collidepoint(x, y):
            self.isMouseButtonLeft = False
            if self.gridMatrix[((y - y % self.pixelSize) - 50) // self.pixelSize][
                ((x - x % self.pixelSize) - self.gridBorderSpace) // self.pixelSize] != self.currentColor:
                self.gridMatrix[((y - y % self.pixelSize) - 50) // self.pixelSize][
                    ((x - x % self.pixelSize) - self.gridBorderSpace) // self.pixelSize] = self.currentColor

    def change_color(self, x, y):
        if self.colorBox.collidepoint(x, y):
            self.currentColor = self.colorMatrix[((y - y % self.pixelSize) - 575) // 20][
                ((x - x % self.pixelSize) - 50) // 20]
            self.eraseActivate = False

    def erase_button_clicked(self):
        self.eraseActivate = True

    def erase(self, x, y):
        if self.gridRect.collidepoint(x, y):
            coord = [((y - y % self.pixelSize) - 50) // self.pixelSize - 1,
                     ((x - x % self.pixelSize) - self.gridBorderSpace) // self.pixelSize - 1]
            self.isMouseButtonLeft = False
            if self.eraserSize == 0:
                self.gridMatrix[coord[0] + 1][coord[1] + 1] = 25
            else:
                try:
                    self.gridMatrix[coord[0]:coord[0] + 3, coord[1]:coord[1] + 3] = 25
                except:
                    pass

    def clean(self, x, y):
        if self.cleanButton.collidepoint(x, y):
            self.gridMatrix.fill(25)

    def select_eraser_size(self, x, y):
        if self.eraseSmallButton.collidepoint(x, y):
            self.eraserSize = 0
        elif self.eraseBigButton.collidepoint(x, y):
            self.eraserSize = 1

    def save_as(self, x, y):
        global image, filename
        imageMatrix = np.empty((50, 50, 3), dtype=np.uint8)
        if self.saveAsButton.collidepoint(x, y):
            try:
                filename = filedialog.asksaveasfile(initialfile='Untitled.png', defaultextension=".png",
                                                    filetypes=[("Images", "*.png")])
                for i in range(50):
                    for j in range(50):
                        imageMatrix[i, j] = [self.dicoColor[self.gridMatrix[i, j]][0],
                                             self.dicoColor[self.gridMatrix[i, j]][1],
                                             self.dicoColor[self.gridMatrix[i, j]][2]]
                        image = Image.fromarray(imageMatrix, 'RGB')
                image.save(filename.name)
                self.currentFile = filename.name
            except:
                pass

    def save(self, x, y):
        global image
        imageMatrix = np.empty((50, 50, 3), dtype=np.uint8)
        if self.saveButton.collidepoint(x, y) and self.currentFile != "":
            for i in range(50):
                for j in range(50):
                    imageMatrix[i, j] = [self.dicoColor[self.gridMatrix[i, j]][0],
                                         self.dicoColor[self.gridMatrix[i, j]][1],
                                         self.dicoColor[self.gridMatrix[i, j]][2]]
                    image = Image.fromarray(imageMatrix, 'RGB')
            image.save(self.currentFile)

    def open(self, x, y):
        if self.openButton.collidepoint(x, y):
            try:
                filename = filedialog.askopenfilename(title='Open a file', initialdir='/',
                                                      filetypes=(('Images files', '*.png'), ("all files", "*.png")))
                self.currentImage = Image.open(filename)
                self.currentImageMatrix = asarray(self.currentImage)
                self.image_decomposer()
                self.currentFile = filename
            except:
                messagebox.showerror("Error", "can't open the file")

    def image_decomposer(self):
        for i in range(50):
            for j in range(50):
                color = list(self.currentImageMatrix[i, j])
                for k in range(len(self.dicoColor)):
                    if self.dicoColor[k] == color:
                        self.gridMatrix[i, j] = k


if __name__ == "__main__":
    try:
        graphiKart((520, 700)).main()
    except:
        messagebox.showerror("Error", "application stop running")
