import pygame
import numpy as np
import math

# --- 設定 ---
WIDTH, HEIGHT = 400, 300
SCALE = 2                 # 画面表示サイズ（ドット感を出すため）

def run_plasma():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pygame.display.set_caption("Old Megademo Plasma")
    clock = pygame.time.Clock()

    # 描画用のサーフェス
    surface = pygame.Surface((WIDTH, HEIGHT))

    # 座標グリッドの作成 (x, y)
    x = np.linspace(0, 1, WIDTH)
    y = np.linspace(0, 1, HEIGHT)
    xv, yv = np.meshgrid(x, y)

    running = True
    t = 0.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t += 0.05

        # --- プラズマ計算 (NumPyで高速演算) ---
        v = np.sin(xv * 10.0 + t)        # 縦波
        v += np.sin(10.0 * (xv * np.sin(t / 2.0) + yv * np.cos(t / 3.0)) + t)   # 横
        cx = xv + 0.5 * np.sin(t / 5.0)
        cy = yv + 0.5 * np.cos(t / 3.0)
        v += np.sin(np.sqrt(100.0 * (cx**2 + cy**2) + 1.0) + t)  # 円状

        # 正規化&色変換
        r = (np.sin(v * np.pi) * 127 + 128).astype(np.uint8)
        g = (np.sin(v * np.pi + 2 * np.pi / 3) * 127 + 128).astype(np.uint8)
        b = (np.sin(v * np.pi + 4 * np.pi / 3) * 127 + 128).astype(np.uint8)

        # 3次元配列にスタック (height, width, 3)
        rgb = np.stack((r, g, b), axis=-1)

        # Pygameのサーフェスに転送(BLIT = bit block transfer)
        pygame.surfarray.blit_array(surface, rgb.swapaxes(0, 1))
        
        # 画面に合わせて拡大表示
        scaled_surface = pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE))
        screen.blit(scaled_surface, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_plasma()
