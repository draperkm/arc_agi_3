import numpy as np
import matplotlib.pyplot as plt

PALETTE = np.array([
    [0,   0,   0  ],  # 0  black
    [30,  147, 255],  # 1  blue
    [247, 3,   40 ],  # 2  red
    [79,  204, 48 ],  # 3  green
    [255, 220, 0  ],  # 4  yellow
    [153, 153, 153],  # 5  grey
    [229, 58,  163],  # 6  fuchsia
    [255, 133, 27 ],  # 7  orange
    [135, 216, 241],  # 8  azure
    [146, 18,  49 ],  # 9  maroon
    [255, 255, 255],  # 10 extended
    [255, 165, 0  ],  # 11 extended
    [128, 0,   128],  # 12 extended
], dtype=np.uint8)


def render_frame(frame, title=None, ax=None):
    """Render a (64,64) int8 color-index frame as an RGB image."""
    rgb = PALETTE[frame]
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(rgb, interpolation='nearest')
    ax.axis('off')
    if title:
        ax.set_title(title)
    else:
        ax.set_title('')
    plt.tight_layout()
    plt.show()


def render_frames(frames, titles=None):
    """Render multiple (64,64) frames side by side."""
    n = len(frames)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 6))
    if n == 1:
        axes = [axes]
    for i, (frame, ax) in enumerate(zip(frames, axes)):
        rgb = PALETTE[frame]
        ax.imshow(rgb, interpolation='nearest')
        ax.axis('off')
        if titles and i < len(titles):
            ax.set_title(titles[i])
        else:
            ax.set_title(f'frame {i}')
    plt.tight_layout()
    plt.show()
